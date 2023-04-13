import threading
import time
from .constants import IP, PORT, CHUNK_SERVER_ID, CHUNK_SERVER_LOCATION_ID, HTTP_OK_STATUS_CODE
from utils.api_request import post
from config import chunk_server

from models.Chunk_Server import Chunk_Server
from utils.checksum import generate_checksum, validate_checksum


'''
{
    "chunkServerId" : " ",
    "isAlive" : true,

    "diskAvail" : 10,
    "chunkInfo" : [
        {
            "checksum" : "",
            "chunkHandle" : "",
            "isPrimary" : true/false,
            "lease" : 20,

        },
        ...,
        {
        
        }
    ]
}

'''

'''
{
    "chunkServerId" : " ",
    "ipAdress" : " ",
    "port" : 2345,
    "chunkLocationId": 12,
    "diskAvail" : 10,

}
'''

class Heartbeat(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def collectInfo(self):
        pass

    def sendInfo(self, data):
        resp = post('', data)

    def flow(self):
        pass

    def run(self):
        while True:
            time.sleep(20)
            self.flow()


class StartServer:
    def __init__(self):
        pass

    def init_chunk_server(self):
        resp = post('', chunk_server.getInitInfo())
        if resp.status_code == HTTP_OK_STATUS_CODE:
            return True
        return False

    def startup(self):

        if not self.init_chunk_server():
            print('chunk server start failure')
            return False

        Heartbeat().start()
        return True
