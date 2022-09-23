from .utils import QueryMaker, RandomMethods
import json
class SearchHandler:

    def __init__(self, gd) -> None:
        self.gd = gd


    def sanitize(q: str):
        if q is None:
            return q
        q = q.replace("'", "\\'")
        return q


    def search(self, query: dict, processor, blocklist):
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

        # removing blocked files

        removed_blocked_list = [] 
        print(blocklist["folders"])
        print("0AItocrgdCTcFUk9PVA" in blocklist["folders"])
        for item in uniq_list:
            print("Checking for ")
            print(json.dumps(item))
            if item["id"] in blocklist["files"] :
                print("blocked file ID detected ", item)
            elif any(x in blocklist["folders"] for x in item["parents"]):
                print(f"Bad parent folder detected for {item} | Parent: {item['parents']}")
            else:
                removed_blocked_list.append(item)
        print(f"after removing blocked items {len(uniq_list)} >> {len(removed_blocked_list)}")
        return removed_blocked_list




