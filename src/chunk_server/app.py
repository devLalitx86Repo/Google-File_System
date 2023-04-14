from driver import app
from chunk_server.util.constants import IP, PORT
from util.general import update_chunks_list

if __name__ == '__main__':
    update_chunks_list()
    app.run(host=IP, port=PORT, debug=True, threaded=True)