from app.main import create_app
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
cfg = {}
cfg["CF_WORKER_SITE"] = config["foogle"]["CF_WORKER_SITE"]
cfg["CRED_JSON_PATH"] = config["foogle"]["CRED_JSON_PATH"]
cfg["TOKEN_JSON_PATH"] = config["foogle"]["TOKEN_JSON_PATH"]
cfg["TEMP_FOLDER"] = config["foogle"]["TEMP_FOLDER"]
cfg["MONGOURI"] = config["foogle"]["MONGOURI"]
if __name__ == "__main__":
    create_app(**cfg).run(host="0.0.0.0", port="5500",debug=True)
else:
    gunicorn = create_app(**cfg)
