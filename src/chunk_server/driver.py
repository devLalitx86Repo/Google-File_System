from flask import Flask
import os
import sys

from read.routes import read_bp
from write.routes import write_bp

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
app = Flask(__name__)

app.register_blueprint(read_bp)
app.register_blueprint(write_bp)
