import sys
import os
from dotenv import load_dotenv

load_dotenv()

IP = os.getenv('ip')
PORT = int(sys.argv[1])
# PORT = int(os.getenv('port'))
RAM_AVAIL_GB = int(os.getenv('ram_avail_gb'))
DISK_AVAIL_GB = int(os.getenv('disk_avail_gb'))
CHUNK_SERVER_ID = f'chunk_server_{PORT}'