from questionaire import app
from tools import DEFAULT_CONFIG_FILE, Config

DEFAULT_PORT = 5000

c = Config(DEFAULT_CONFIG_FILE)

if __name__ == "__main__":
    app.run(debug=c.get('debug', False), port=c.get('http_port', DEFAULT_PORT))
