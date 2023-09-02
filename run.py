from app.main import create_app
import configparser
from app.data import Config
config = configparser.ConfigParser()
config.read('config.ini')
cfg = Config(**config['foogle'])

if __name__ == "__main__":
    create_app(cfg).run(host="127.0.0.1", port="5500", debug=True)
else:
    gunicorn = create_app(cfg)
