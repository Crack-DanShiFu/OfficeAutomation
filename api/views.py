
import os

from flask import request, app, send_from_directory, abort

from api.server import *
from . import api


@api.route('/')
def index():
    return "api"
