from flask import Blueprint, jsonify, request
from app.utils import QueryMaker
from app.utils import LinkMaker

def create_blueprint(gd, cf_worker):
    api = Blueprint("api", __name__)
    @api.route("/hw")
    def hw():
        return jsonify("hii")


    @api.route("/series_search")
    def series_search():
        search_data = [None] * 3
        search_data[0], search_data[1], search_data[2] = request.args.get("search_box"), request.args.get("sess_nm"), request.args.get("epi_nm")
        list_file = []
        link_m = LinkMaker(cf_worker=cf_worker, stream_link=True, process_link=True)
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
            return jsonify({"error":"found nothing"})
        for i in list_file:
            i = link_m.make_links(i)
        return jsonify(list_file)

    return api