import sys
import os
from dotenv import load_dotenv
import random

load_dotenv()

IP = os.getenv('ip')
PORT = int(sys.argv[1])
# PORT = int(os.getenv('port'))
RAM_AVAIL_GB = int(os.getenv('ram_avail_gb'))
DISK_AVAIL_GB = int(os.getenv('disk_avail_gb'))
CHUNK_SERVER_ID = f'CS_{PORT}'
CHUNK_SERVER_LOCATION_ID = random.randint(1, 10)
if len(sys.argv) > 2:
    CHUNK_LOCATION = os.path.join(os.getenv('chunk_location'), sys.argv[2])
else:
    CHUNK_LOCATION = os.getenv('chunk_location')
POST = ['POST']
GET = ['GET']
DELETE = ['DELETE']
HTTP_OK_STATUS_CODE = 200
HTTP_BAD_REQUEST_STATUS_CODE = 400
HTTP_INTERNAL_SERVER_ERROR_STATUS_CODE = 500
MASTER_URLS = os.getenv('master_urls').split(',')