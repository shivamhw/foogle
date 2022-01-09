from typing import List


class QueryMaker:

    file_type = {"video": "mimeType contains 'video/'"}

    def sanitize(q: str):
        q = q.replace("'", "\\'")
        return q

    @classmethod
    def make_query(self, processor, args: List, type="video", size=None):
        for i, val in enumerate(args):
            args[i] = self.sanitize(val)
        queries = {"q": []}
        for temp in processor(args):
            queries["q"].append(temp)
        if size != None:
            queries["size"] = size
        return queries

    @classmethod
    def movie_querymaker(self, query: List):
        queries = []
        for i in query:
            dotted_query = ".".join(i.split())
            queries.append(
                f"name contains '{i}' and {self.file_type['video']}")
            queries.append(
                f"name contains '{dotted_query}' and {self.file_type['video']}")
        return queries

    @classmethod
    def series_querymaker(self, query: List):
        name, season, epi = query
        alternate_q = [f"name contains '{name} s{season}e{epi}' or name contains '{name} s{season} e{epi}'",
                       f"name contains '{name} s{season} ep{epi}' or name contains '{name} s{season}ep{epi}'",
                       f"name contains '{name} s{season}.e{epi}' or name contains '{name} s{season}.ep{epi}'",
                       f"name contains '{name}'"]
        for ind, val in enumerate(alternate_q):
            alternate_q[ind] = val + " and "+self.file_type["video"]
        return alternate_q
