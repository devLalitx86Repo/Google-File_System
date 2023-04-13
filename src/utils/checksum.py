import hashlib

def generate_checksum(chunk_data):
    md5 = hashlib.md5()
    md5.update(chunk_data)
    return md5.digest()

def validate_checksum(chunk_data, checksum):
    return generate_checksum(chunk_data) == checksum
