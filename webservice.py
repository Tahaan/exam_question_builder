from config import Config
from questionaire import create_app
# from tools import DEFAULT_CONFIG_FILE, ConfigManager

DEFAULT_PORT = 5000

# c = ConfigManager(DEFAULT_CONFIG_FILE)
c = Config

app = create_app(c)

if __name__ == "__main__":
    app.run(debug=c.DEBUG, port=c.HTTP_PORT)
