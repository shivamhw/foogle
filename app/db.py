from pymongo import MongoClient


class LinkDB:

    def __init__(self, mongouri):
        con = MongoClient(mongouri)
        self.db = con.foogle


    def get_file_blocklist(self):
        result = self.db.bad_files.find({})
        output = []
        for i in result:
            output.append(i['_id'])
        return output

    def get_folder_blocklist(self):
        result = self.db.bad_folders.find({})
        output = []
        for i in result:
            output.append(i['_id'])
        return output

    def add_file_blocklist(self, fileid):
        data = {"_id": fileid, "tries": 1}
        result = self.db.bad_files.find_one({"_id": fileid})
        if result == None:
            self.db.bad_files.insert_one(data)
        else:
            result['tries'] += 1
            self.db.bad_files.update_one(
                {"_id": fileid}, {"$set": {"tries": result['tries']}})

    def add_folder_blocklist(self, folderid, fileid):
        data = {"_id": folderid, "tries": 1, "files": [fileid]}
        result = self.db.bad_folders.find_one({"_id": folderid})
        if result == None:
            self.db.bad_folders.insert_one(data)
        else:
            if fileid not in result["files"]:
                result['tries'] += 1
                result['files'].append(fileid)
                self.db.bad_folders.update_one({"_id": folderid}, {
                                               "$set": {"tries": result["tries"], "files": result["files"]}})
            else:
                print(
                    f"already reported file : {fileid} for folder : {folderid}")

    def get_tries_count(self, id, isFolder=False):
        if isFolder:
            result = self.db.bad_folders.find_one({"_id": id})
        else:
            result = self.db.bad_files.find_one({"_id": id})
        if result == None:
            return 0
        else:
            return result["tries"]
