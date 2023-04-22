import time
from utils.constants import LEASE_TIME

#local imports
from .Chunk import Chunk
from .Chunk_Server import Chunk_Server
from utils.gen import generate_uuid

class MasterServer:
    def __init__(self):
        self.name = "MasterServer"
        self.ip = ""
        self.port = 0
        self.chunkHandle = {} # key: Chunk Handle, value: ChunkServer ID list
        self.chunk_servers = {} # key: ChunkServer ID, value: ChunkServer Object
        self.isServerAlive = {} # key: ChunkServer ID, value: True/False
        self.ServerCapacity = {} # key: ChunkServer ID, value: Capacity i.e. available space
        self.fileToChunks = {} # key: File Name, value: List of Chunk Objects Corresponding to file
        self.chunkHandleToObj = {} # key: Chunk Handle, value: ChunkObject
        self.chunkHandleToPrimary = {} # key: Chunk Handle, value: [Primary ChunkServer ID, Start Time]

    
    def chunk_avail(self,file_name,index):
        if file_name in self.fileToChunks and len(self.fileToChunks[file_name]) > index:
            return True
        return False
            

    def addChunk(self, file_name, index,checksum):        
        handle = generate_uuid()
        chunk = Chunk(file_name,checksum,index,handle)

        if file_name not in self.fileToChunks:
            self.fileToChunks[file_name] = []
        
        self.fileToChunks[file_name].append(chunk)
        self.chunkHandleToObj[handle] = chunk

        # chunkServers = self.getChunkServers()
        # chunkObj.chunk_server_ip = [server.ip for server in chunkServers]
        # chunkObj.chunk_server_port = [server.port for server in chunkServers]

        # self.chunkHandle[chunkObj.handle] = [server.id for server in chunkServers]
        # # Deciding Primary Server
        # self.chunkHandleToPrimary[chunkObj.handle] = [self.DecidePrimaryServer(chunkServers), time.time()+LEASE_TIME]
        # # Updating Replica Count
        # chunkObj.replica_count = len(chunkServers)
        # TODO: Update the Useful space in Chunk Object
        return True, chunk.__dict__()

    def getChunk(self, fileName, chunkIndex):
        chunkList = self.fileToChunks[fileName]
        return chunkList[chunkIndex]
    
    
    #Methods for Chunk Servers  

    def getChunkServers(self):
        chunkServerLis = []
        for chunkServer in self.chunk_servers.values():
            # TODO: Change this to select 3 most available chunk servers 
            if chunkServer.isAlive:
                chunkServerLis.append(chunkServer)
            if(len(chunkServerLis)==3):
                break   
        return chunkServerLis

    def addChunkServer(self, payload: dict):
        try:
            id = payload.get("chunkServerId")
            ip = payload.get("ipAdress")
            port = payload.get("port")
            loc = payload.get("chunkLocationId")
            diskAvail = payload.get("diskAvail")
            chunk_server = Chunk_Server(ip,port,id, diskAvail, loc)  

            self.chunk_servers[chunk_server.id] = chunk_server
            self.isServerAlive[chunk_server.id] = True
            self.ServerCapacity[chunk_server.id] = chunk_server.diskAvail
            return True, "OK"
        except Exception as e:
            raise e

    def getCSList(self):
        return list(server.__dict__() for server in self.chunk_servers.values())
    
    def update_ts(self, chunkServerID, timestamp):
        self.chunk_servers[chunkServerID].update_ts(timestamp)
    
    def update_diskAvail(self, chunkServerID, diskSize):
        self.chunk_servers[chunkServerID].update_diskAvail(diskSize)

    def removeChunkServer(self, chunk_server):
        # set chunk server to dead
        self.chunk_servers[chunk_server.id].isAlive = False
    
    
    def update_chunkInfo(self, chunkServerID, chunkInfo_lis):
        chunkServerObj = self.chunk_servers[chunkServerID]
        CS_ChunkList = []
        for chunkInfo in chunkInfo_lis:
            chunkHandle = chunkInfo["chunkHandle"]
            CS_ChunkList.append(chunkHandle)
        CS_ChunkList.sort()
        chunkServerObj.chunkList.sort()
        if(CS_ChunkList==chunkServerObj.chunkList):
            return "OK"
        else:
            return "ERROR"
            


    # def findChunkHandle(self,fileName, offset):
    #     ChunkLis = self.fileToChunks[fileName]
    #     for chunk_obj in ChunkLis:
    #         if offset < chunk_obj.usefulSpace:
    #             return chunk_obj.handle
    #         offset -= chunk_obj.usefulSpace
    #     return -1
    
    def DecidePrimaryServer(self, chunkServerLis):
        chunkServerIDs = [server.id for server in chunkServerLis]
        spaceAvailable = -1
        primaryID = -1
        for id in chunkServerIDs:
            id = str(id)
            if id in self.isServerAlive and self.isServerAlive[id]:
                if id in self.ServerCapacity and self.ServerCapacity[id] > spaceAvailable:
                    spaceAvailable = self.ServerCapacity[id]
                    primaryID = id
            
        return primaryID
                

    # def getChunkServerID(self, chunkHandle):
    #     return self.chunkHandle[chunkHandle]

    # def getChunkServerAdd(self, chunkServerID):
    #     address = self.chunkServer[chunkServerID]
    #     ip, port = address.split(":")
    #     return ip, port
    
    # def getMetadata(self, chunkHandle):
    #     chunkServerIDs = self.getChunkServerID(chunkHandle)
    #     primaryID = self.DecidePrimaryServer(chunkServerIDs)
    #     ChunkServerList = []
    #     for id in chunkServerIDs:
    #         id = str(id)
    #         if (id in self.isServerAlive) and self.isServerAlive[id]:
    #             ip, port = self.getChunkServerAdd(id)
    #             if id == primaryID:
    #                 chunk = ChunkServer(chunkHandle, id, ip, port, True)
    #             else:
    #                 chunk = ChunkServer(chunkHandle, id, ip, port)
    #             ChunkServerList.append(chunk)
            
    #     return ChunkServerList
    
    # def printInfo(self):
    #     print("Chunk Handle: ", self.chunkHandle)
    #     print("Chunk Server: ", self.chunkServer)
    #     print("Is Server Alive: ", self.isServerAlive)
    #     print("Added Chunks = ", self.fileToChunks)


    # # Methods for Chunk

    def getPrimaryServer(self, chunkHandle):
        requestTime = time.time()
        if(chunkHandle not in self.chunkHandleToPrimary):
            return -1
        time_gap = requestTime - self.chunkHandleToPrimary[chunkHandle][1]
        if(time_gap > LEASE_TIME):
            chunkServers = self.getChunkServers()
            self.chunkHandleToPrimary[chunkHandle] = [self.DecidePrimaryServer(chunkServers), time.time()+LEASE_TIME]
        
        return self.chunkHandleToPrimary[chunkHandle][0], self.chunkHandleToPrimary[chunkHandle][1]



    # Method for Operations 


    # def write(self, chunkHandle, byteStart, byteEnd, chunkServerInfo):

    #     for chunkServer in chunkServerInfo:
    #         chunkServerId = chunkServer["chunkServerId"]
    #         if chunkServerId not in self.chunkHandle[chunkHandle]:
    #             self.chunkHandle[chunkHandle].append(chunkServerId)
    #         chunkServerObj = self.chunk_servers[chunkServerId]
    #         chunkServerObj.write_update(chunkHandle) # This will update the chunk list of the chunk server
    #         # To update the start Byte and End Byte of the chunk
    #         fileName = self.ChunkToFile[chunkHandle]
    #         chunkObj = 

            