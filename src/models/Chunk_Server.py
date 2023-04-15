# import requests
from threading import Thread
import time

# local imports
# from utils.gen import generate_uuid


class Chunk_Server:
    def __init__(self, ip, port, loc_id, diskAvail, id=None):
        self.id = id
        # if id == None:
        #     self.id = generate_uuid()
        self.ip = ip
        self.port = port
        self.isAlive = True
        self.masters = ["localhost:5000"]
        self.last_ping = time.time()
        self.location_id = loc_id
        self.totalDisk = diskAvail
        self.diskAvail = diskAvail
        # self.availableChunks = []

    def getInitInfo(self):
        return {
            "chunkServerId" : self.id,
            "ipAdress" : self.ip,
            "port" : self.port,
            "chunkLocationId": self.location_id,
            "diskAvail" : self.diskAvail,
        }
    
    def getPingInfo(self):
        return {
            "chunkServerId" : self.id,
            "isAlive" : self.isAlive,
            "diskAvail" : self.diskAvail,
            "timestamp" : time.time(),
            # "chunkInfo" : self.availableChunks
        }


    # def start(self):
    #     for master in self.masters:
    #         url = "http://{}/initiate".format(master)
    #         payload = {"id": self.id, "ip": self.ip, "port": self.port}
    #         try:
    #             response = requests.post(url, json=payload)
    #             if response.status_code == 200:
    #                 self.ping_master()
    #                 print(response.json())
    #                 break
    #         except Exception as e:
    #             print("Error: {}".format(str(e)))

    # def ping_master(self):
    #     ping_route = "/ping"

    #     def ping():
    #         while self.isAlive:
    #             for master in self.masters:
    #                 url = "http://{}{}".format(master, ping_route)
    #                 payload = {"id": self.id, "timestamp": time.time()}
    #                 try:
    #                     response = requests.post(url, json=payload)
    #                     if response.status_code == 200:
    #                         # print(response.json())
    #                         break
    #                 except Exception as e:
    #                     print("Error: {}".format(str(e)))
    #             time.sleep(15)
                
    #     Thread(target=ping).start()

    def shutdown(self):
        self.isAlive = False

    def alive(self):
        return self.isAlive

    def update_ts(self, timestamp):
        self.last_ping = timestamp

    def __dict__(self):
        return {"id": self.id, "ip": self.ip, "port": self.port, "isAlive": self.isAlive, "last_ping": self.last_ping}


