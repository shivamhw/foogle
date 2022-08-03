from flask import Flask, request, redirect, send_file
from flask.helpers import url_for
from flask.templating import render_template
import requests
from .utils import QueryMaker, LinkMaker
from .search_handler import SearchHandler
from .gdrive import  GDriveHelper, FileAccessError
from .api.api_app import create_blueprint

def create_app(CF_WORKER_SITE, TOKEN_JSON_PATH, CRED_JSON_PATH, TEMP_FOLDER):
    app = Flask(__name__)
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    gd = GDriveHelper(TOKEN_JSON_PATH, CRED_JSON_PATH, TEMP_FOLDER)
    app.register_blueprint(create_blueprint(gd, CF_WORKER_SITE), url_prefix="/api")
    links_result = LinkMaker(CF_WORKER_SITE, stream_link=True, process_link=True, cf_download_link=True)
    link_final_page = LinkMaker(CF_WORKER_SITE, stream_link=True, gdrive_link=True, cf_download_link=True)

    @app.route("/")
    def index():
        return render_template('index.html')

    @app.route("/files.html")
    def files_page():
        return render_template("files.html")

    @app.route("/robots.txt")
    def robot():
        return send_file("robots.txt")

    @app.route("/season_details/<series_id>/<season_id>")
    def season_details(series_id, season_id):
        return render_template("season_details.html", series_id=series_id, season_id=season_id)

    @app.route("/series_details/<series_id>")
    def series_details(series_id):
        return render_template("series_info.html", series_id=series_id)

    @app.route("/series.html")
    def se_se():
        return render_template("series.html")

    @app.route("/series_search")
    def s_search():
        search_data = [None] * 3
        search_data[0], search_data[1], search_data[2] = request.args.get("search_box"), request.args.get(
            "sess_nm"), request.args.get("epi_nm")
        list_file = []
        alternate_q = QueryMaker.make_query(
            QueryMaker.series_querymaker, search_data)
        for q in alternate_q["q"]:
            print("execute query ", q)
            result = gd.search(q)
            print(len(result))
            if len(result) != 0:
                list_file += result
            if len(list_file) > 5:
                break
        if len(list_file) == 0:
            return render_template("error.html", error=["No results for that one! Might consider checking spelling."])
        for i in list_file:
            i = links_result.make_links(i)
        print(list_file)
        return render_template('result.html', my_list=list_file)

    @app.route("/links")
    def links():
        file_id = request.args.get("file_id")
        try:
            file_info = gd.get_file_info(file_id)
            check_code = requests.head(file_info["webContentLink"]).status_code
            if  check_code not in [200, 302, 303]:
                raise requests.exceptions.HTTPError("Got invalid status code")
        except FileAccessError as e:
            return render_template('error.html', error=[f"broken link!! Try other links.", f"{str(e)}"])
        except requests.exceptions.HTTPError as e:
            return render_template('error.html', error=[f"broken link!! Try other links. RT{str(e)}"])
        file_info = link_final_page.make_links(file_info)
        return render_template("links.html", link_dict=file_info)

    @app.route("/process_file/<file_id>")
    def process_f(file_id):
        try:
            dst_file_id = gd.prepare_file(file_id)
            if dst_file_id == None:
                return "error at getting new file"
        except Exception as e:
            print(e)
            return render_template("error.html", error = ["this one is on me :)" ,str(e)])
        return redirect(url_for('links', file_id=dst_file_id))

    @app.route("/search")
    def search_handler():
        query = {}
        query["name"] = request.args.get("search_box")
        query["release_year"] = request.args.get("release_year", None)
        list_file = []
        sh = SearchHandler(gd)
        print(query)
        list_file = sh.search(query, QueryMaker.movie_querymaker)
        if len(list_file) == 0:
            return render_template("error.html", error=["No results for that one! Might consider checking spelling."])
        for i in list_file:
            i = links_result.make_links(i)
        return render_template('result.html', my_list=list_file)

    @app.route("/file_search")
    def file_search_handler():
        query = [None] *2
        query[0], query[1] = request.args.get("search_box"), request.args.get("type", None)
        queries = QueryMaker.make_query(QueryMaker.files_querymaker, query)
        print(queries)
        for q in queries["q"]:
            print(q)
            list_of_files = gd.search(q)
        if(len(list_of_files) == 0):
            return render_template("error.html", error=["No results for that one! Might consider checking spelling."])
        for i in list_of_files:
            i = links_result.make_links(i)
        return render_template('result.html', my_list=list_of_files)

    return app