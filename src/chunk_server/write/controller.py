
import os
from util.models import chunkTempInfo, ChunkMetaInfo
from config import temporary_chunks, list_of_chunks
from util.constants import CHUNK_SERVER_ID, HTTP_BAD_REQUEST_STATUS_CODE, HTTP_INTERNAL_SERVER_ERROR_STATUS_CODE, HTTP_OK_STATUS_CODE, CHUNK_LOCATION
from utils.checksum import generate_checksum, validate_checksum
from utils.api_request import post_dict
from utils.gen import make_url
import traceback


class WriteChunk:
    def __init__(self):
        pass


    def operation(self, pkt_json):
        try:
            other_chunk_server_info = None
            if 'chunkServerInfo' in pkt_json:
                other_chunk_server_info = [*pkt_json['chunkServerInfo']]
                del pkt_json['chunkServerInfo']
            
            if other_chunk_server_info:
                resp = self.replicate(pkt_json, other_chunk_server_info)
                if not resp:
                    return None
            else:
                self.writeIntoMemory(pkt_json['chunkHandle'], pkt_json['byteStart'], pkt_json['byteEnd'], pkt_json['data'])
                resp = True

            return resp
        except Exception as e:
            print(e)
            print(traceback.format_exc())
        return None

    def writeIntoMemory(self, handle, byte_start, byte_end, file_data):
        obj = chunkTempInfo(file_data, byte_start, byte_end)
        temporary_chunks[handle] = obj


    def uncommit(self, pkt_json):
        pass

    def commit(self, pkt_json):
        try:
            handle = pkt_json['chunkHandle']
            if handle not in temporary_chunks:
                return None
            
            obj = temporary_chunks[handle]

            resp = self.writeIntoDisk(handle, obj.byteStart, obj.byteEnd, obj.chunkData)
            del temporary_chunks[handle]
            if resp:
                return resp
        except Exception as e:
            print(e)
            print(traceback.format_exc())

        return None
    
    def sendDataForReplication(self, url, pkt_json):

        jdata, scode = post_dict(url, pkt_json)
        if scode == HTTP_OK_STATUS_CODE:
            return True
        return False
    
    def sendCommitRequest(self, url, data):
        jdata, scode = post_dict(url, data)
        if scode == HTTP_OK_STATUS_CODE:
            return jdata['checksum']
        return None

    def replicate(self, pkt_json, other_chunk_server_info):
        replication_factor = 0

        for info in other_chunk_server_info:
            if info['chunkServerId'] == CHUNK_SERVER_ID:
                continue

            proper_url = make_url(info['ipAddress'], info['port']) + '/write/'
            res = self.sendDataForReplication(proper_url, pkt_json)
            if not res:
                return None
            replication_factor += 1

        checks = []
        mk_rf = 0

        for info in other_chunk_server_info:
            if info['chunkServerId'] == CHUNK_SERVER_ID:
                continue

            proper_url = make_url(info['ipAddress'], info['port']) + '/write/commit'
            res = self.sendCommitRequest(proper_url, {'chunkHandle' : pkt_json['chunkHandle']})
            # if not res:
            #     return None
            if res:
                checks.append(res)
                mk_rf += 1

        if mk_rf != replication_factor:
            #uncommit all
            pass
        
        checksum_gen = generate_checksum(pkt_json['data'])
        for check in checks:
            if check != checksum_gen:
                return None
            
        res = self.writeIntoDisk(pkt_json['chunkHandle'], pkt_json['byteStart'], pkt_json['byteEnd'], pkt_json['data'])
        return res


    def updateChunkList(self, handle, data):
        checksum = generate_checksum(data)
        obj = ChunkMetaInfo(handle, checksum)
        list_of_chunks[handle] = obj
        return checksum

    def writeIntoDisk(self, handle, byte_start, byte_end, file_data):
        file_path = os.path.join(CHUNK_LOCATION, handle)
        if not os.path.isfile(file_path):
            with open(file_path, 'w') as y:
                pass
            
        file_size = os.path.getsize(file_path)
        if(byte_start < 0 or byte_start > file_size or (byte_start != 0 and file_size < byte_end) or  byte_end <= 0 or len(file_data) != byte_end - byte_start + 1):
            return None
        with open(file_path, 'r+') as tmp:
            tmp.seek(byte_start)
            tmp.write(file_data)

        checksum = self.updateChunkList(handle, file_data)

        return checksum