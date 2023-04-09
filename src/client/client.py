import sys
import time
import json
import requests

MASTER_URL = ""

class File:
    def __init__(self, file_name) -> None:
        self.chunks = dict()
        self.file_name = file_name
        self.size = 0
    
    def request_md(self, chunk_idx):
        chunk = self.chunks[chunk_idx] # key error
        if chunk.exp_time > time.time():
            # request Master: (file_name, chunk_idx) --> chunk_md
            parameters = {"file_name":file_name, "chunk_idx":chunk_idx}
            response = requests.get(MASTER_URL, params=parameters)
            chunk_md = json.load(response.json)
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
            parameters = {"chunk_handle":self.handle,"byte_range":byte_range}
            response = requests.get(chunk_server.id, params=parameters)
            return json.load(response)
        return None
    
if __name__ == "__main__":
    files = dict()

    while True:
        cmd = input().split()
        if cmd[0] == "read": # read file_name chunk_idx
            file_name = cmd[1]
            chunk_idx = cmd[2]

            if file_name not in files:
                new_file = File(file_name)
                files[file_name] = new_file
            response = files[file_name].read_chunk(chunk_idx)
            if response.status == "OK":
                print(response.data)
            else:
                print("Error reading chunk:", response.error)
        elif cmd[0] == "write": # write file_name chunk_idx local_file_path
            pass
        elif cmd[0] == "append": # append file_name local_file_path
            pass
        # elif cmd[0] == "create":
        elif cmd[0] == "delete":
            pass
        
            