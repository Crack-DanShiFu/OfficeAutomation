import os
import time

from flask import request, app, send_from_directory, abort, session
from flask_login import login_required

from api.server import *
from . import api


@api.route('/')
@login_required
def index():
    return "api"


@api.route('/getWorkList/')
@login_required
def getWorkList():
    user_name = session.get('user_name')
    d = datetime.datetime.now().strftime('%Y-%m-%d')
    return queryWorkListByName(user_name, d)
