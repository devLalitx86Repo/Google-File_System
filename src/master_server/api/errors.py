from flask import Blueprint, Response
from threading import Thread
import time

errors = Blueprint("errors", __name__)

@errors.app_errorhandler(Exception)
def server_error(error):
    return Response(f"Oops, got an error! {error}", status=500)

class Crash_Routine():
    def __init__(self, master_server):
        self.master_server = master_server
        self.inspect_servers()

    def inspect_servers(self):
        inspect_gap = 5
        alive_cap = 30
        def inspect():
            while True:
                print("Inspecting Servers... ",len(self.master_server.chunk_servers))
                for chunk_server in self.master_server.chunk_servers.values():
                    if time.time() - chunk_server.last_ping > alive_cap:
                        self.master_server.removeChunkServer(chunk_server)
                time.sleep(inspect_gap)
        Thread(target=inspect).start()
