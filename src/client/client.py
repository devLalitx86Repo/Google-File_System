import sys
import time
import requests

class File:
    def __init__(self, file_name) -> None:
        self.chunks = dict()
        self.file_name = file_name
        self.size = 0
    
    def request_md(self, chunk_idx):
        chunk = self.chunks[chunk_idx] # key error
        if chunk.exp_time > time.time():
            # request Master: (file_name, chunk_idx) --> chunk_md
            chunk_md = None
            chunk = Chunk(chunk_md)
            self.chunks[chunk_idx] = chunk
        return chunk
    
    def read_chunk(self, chunk_idx):
        chunk = self.request_md(chunk_idx)
        return chunk.read()

class Chunk:
    def __init__(self, chunk_md) -> None:
        self.size = chunk_md["size"]
        self.handle = chunk_md["handle"]
        self.chunk_servers = chunk_md["chunk_servers"] # list
        self.primary_server = chunk_md["primary_server"]
        self.exp_time = chunk_md["exp_time"]
        # sort chunk_servers wrt client's location
    
    def read(self, byte_range):
        for chunk_server in self.chunk_servers:
            # request chunk_server: (chunk_handle, byte_range) --> (status, data, check_sum)
            response = None
            if response.status is "OK":
                return response.data # Bytes
        return None
    
if __name__ == "__main__":
    files = dict()
    file_name = "main.c"
    files[file_name] = File(file_name)
    files[file_name].request_md(0)