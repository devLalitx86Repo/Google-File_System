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


    def addChunk(self, chunkObj):
        fileName = chunkObj.fileName
        if(fileName not in self.fileToChunks):
            self.fileToChunks[fileName] = []
        self.fileToChunks[fileName].append(chunkObj)
        self.chunkHandleToObj[chunkObj.handle] = chunkObj


    def getChunk(self, fileName, chunkIndex):
        chunkList = self.fileToChunks[fileName]
        return chunkList[chunkIndex]
    
    
    #Methods for Chunk Servers    
    def addChunkServer(self, chunk_server):
       self.chunk_servers[chunk_server.id] = chunk_server

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
    
    # def DecidePrimaryServer(self, chunkServerIDs):
    #     # Decide which chunk server to be primary
    #     # Return the chunk server ID
    #     spaceAvailable = 0
    #     primaryID = 0
    #     for id in chunkServerIDs:
    #         id = str(id)
    #         if id in self.isServerAlive and self.isServerAlive[id]:
    #             if id in self.ServerCapacity and self.ServerCapacity[id] > spaceAvailable:
    #                 spaceAvailable = self.ServerCapacity[id]
    #                 primaryID = id
    #     return primaryID
                

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


    # # Methods for Operations

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

            