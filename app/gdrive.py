from googleapiclient import errors
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import math 

TEMP_FOLDER = "1rq0YjXG8hfZHmFcixBktEoVj2JeXlp7w" 
SCOPES = ['https://www.googleapis.com/auth/drive']

class FileCopyFailed(Exception):
    pass

class FileAccessFailed(Exception):
    pass

class PermissionChangeFailed(Exception):
    pass

class SearchFailed(Exception):
    pass

class GDriveHelper:
    def __init__(self):
        creds = None
        if os.path.exists('app/token.json'):
            creds = Credentials.from_authorized_user_file('app/token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'app/credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('app/token.json', 'w') as token:
                token.write(creds.to_json())
        self.drive_service = build('drive', 'v3', credentials=creds)


    def convert_size(size_bytes):
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2) 
        return "%s %s" % (s, size_name[i])


    def copy_file(self, source, destination = TEMP_FOLDER):
        origin_file_id = source 
        folder_id = destination 
        copied_file = {'title': 'copy_title.mkv', 'parents':[folder_id]}
        try:
            return self.drive_service.files().copy(
                fileId=origin_file_id, body=copied_file,supportsAllDrives = True).execute()
        except errors.HttpError as error:
            raise FileCopyFailed(f"Copying file failed to {destination}. Got back {error.error_details}")


    def has_parent(self, file_id, parent=TEMP_FOLDER):
        try:
            res = self.drive_service.files().get(fileId=file_id, fields='parents',supportsAllDrives='true').execute()
            files_parent = res.get('parents', None)
            if files_parent != None and parent in files_parent :
                return True
            else:
                return False
        except errors.HttpError as e:
            raise FileAccessFailed(f"Can't access file {file_id}, got {e.error_details}")


    def prepare_file(self, src_file_id):
        if self.has_parent(src_file_id):
            print("not copying")
            return src_file_id
        else:
            print("Copying file")
            r = self.copy_file(src_file_id)
            print("copy complete")
            dst_file_id = r.get("id", None)
            print(dst_file_id)
            # if dst_file_id != None:
                # self.change_permission(dst_file_id)
        print("return id")
        return dst_file_id


    def change_permission(self, file_id, user_permission = None):
        if user_permission == None:
            user_permission = {
             'type': 'anyone',
             'role': 'reader'
            }
        try:
            self.drive_service.permissions().create(fileId=file_id,body=user_permission,fields='id',supportsAllDrives = "true").execute()
        except errors.HttpError as e:
            raise PermissionChangeFailed(f"Failed to change permission of {file_id}, got {e.error_details}")

    
    def get_file_info(self, src_file_id, param='id, name, webContentLink, size'):
        try:
            res = self.drive_service.files().get(fileId=src_file_id, fields=param,supportsAllDrives='true').execute()
            res['size'] = GDriveHelper.convert_size(int(res['size']))
            return res
        except errors.HttpError as e:
            raise FileAccessFailed(f"Cant get info of {src_file_id}, got {e.error_details}")

    
    def search(self, search_q, onePageLimit=25):
        page_token = None
        # f"{search_q} and  mimeType contains 'video/'"
        # print(search_q)
        try:
            response = self.drive_service.files().list(q=search_q,
                                                    pageSize=onePageLimit,
                                                    spaces='drive',
                                                    fields='nextPageToken, files(id, name, modifiedTime, size)',
                                                    pageToken=page_token,
                                                    corpora = "allDrives",
                                                    includeItemsFromAllDrives = "true",
                                                    supportsAllDrives = "true").execute()
            list_of_files = response.get('files', [])
            san_list = [] 
            if len(list_of_files) != 0:
                for i in list_of_files:
                    if i.get('size', None) != None:
                        i['size'] = GDriveHelper.convert_size(int(i['size']))
                        san_list.append(i)
            return san_list
        except errors.HttpError as e:
            raise SearchFailed(f"Search failed for {search_q}, got {e.error_details}")

if __name__=="__main__":
    gd = GDriveHelper()