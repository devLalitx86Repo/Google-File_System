from driver import app
from chunk_server.util.constants import IP, PORT
from util.yen import StartServer

if __name__ == '__main__':
    # if StartServer().up():
    #     print('Successful Start')
    #     app.run(host=IP, port=PORT, debug=False, threaded=True)
    # else:
    #     print('unable to start')
    app.run(host=IP, port=PORT, debug=False, threaded=True)