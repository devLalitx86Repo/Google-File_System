from models.Chunk_Server import Chunk_Server
from utils.constants import IP, PORT, CHUNK_SERVER_LOCATION_ID, DISK_AVAIL_GB, CHUNK_SERVER_ID

list_of_chunks = {}

chunk_server = Chunk_Server(
    ip=IP,
    port=PORT,
    loc_id=CHUNK_SERVER_LOCATION_ID,
    diskAvail=DISK_AVAIL_GB,
    id=CHUNK_SERVER_ID
)