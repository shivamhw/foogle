from flask import Flask, request, redirect, send_file
from flask.helpers import url_for
from flask.templating import render_template
import requests
from .utils import QueryMaker
from .gdrive import  GDriveHelper
from .exceptions import FileAccessError
from urllib.parse import quote

def create_app(CF_WORKER_SITE, TOKEN_JSON_PATH, CRED_JSON_PATH, TEMP_FOLDER):
    app = Flask(__name__)
    gd = GDriveHelper(TOKEN_JSON_PATH, CRED_JSON_PATH, TEMP_FOLDER)

    @app.route("/")
    def index():
        return render_template('index.html')

    @app.route("/robots.txt")
    def robot():
        return send_file("robots.txt")

    @app.route("/series_search")
    def s_search():
        search_data = [None] * 3
        search_data[0], search_data[1], search_data[2] = request.args.get("search_box"), request.args.get(
            "sess_nm"), request.args.get("epi_nm")
        list_file = []
        print(search_data, "dekhlo")
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
        return render_template('result.html', my_list=list_file, cf_worker=CF_WORKER_SITE, function=quote)

    @app.route("/series.html")
    def se_se():
        return render_template("series.html")

    @app.route("/links")
    def links():
        file_id = request.args.get("file_id")
        link_dict = {}
        try:
            file_info = gd.get_file_info(file_id)
        except FileAccessError as e:
            return render_template('error.html', error=[f"broken link!! Try other links.", f"{str(e)}"])
        link_dict['size'] = file_info['size']
        link_dict['g_link'], link_dict['raw_name'], link_dict['id'] = file_info['webContentLink'], file_info["name"], file_info['id']
        link_dict['direct_link'] = f"{CF_WORKER_SITE}/getfile/{file_id}"
        link_dict["vlc_link"] = f"vlc://{CF_WORKER_SITE}/stream_file/{file_id}/{ quote(link_dict['raw_name']) }"

        check_code = requests.head(link_dict['g_link']).status_code
        if  check_code not in [200, 302, 303]:
            return render_template('error.html', error=[f"broken link!! Try other links. RT{str(check_code)}"])
        return render_template("links.html", link_dict=link_dict)

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
        query = request.args.get("search_box")
        list_file = []
        queries = QueryMaker.make_query(QueryMaker.movie_querymaker, [query])
        for query in queries["q"]:
            print("q : ", query)
            result = gd.search(query)
            print(len(result))
            if len(result) != 0:
                list_file += result
            if len(list_file) > 5:
                break
        if len(list_file) == 0:
            return render_template("error.html", error=["No results for that one! Might consider checking spelling."])
        return render_template('result.html', my_list=list_file, cf_worker=CF_WORKER_SITE, function=quote)

    @app.route("/files.html")
    def files_page():
        return render_template("files.html")

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
        return render_template('result.html', my_list=list_of_files,  cf_worker=CF_WORKER_SITE, function=quote)

    return app