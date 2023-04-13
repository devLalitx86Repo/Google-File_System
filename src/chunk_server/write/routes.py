from flask import Blueprint
from utils.constants import POST

write_bp = Blueprint('write', __name__, url_prefix='/write')

@write_bp.route('/', methods = POST)
def writeChunk():
    pass