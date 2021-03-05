from flask import Blueprint


api = Blueprint('routes', __name__)

from .index import index
