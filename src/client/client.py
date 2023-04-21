from utils.api_request import post_dict, get_dict
from utils.gen import make_url
import requests
import time
import json
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MASTER_URL = ""
files = dict()

class File:
    def __init__(self, file_name) -> None:
        self.chunks = dict()
        self.file_name = file_name
        self.size = 0
        self.last_chunk_id = 0
    
    def request_md(self, chunk_idx):
        if chunk_idx not in self.chunks or chunk.exp_time < time.time():
            # request Master: (file_name, chunk_idx) --> chunk_md
            body = {"file_name":file_name, "chunk_idx":chunk_idx}
            response, status_code = post_dict(MASTER_URL + "/query_chunk", body)
            if status_code == 200:
                chunk_md = json.load(response.json)
                chunk = Chunk(chunk_md)
                self.chunks[chunk_idx] = chunk
                self.last_chunk_id = max(self.last_chunk_id, chunk_idx)
        else:
            chunk = self.chunks[chunk_idx] # key error
        return chunk
    
    def read_chunk(self, chunk_idx):
        chunk = self.request_md(chunk_idx)
        return chunk.read()
    
    def append_chunk(self, data):
        chunk = self.request_md(-1) # -1 denotes last chunk
        return chunk.append(data)
    
    def write_chunk(self, chunk_idx, byte_start, byte_end, data):
        chunk = self.request_md(chunk_idx)
        return chunk.write(data, byte_start, byte_end)

    def create_new_chunk(self):
        body = {"file_name":file_name, "chunk_idx":self.last_chunk_id + 1, "checksum":"000"}
        response = requests.post(MASTER_URL + "/query_chunk", json=body)
        if response.status_code == 200:
            print(response.json)
            
class Chunk:
    def __init__(self, chunk_md) -> None:
        self.md = chunk_md
        self.file_name = chunk_md["fileName"]
        self.chunk_idx = chunk_md["chunkIndex"] 
        self.handle = chunk_md["handle"]
        self.checksum = chunk_md["checksum"]
        self.replica_count = int(chunk_md["replica_count"])
        self.chunk_server_info = list() # dict
        self.exp_time = chunk_md["expiryTime"]
        self.primary_server = chunk_md["primaryServer"]
        # sort chunk_servers wrt client's location
        for chi in range(self.replica_count):
            chunk_server_i = {
                "chunkServerId":"xxx",
                "ipAddress":chunk_md["chunk_server_ip"][chi],
                "port":chunk_md["chunk_server_port"][chi]
            }
            self.chunk_servers.append(chunk_server_i)
    
    def read(self, byte_range):
        for chs_i in range(self.md["replica_count"]):
            # request chunk_server: (chunk_handle, byte_range) --> (status, data, check_sum)
            # parameters = {"chunk_handle":self.handle,"byte_range":byte_range}
            chunk_server_url = make_url(self.md["chunk_server_ip"][chs_i], self.md["chunk_server_port"][chs_i])
            body = {
                "chunkHandle" : self.md["handle"],
                "byteOffset " : byte_range[0],
                "totalBytes" : byte_range[1],
            }
            print("Read request sent to:", chunk_server_url)
            return post_dict(chunk_server_url + "/read/", body)
    
    def append(self, data):
        # request primary: (chunk_handle, data) --> (status)
        # parameters = {"chunk_handle":self.handle,"data":data}
        chunk_server_url = make_url(self.chunk_servers[self.primary_server]["ip"],self.chunk_servers[self.primary_server]["port"])
        body = {
            "clientIP" : "localhost",
            "clientPort" : 6969,
            "chunkHandle" : self.handle,
            "data" : data,
            "chunkServerInfo" : self.chunk_server_info
        }
        print("Append request sent to:", chunk_server_url)
        return post_dict(chunk_server_url + "/append/", body)
    
    def write(self, data, byteStart, byteEnd):
        chunk_server_url = make_url(self.chunk_servers[self.primary_server]["ip"],self.chunk_servers[self.primary_server]["port"])
        body = {
            "clientIP" : "localhost",
            "clientPort" : 6969,
            "chunkHandle" : self.handle,
            "byteStart" : byteStart,
            "byteEnd" : byteEnd,
            "data" : data,
            "chunkServerInfo" : self.chunk_server_info
        }
        print("Write request sent to:", chunk_server_url)
        return post_dict(chunk_server_url + "/write/", body)

def read_handler(file_name, chunk_idx):
    if file_name not in files:
        new_file = File(file_name)
        files[file_name] = new_file
    print("Read initiated")
    response, status_code = files[file_name].read_chunk(chunk_idx)
    if status_code == 200:
        print(response)
    else:
        print("Error reading chunk: \n", response)

def append_handler(file_name, file_path):
    with open(file_path, "rb") as f:
        file_data = f.read()
    if file_name not in files:
        new_file = File(file_name)
        files[file_name] = new_file
    print("Append initiated")
    for attepmts in range(3):
        print("Attempt#: ", attepmts)
        response, status_code = files[file_name].append_chunk(file_data)
        if status_code == 200:
            print(response)
            return
        else:
            print("Error appending data: \n", response)
            files[file_name].create_new_chunk()
            print("waiting for 5 seconds...")
            time.sleep(5)
    print("Cannot append, try again later.")

def write_handler(file_name, chunk_idx, byte_start, byte_end, file_path):
    with open(file_path, "rb") as f:
        file_data = f.read()
    if file_name not in files:
        new_file = File(file_name)
        files[file_name] = new_file
    print("Write initiated")
    for attepmts in range(3):
        print("Attempt#: ", attepmts)
        response, status_code = files[file_name].write_chunk(file_data, byte_start, byte_end)
        if status_code == 200:
            print(response)
            return
        else:
            print("Error writing data: \n", response)
    print("Cannot write, try again later.")

def create_file_handler(file_name):
    if file_name not in files:
        new_file = File(file_name)
        files[file_name] = new_file
    print("Create initiated")
    files[file_name].create_new_chunk()

if __name__ == "__main__":
    while True:
        cmd = input().split()
        try:
            if cmd[0] == "read": # read file_name chunk_idx
                file_name = cmd[1]
                chunk_idx = int(cmd[2])
                read_handler(file_name, chunk_idx)

            elif cmd[0] == "write": # write file_name chunk_idx local_file_path
                write_handler(cmd[1], int(cmd[2]), int(cmd[3]), int(cmd[4]), cmd[5])

            elif cmd[0] == "append": # append file_name local_file_path
                file_name = cmd[1]
                file_path = cmd[2]
                append_handler(file_name, file_path)

            elif cmd[0] == "create":
                file_name = cmd[1]
                create_file_handler(file_name)
            
            elif cmd[0] == "delete":
                pass
            
            elif cmd[0] == "setmaster": # setmaster master_url; eg 10.37.155.40:8080
                MASTER_IP = cmd[1]
                MASTER_PORT = cmd[2]
                MASTER_URL = make_url(MASTER_IP, MASTER_PORT)
                

            elif cmd[0] == "exit":
                break

        except Exception as e:
            print("Invalid command")    