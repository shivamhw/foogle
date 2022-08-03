from .utils import QueryMaker


class SearchHandler:

    def __init__(self, gd) -> None:
        self.gd = gd

    def sanitize(q: str):
        if q is None:
            return q
        q = q.replace("'", "\\'")
        return q

    def search(self, query: dict, processor):
        for key, val in query.items():
            if val != None:
                query[key] = SearchHandler.sanitize(val)
        queries = QueryMaker.make_query(processor, query)
        print(queries)
        output_list = []
        for query in queries["q"]:
            print("executing  : ", query)
            result = self.gd.search(query)
            print("Found resutls : ", len(result))
            print(result)
            output_list += result
        print("Before running uniq item ", len(output_list))
        uniq_list = []
        temp_id_db = set()
        for file in output_list:
            if not file['id'] in temp_id_db:
                temp_id_db.add(file['id'])
                uniq_list.append(file)
        print(uniq_list)
        print("Before afer uniq item ", len(uniq_list))
        return uniq_list

        


