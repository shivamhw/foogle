# Foogle
File search that creates direct download and streaming links from google drive and teamdrives.
# Current Features
1. Main page supports video search
2. Series page supports collection like series, seasons 

# Installation

1. git clone the repo using 
```
git clone -b dev https://github.com/shivamhw/foogle.git 
```
2. edit following in config .ini file
```
CRED_JSON_PATH = #Path to credentials.json
TOKEN_JSON_PATH = #Path to token.json
```
3. run this in foogle dir
```
pip install -r requirements.txt
```
4. finally run this
```
python run.py
```
Check it out on [Foogle](https://www.shivamhw.codes/)
