from __future__ import print_function
import os.path
from flask import Flask, request, redirect
from re import search
from flask.helpers import url_for
from flask.templating import render_template
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import math
import base64
import urllib.parse
import requests

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']
app = Flask(__name__)
drive_service = None
# BASE_URL = "https://api.shivamhw.codes/2:video/"
BASE_URL = "https://api.shivamhw.codes/"
TEMP_FOLDER = "1rq0YjXG8hfZHmFcixBktEoVj2JeXlp7w"   
DRIVE_ID = "2"

def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])

def copy_file(source, destination):
    global drive_service
    origin_file_id = source # "1A69l_H_wPhrIYyG5DujGuJfMHzTyGYqx"
    folder_id = destination #folder.get('id')
    copied_file = {'title': 'copy_title.mkv', 'parents':[folder_id]}
    try:
        return drive_service.files().copy(
            fileId=origin_file_id, body=copied_file,supportsAllDrives = True).execute()
    except Exception as error:
        print(error)
    return None

def callback(request_id, response, exception):
        if exception:
            # Handle error
            print(exception)
        else:
            print("Permission Id: %s" % response.get('id'))


def change_permission(file_id):
    global drive_service
    batch = drive_service.new_batch_http_request(callback=callback)
    user_permission = {
        'type': 'anyone',
        'role': 'reader'
    }
    batch.add(drive_service.permissions().create(
            fileId=file_id,
            body=user_permission,
            fields='id',
            supportsAllDrives = "true"
    ))
    batch.execute()

def initialize():
    global drive_service
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    drive_service = build('drive', 'v3', credentials=creds)

def get_file(src_file_id):
    global drive_service, TEMP_FOLDER
    print("file to copy ", src_file_id)
    res = drive_service.files().get(fileId=src_file_id, fields='parents',supportsAllDrives='true').execute()
    parent = res.get('parents', None)
    if(parent[0] == TEMP_FOLDER):
        dst_file_id = src_file_id
        print("file already exist not copying")
    else:
        r = copy_file(src_file_id, TEMP_FOLDER)
        dst_file_id = r.get("id")
        change_permission(dst_file_id)
    file_info = drive_service.files().get(fileId=dst_file_id, fields='id, name, webContentLink', supportsAllDrives = 'true').execute()
    raw_name = file_info.get('name')
    return file_info.get("webContentLink"), raw_name


def get_file_id(src_file_id):
    global drive_service, TEMP_FOLDER
    print("file to copy ", src_file_id)
    res = drive_service.files().get(fileId=src_file_id, fields='parents',supportsAllDrives='true').execute()
    parent = res.get('parents', None)
    if(parent[0] == TEMP_FOLDER):
        dst_file_id = src_file_id
        print("file already exist not copying")
    else:
        r = copy_file(src_file_id, TEMP_FOLDER)
        dst_file_id = r.get("id")
        change_permission(dst_file_id)
    return dst_file_id

def get_file_info(src_file_id):
    res = drive_service.files().get(fileId=src_file_id, fields='id, name, webContentLink, size',supportsAllDrives='true').execute()
    return res

def search(search_q, onePageLimit=25):
    global drive_service
    page_token = None
    file_id = None
    response = drive_service.files().list(q=f"{search_q} and  mimeType contains 'video/'",
                                            pageSize=onePageLimit,
                                            spaces='drive',
                                            fields='nextPageToken, files(id, name, modifiedTime, size)',
                                            pageToken=page_token,
                                            corpora = "allDrives",
                                            includeItemsFromAllDrives = "true",
                                            supportsAllDrives = "true").execute()
    list_of_files = response.get('files', [])
    print(list_of_files)
    san_list = [] 
    if len(list_of_files) != 0:
        for i in list_of_files:
            if i.get('size', None) != None:
                i['size'] = convert_size(int(i['size']))
                san_list.append(i)
    return san_list


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/series_search")
def s_search():
    name = request.args.get("name")
    season = request.args.get("sess_nm")
    epi = request.args.get("epi_nm")
    alternate_q = [f"name contains '{name} s{season}e{epi}' or name contains '{name} s{season} e{epi}'", \
        f"name contains '{name} s{season} ep{epi}' or name contains '{name} s{season}ep{epi}'", \
        f"name contains '{name} s{season}.e{epi}' or name contains '{name} s{season}.ep{epi}'", \
            f"name contains '{name}'"]
    list_file = []
    for q in alternate_q:
        print("inuse q : ", q)
        list_file = search(q)
        if len(list_file) !=0 :
            break
    if len(list_file) == 0:
        return "found nothing"
    return render_template('result.html', my_list=list_file)

@app.route("/series.html")
def se_se():
    return render_template("series.html")

@app.route("/links")
def links():
    file_id = request.args.get("file_id")
    link_dict = {}
    file_info = get_file_info(file_id)
    link_dict['size'] = convert_size(int(file_info['size']))
    link_dict['g_link'], link_dict['raw_name'], link_dict['id']= file_info['webContentLink'], file_info["name"], file_info['id']
    b64_name = f"/{DRIVE_ID}:/{link_dict['raw_name']}".encode("ascii")
    b64_name = base64.b64encode(b64_name)
    b64_name = b64_name.decode("ascii")
    url_name = urllib.parse.quote(link_dict['raw_name'])
    link_dict['web_player'] =  f"{BASE_URL}{DRIVE_ID}:video/{b64_name}" #  BASE_URL + name
    link_dict['direct_link'] = f"{BASE_URL}{DRIVE_ID}:/{url_name}" # "https://api.shivamhw.codes/"+base64.b64decode(name).decode('ascii')[1:]
    link_dict['vlc_link'] = f"vlc://{BASE_URL}{DRIVE_ID}:/{url_name}"  # "vlc://"+"https://api.shivamhw.codes/2:/"+urllib.parse.quote(link_dict['link_dict['raw_name']'])
    if requests.head(link_dict['g_link']).status_code != 200:
        return "broken link!! Try other links"
    return render_template("links.html", link_dict=link_dict)


@app.route("/process_file/<file_id>")
def process_f(file_id):
    try:
        dst_file_id = get_file_id(file_id)
    except Exception as e:
        print(e)
        return "error and no error is handled at backend. Try another link or call me"+str(e)
    return redirect(url_for('links', file_id=dst_file_id))

@app.route("/search")
def search_handler():
    query = request.args.get("search_box")
    dotted_query = ".".join(query.split())
    query = f"name contains '{query}'" #or name contains '{dotted_query}'"
    print(query)
    list_file = search(query)
    if len(list_file) == 0:
        return "nothing found"
    return render_template('result.html', my_list=list_file)

if __name__ == '__main__':
    initialize()
    app.run(host='0.0.0.0', port=80)
    # app.run()
