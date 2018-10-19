
from flask import Blueprint
api = Blueprint('api', __name__)

from . import hello
from . import health
from . import demo
