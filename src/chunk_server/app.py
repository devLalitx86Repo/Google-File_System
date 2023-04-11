
from driver import app
from constants import IP, PORT

if __name__ == '__main__':
    app.run(host=IP, port=PORT, debug=True)