from flask import Flask, request
from flask.templating import render_template
from .utils import QueryMaker, Utils
from .search_handler import SearchHandler
from .gdrive import GDriveHelper
from .api.api_app import create_blueprint
from .static_routes.static_pages import handle_static_pages
from .data import Config, AppConfig, SeriesSearchRequest

context = None


def create_app(config: Config):
    group = config.tele_group
    bot = config.tele_bot
    app = Flask(__name__)
    gd = GDriveHelper(config.token_path, config.cred_path)
    search_handler = SearchHandler(gd)
    context = AppConfig(group=group, bot=bot, app=app, search_handler=search_handler, gd=gd, config=config)
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.register_blueprint(create_blueprint(context), url_prefix="/api")
    app.register_blueprint(handle_static_pages(), url_prefix="/")

    @app.route("/series_search")
    def series_search():
        series = SeriesSearchRequest(request.args.get("search_box"), request.args.get(
            "sess_nm"), request.args.get("epi_nm"))
        queries = QueryMaker.series_querymaker(series)
        results = context.search_handler.search(queries)
        if len(results) == 0:
            return render_template("error.html", error=["No results for that one! Might consider checking spelling."])
        return render_template('result.html', my_list=results)

    @app.route("/search")
    def movie_search_handler():
        movie_name = request.args.get("search_box")
        movie_release_year = request.args.get("release_year", "")
        queries = QueryMaker.movie_querymaker(movie_name, movie_release_year)
        results = context.search_handler.search(queries)
        Utils.make_inline_links(results, context)
        if len(results) == 0:
            return render_template("error.html", error=["No results for that one! Might consider checking spelling."])
        return render_template('result.html', my_list=results)

    @app.route("/file_search")
    def file_search_handler():
        query = request.args.get("search_box")
        queries = QueryMaker.files_querymaker(query)
        results = context.search_handler.search(queries)
        Utils.make_inline_links(results, context)
        if len(results) == 0:
            return render_template("error.html", error=["No results for that one! Might consider checking spelling."])
        return render_template('result.html', my_list=results)

    return app
