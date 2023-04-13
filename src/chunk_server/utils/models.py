import time

class ChunkMetaInfo:
    def __init__(self, chunkHandle, checksum):
        self.chunkHandle = chunkHandle
        self.checksum = checksum
        self.isPrimary = False
        self.leaseTimestamp = None

    def getLeaseSpanDuration(self) -> float:
        if self.isPrimary:
            return time.time()
        return 0
    
    def getChunkInfo(self) -> dict:
        return {
            "checksum" : self.checksum,
            "chunkHandle" : self.chunkHandle,
            "isPrimary" : self.isPrimary,
            "lease" : self.getLeaseSpanDuration(),
        }
    
    def __str__(self) -> str:
        return self.getChunkInfo()