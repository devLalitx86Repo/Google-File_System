from driver import app
from chunk_server.util.constants import IP, PORT

if __name__ == '__main__':
    app.run(host=IP, port=PORT, debug=True)