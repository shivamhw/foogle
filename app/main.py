from flask import Flask, request, redirect, send_file
from flask.helpers import url_for
from flask.templating import render_template
import requests
from .utils import QueryMaker, LinkMaker, send_msg
from .search_handler import SearchHandler
from .gdrive import  GDriveHelper, FileAccessError
from .api.api_app import create_blueprint
from .db import LinkDB
import logging
import json
import random

bad_file_id_logger = logging.getLogger("bad_file")
blocklist = {}
bot = None
group = None
td_dir = None

def load_td(path):
    global td_dir
    with open(path, 'r') as f:
        td_dir = json.load(f)
    print(td_dir)

def get_temp(all=False):
    if all:
        return td_dir
    return random.choice(td_dir)

def create_app(CF_WORKER_SITE, TOKEN_JSON_PATH, CRED_JSON_PATH, TEMP_FOLDER, MONGOURI, TELE_BOT, GROUP):
    global bot
    global group
    group = GROUP
    bot = TELE_BOT
    app = Flask(__name__)
    db = LinkDB(MONGOURI)
    load_td(TEMP_FOLDER)
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    gd = GDriveHelper(TOKEN_JSON_PATH, CRED_JSON_PATH, get_temp)
    app.register_blueprint(create_blueprint(gd, CF_WORKER_SITE), url_prefix="/api")
    links_result = LinkMaker(CF_WORKER_SITE, stream_link=True, process_link=True, cf_download_link=True)
    link_final_page = LinkMaker(CF_WORKER_SITE, stream_link=True, gdrive_link=True, cf_download_link=True, td_override=True)
    logging.basicConfig(level=logging.WARNING, filemode="w", filename="main_log.log")
    bad_handler = logging.FileHandler("file_id.log")
    bad_file_id_logger.addHandler(bad_handler)
    blocklist["files"] = []
    blocklist["folders"] = []
    # blocklist["files"] = db.get_file_blocklist()
    # blocklist["folders"] = db.get_folder_blocklist()
    # print("Blocklist ", blocklist)

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
        return render_template("series_details.html", series_id=series_id)

    @app.route("/series.html")
    def se_se():
        return render_template("series.html")

    @app.route("/series_search")
    def s_search():
        search_data = [None] * 3
        search_data[0], search_data[1], search_data[2] = request.args.get("search_box"), request.args.get(
            "sess_nm"), request.args.get("epi_nm")
        send_msg(f"Series search handler :  {search_data[0]}", bot, group)
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
        td = request.args.get("td")
        td = td.replace("'", "\"")
        td = json.loads(td)
        try:
            file_info = gd.get_file_info(file_id)
            check_code = requests.head(file_info["webContentLink"]).status_code
            if  check_code not in [200, 302, 303]:
                raise requests.exceptions.HTTPError("Got invalid status code")
        except FileAccessError as e:
            bad_file_id_logger.error(f"Bad file : {file_id} {str(e)}")
            logging.exception("File Error in /links ")
            return render_template('error.html', error=[f"broken link!! Try other links.", f"{str(e)}"])
        except requests.exceptions.HTTPError as e:
            bad_file_id_logger.error(f"Bad file : {file_id} {str(e)}")
            logging.exception("HttpError in /links")
            return render_template('error.html', error=[f"broken link!! Try other links. RT{str(e)}"])
        file_info['td_override'] = td['name']
        file_info = link_final_page.make_links(file_info)
        return render_template("links.html", link_dict=file_info)

    @app.route("/process_file/<file_id>")
    def process_f(file_id):
        parents = None
        try:
            parents = gd.get_parents(file_id)
            print("got parent", parents)
            dst_file_id, td = gd.prepare_file(file_id, parents)
            if dst_file_id == None:
                return "error at getting new file"
        except Exception as e:
            bad_file_id_logger.error(f"Bad file : {file_id} | Parent :{parents} | {str(e)}")
            db.add_file_blocklist(file_id)
            if parents is not None:
                for parent in parents:
                    db.add_folder_blocklist(parent, file_id)
            return render_template("error.html", error = ["this one is on me :)" ,str(e)])
        return redirect(url_for('links', file_id=dst_file_id, td=td))

    @app.route("/search")
    def search_handler():
        global blocklist
        query = {}
        query["name"] = request.args.get("search_box")
        send_msg(f"Movie search handler :  {query['name']}", bot, group)
        query["release_year"] = request.args.get("release_year", None)
        list_file = []
        sh = SearchHandler(gd)
        list_file = sh.search(query, QueryMaker.movie_querymaker, blocklist)
        if len(list_file) == 0:
            return render_template("error.html", error=["No results for that one! Might consider checking spelling."])
        for i in list_file:
            i = links_result.make_links(i)
        return render_template('result.html', my_list=list_file)

    @app.route("/file_search")
    def file_search_handler():
        query = [None] *2
        query[0], query[1] = request.args.get("search_box"), request.args.get("type", None)
        send_msg(f"Custom search handler :  {query[0]}", bot, group)
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