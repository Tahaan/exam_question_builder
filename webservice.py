from config import Config
from questionaire import create_app
from tools import DEFAULT_CONFIG_FILE, ConfigManager

DEFAULT_PORT = 5000

c = ConfigManager(DEFAULT_CONFIG_FILE)

app = create_app(Config)

if __name__ == "__main__":
    app.run(debug=c.get('debug', False), port=c.get('http_port', DEFAULT_PORT))
