
import threading
import time

'''
{
    "chunkServerId" : " ",
    "isAlive" : true,
    "ipAdress" : " ",
    "port" : 2345,

    "diskAvail" : "",
    "chunkInfo" : [
        {
            "chunkHandle" : "",
            "isPrimary" : true/false,

        },
        ...,
        {
        
        }
    ]
}

'''

class Heartbeat(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def collectInfo(self):
        pass  

    def sendInfo(self):
        pass

    def run(self):
        pass


class StartServer:
    def __init__(self):
        pass
    
    def init_chunk_server(self):
        pass

    def startup(self):

        self.init_chunk_server()

        Heartbeat().start()

