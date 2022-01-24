from __future__ import print_function
from flask import Flask, request, redirect
from flask.helpers import url_for
from flask.templating import render_template
import base64
import urllib.parse
import requests
from .utils import QueryMaker
from .gdrive import  GDriveHelper
from .exceptions import FileAccessError

def create_app(CF_WORKER_SITE, DRIVE_ID, TOKEN_JSON_PATH, CRED_JSON_PATH, TEMP_FOLDER):
    app = Flask(__name__)
    gd = GDriveHelper(TOKEN_JSON_PATH, CRED_JSON_PATH, TEMP_FOLDER)

    @app.route("/")
    def index():
        return render_template('index.html')

    @app.route("/series_search")
    def s_search():
        search_data = [None] * 3
        search_data[0], search_data[1], search_data[2] = request.args.get("name"), request.args.get(
            "sess_nm"), request.args.get("epi_nm")
        list_file = []
        alternate_q = QueryMaker.make_query(
            QueryMaker.series_querymaker, search_data)
        for q in alternate_q["q"]:
            list_file = gd.search(q)
            # print("inuse q : ", q, "Results :: ", len(list_file), list_file)
            if len(list_file) != 0:
                break
        if len(list_file) == 0:
            return render_template("error.html", error=["No results for that one! Might consider checking spelling."])
        return render_template('result.html', my_list=list_file)

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
        b64_name = f"/{DRIVE_ID}:/{link_dict['raw_name']}".encode("utf-8")
        b64_name = base64.b64encode(b64_name)
        b64_name = b64_name.decode("utf-8")
        url_name = urllib.parse.quote(link_dict['raw_name'])
        link_dict['web_player'] = f"{CF_WORKER_SITE}{DRIVE_ID}:video/{b64_name}"
        link_dict['direct_link'] = f"{CF_WORKER_SITE}{DRIVE_ID}:/{url_name}"
        link_dict['vlc_link'] = f"vlc://{CF_WORKER_SITE}{DRIVE_ID}:/{url_name}"
        check_code = requests.head(link_dict['g_link']).status_code
        if  check_code != 200 and check_code != 302:
            return render_template('error.html', error=[f"broken link!! Try other links. RT{str(check_code)}"])
        return render_template("links.html", link_dict=link_dict)

    @app.route("/process_file/<file_id>")
    def process_f(file_id):
        try:
            dst_file_id = gd.prepare_file(file_id)
            # print(dst_file_id)
            if dst_file_id == None:
                return "error at getting new file"
        except Exception as e:
            print(e)
            return render_template("error.html", error = ["this one is on me :)" ,str(e)])
        return redirect(url_for('links', file_id=dst_file_id))

    @app.route("/search")
    def search_handler():
        query = request.args.get("search_box")
        queries = QueryMaker.make_query(QueryMaker.movie_querymaker, [query])
        for query in queries["q"]:
            print("q : ", query)
            list_file = gd.search(query)
            if len(list_file) != 0:
                break
        else:
            return render_template("error.html", error=["No results for that one! Might consider checking spelling."])
        return render_template('result.html', my_list=list_file)
    return app
