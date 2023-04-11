import uuid

# def generate_file_Path():

def generate_uuid():
    return str(uuid.uuid1().int>>64)