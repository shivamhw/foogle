from .utils import QueryMaker, RandomMethods

class SearchHandler:

    def __init__(self, gd) -> None:
        self.gd = gd


    def sanitize(q: str):
        if q is None:
            return q
        q = q.replace("'", "\\'")
        return q


    def search(self, query: dict, processor):
        # sanitize input
        for key, val in query.items():
            if val != None:
                query[key] = SearchHandler.sanitize(val)
        # making quiries 
        queries = QueryMaker.make_query(processor, query)
        print(queries)
        # executing search on query 
        output_list = []
        for query in queries["q"]:
            print("executing  : ", query)
            result = self.gd.search(query)
            print("Found resutls : ", len(result))
            output_list += result
        # sorting uniq items 
        uniq_list = RandomMethods.uniq_from_list(output_list)
        print(f"Uniq = {len(output_list)} >> {len(uniq_list)}")

        return uniq_list




