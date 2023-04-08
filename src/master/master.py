# Create a class that has information about all the chunks of the file
class FileDetails:
    def __init__(self, fileName, offset):
        self.fileName = fileName
        self.offset = offset
        self.chunkSizes = {} # key: Chunk Handle, value: Chunk Useful Size
        self.chunkCount = 0

    # def findChunkHandle(self, offset):
    #     # Find the chunk handle for the given offset
    #     # Return the chunk handle
    #     for chunkHandle in self.chunkSizes:
    #         if offset < self.chunkSizes[chunkHandle]:
    #             return chunkHandle
    #         offset -= self.chunkSizes[chunkHandle]
    #     return -1





# Create a class having information needed to be sent to client for a chunk
class ChunkServer:
    def __init__(self, chunkHandle, chunkServerID, chunkServerIP, chunkServerPort, isPrimary=False):
        self.chunkHandle = chunkHandle
        self.chunkServerID = chunkServerID
        self.chunkServerIP = chunkServerIP
        self.chunkServerPort = chunkServerPort
        self.isPrimary = isPrimary
    
    def printInfo(self):
        print("Chunk Handle: ", self.chunkHandle)
        print("Chunk Server ID: ", self.chunkServerID)
        print("Is Server Primary: ", self.isPrimary)

# Create a class for the master server of google file system

class MasterServer:
    def __init__(self):
        self.name = "MasterServer"
        self.ip = ""
        self.port = 0
        self.chunkHandle = {} # key: Chunk Handle, value: ChunkServer ID list
        self.chunkServer = {} # key: ChunkServer ID, value: ChunkServer IP:Port
        self.isServerAlive = {} # key: ChunkServer ID, value: True/False
        self.ServerCapacity = {} # key: ChunkServer ID, value: Capacity i.e. available space

    
    def DecidePrimaryServer(self, chunkServerIDs):
        # Decide which chunk server to be primary
        # Return the chunk server ID
        spaceAvailable = 0
        primaryID = 0
        for id in chunkServerIDs:
            id = str(id)
            if id in self.isServerAlive and self.isServerAlive[id]:
                if id in self.ServerCapacity and self.ServerCapacity[id] > spaceAvailable:
                    spaceAvailable = self.ServerCapacity[id]
                    primaryID = id
        return primaryID
                

    def getChunkServerID(self, chunkHandle):
        return self.chunkHandle[chunkHandle]

    def getChunkServerAdd(self, chunkServerID):
        address = self.chunkServer[chunkServerID]
        ip, port = address.split(":")
        return ip, port
    
    def getMetadata(self, chunkHandle):
        chunkServerIDs = self.getChunkServerID(chunkHandle)
        primaryID = self.DecidePrimaryServer(chunkServerIDs)
        ChunkServerList = []
        for id in chunkServerIDs:
            id = str(id)
            if (id in self.isServerAlive) and self.isServerAlive[id]:
                ip, port = self.getChunkServerAdd(id)
                if id == primaryID:
                    chunk = ChunkServer(chunkHandle, id, ip, port, True)
                else:
                    chunk = ChunkServer(chunkHandle, id, ip, port)
                ChunkServerList.append(chunk)
            
        return ChunkServerList
    
    def printInfo(self):
        print("Chunk Handle: ", self.chunkHandle)
        print("Chunk Server: ", self.chunkServer)
        print("Is Server Alive: ", self.isServerAlive)


def dummyEnteries(masterServer):
    masterServer.chunkHandle = {"1": [1, 2, 3], "2": [1, 2, 3], "3": [1, 2, 3], "4": [1, 2, 3], "5": [1, 2, 3]}
    masterServer.chunkServer = {"1":"1.1.1.2:5000"}
    masterServer.isServerAlive = {"1": True}
    masterServer.ServerCapacity = {"1": 100}



# Create an object of MasterServer class
masterServer = MasterServer()
dummyEnteries(masterServer)
ChunkServerlis = (masterServer.getMetadata("1"))

for CS in ChunkServerlis:
    CS.printInfo()