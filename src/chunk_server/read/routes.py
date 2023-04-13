from flask import Blueprint
from utils.constants import GET

read_bp = Blueprint('read', __name__, url_prefix='/read')

@read_bp.route('/<chunkHandle>', methods = GET)
def readChunk(chunkHandle):
    pass