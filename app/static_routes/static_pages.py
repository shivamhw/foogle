from flask import Blueprint
from flask.templating import render_template
from flask import send_file

static_pages = Blueprint("static_pages", __name__)

@static_pages.route("/")
def index():
    return render_template('index.html')

@static_pages.route("/files.html")
def files_page():
    return render_template("files.html")

@static_pages.route("/robots.txt")
def robot():
    return send_file("../static/robots.txt")

@static_pages.route("/season_details/<series_id>/<season_id>")
def season_details(series_id, season_id):
    return render_template("season_details.html", series_id=series_id, season_id=season_id)

@static_pages.route("/series_details/<series_id>")
def series_details(series_id):
    return render_template("series_details.html", series_id=series_id)

@static_pages.route("/series.html")
def se_se():
    return render_template("series.html")