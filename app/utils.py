from urllib.parse import quote
import requests
import logging


def send_msg(msg, BOT_TOKEN, GROUP_CHAT_ID):
    # The message you want to send to the group
    MESSAGE = msg

    # URL for the Telegram Bot API's sendMessage method
    URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    # Parameters for the sendMessage method
    params = {"chat_id": GROUP_CHAT_ID, "text": MESSAGE}

    # Send the message to the group chat using the requests library
    response = requests.post(URL, data=params)

    # Check if the request was successful (HTTP status code 200)
    if response.status_code == 200:
        logging.info("Message sent successfully!")
    else:
        logging.info(f"Error sending message: {response.text}")

class RandomMethods:

    @classmethod
    def uniq_from_list(self, input_list):
        uniq_list = []
        temp_id_db = set()
        for file in input_list:
                if not file['id'] in temp_id_db:
                    temp_id_db.add(file['id'])
                    uniq_list.append(file)
        return uniq_list


class QueryMaker:

    file_type = {"video": "mimeType contains 'video/'"}

    @classmethod
    def make_query(self, processor, args: dict):
        queries = {"q": []}
        for temp in processor(args):
            queries["q"].append(temp)
        return queries

    @classmethod
    def movie_querymaker(self, query: dict, sep=[" ", ".", ""]):
        queries = []
        release_year = query['release_year']
        name = query['name']
        if release_year == None:
            release_year = ""
        for s in sep:
            temp = f"{name}{s}{release_year}"
            if s == " " and len(release_year) == 0:
                continue
            if s == "":
                temp = name
            queries.append(
                f"name contains '{temp}' and {self.file_type['video']}")
        queries.append(
            f"name contains '{'.'.join(name.split())}' and {self.file_type['video']}")
        print(queries)
        return queries

    @classmethod
    def series_querymaker(self, query: dict, sep="."):
        name, season, epi = query
        alternate_q = [f"name contains '{ sep.join(name.split()) }{sep}s{season}e{epi}'",
                       f"name contains '{ sep.join(name.split()) }{sep}s{season}ep{epi}'",
                       f"name contains '{ sep.join(name.split()) }{sep}s{season}{sep}e{epi}'",
                       f"name contains '{ sep.join(name.split()) }{sep}s{season}{sep}ep{epi}'",
                       f"name contains '{name} s{season}e{epi}'",
                       f"name contains '{name} s{season} e{epi}'",
                       f"name contains '{name} s{season} ep{epi}'",
                       f"name contains '{name} s{season}ep{epi}'",
                       f"name contains '{name} s{season}'",
                       f"name contains '{name} season {season}'",
                       f"name contains '{name}'"]
        for ind, val in enumerate(alternate_q):
            alternate_q[ind] = val + " and "+self.file_type["video"]
        return alternate_q

    @classmethod
    def files_querymaker(self, query):
        name, type = query
        return [f"name contains '{name}'"]


class LinkMaker:

    def __init__(self, cf_worker, **kwargs) -> None:
        self.options = kwargs
        self.cf_worker = cf_worker

    def make_links(self, file: dict, **kwargs):
        if kwargs:
            options = kwargs
        else:
            options = self.options
        if options.get("td_override", False):
            file["td_override"] = f"https://hw77.gokuhw77.workers.dev/{file['td_override']}:/Foogle/{ quote(file['name']) }"
        if options.get("stream_link", False):
            file["stream_link"] = f"{ self.cf_worker }/stream_file/{ file['id'] }/{ quote(file['name'].replace(' ', '_')) }"
        if options.get("process_link", False):
            file["process_link"] = f"/process_file/{ file['id'] }"
        if options.get("cf_download_link", False):
            file["cf_download_link"] = f"{self.cf_worker}/getfile/{file['id']}"
        if options.get("gdrive_link", False):
            file["gdrive_link"] = file["webContentLink"]
        return file


if __name__ == "__main__":
    print("this function ")
    q = QueryMaker.make_query(QueryMaker.movie_querymaker, {
                              "name": "wanted", "release_year": "2009"})
    print(q)
