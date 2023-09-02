from flask import Blueprint, jsonify, request

from app.data import SeriesSearchRequest
from app.utils import QueryMaker, Utils


def create_blueprint(context):
    api = Blueprint("api", __name__)
    @api.route("/hw")
    def hw():
        return jsonify("hii")


    @api.route("/series_search")
    def series_search():
        series = SeriesSearchRequest(series_name = request.args.get("search_box"), season_nm = request.args.get(
            "sess_nm"), episode_nm = request.args.get("epi_nm"))
        queries = QueryMaker.series_querymaker(series)
        results = context.search_handler.search(queries)
        Utils.make_inline_links(results, context)
        output = [x.json() for x in results]
        return jsonify(output)

    return api