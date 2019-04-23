from questionaire import app
from tools import DEFAULT_CONFIG_FILE, ConfigManager

DEFAULT_PORT = 5000

c = ConfigManager(DEFAULT_CONFIG_FILE)

if __name__ == "__main__":
    app.run(debug=c.get('debug', False), port=c.get('http_port', DEFAULT_PORT))
