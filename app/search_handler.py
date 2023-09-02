import concurrent
from typing import List
from .utils import Utils
from .data import GdSearchResponse


class SearchHandler:

    def __init__(self, gd) -> None:
        self.gd = gd

    def search(self, query: List[str]) -> List[GdSearchResponse]:
        # TODO: add sanitization
        sanitized_queries = query
        # for i in query:
            # sanitized_queries.append(Utils.sanitize(i))
        output_list = []
        print("Generated queries ", sanitized_queries)
        for q in sanitized_queries:
            print("executing  : ", q)
            result = self.gd.search(q)
            print("Found resutls : ", len(result))
            output_list += result
        # with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        #     future_to_q = {executor.submit(self.gd.search , q): q for q in query}
        #     for q in concurrent.futures.as_completed(future_to_q):
        #         item = future_to_q[q]
        #         try:
        #             output_list += q.result()
        #         except Exception as exc:
        #             pass
        # sorting uniq items
        uniq_list = Utils.uniq_from_list(output_list)
        print(f"Uniq = {len(output_list)} >> {len(uniq_list)}")
        return list(map(lambda item: GdSearchResponse(**item), uniq_list))