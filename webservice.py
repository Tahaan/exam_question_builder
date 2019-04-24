from config import Config
from questionaire import create_app

DEFAULT_PORT = 5000

conf = Config
app = create_app(conf)

if __name__ == "__main__":
    app.run(debug=conf.DEBUG, port=conf.HTTP_PORT)
