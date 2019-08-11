import os
import time

from flask import request, app, send_from_directory, abort, session, redirect
from flask_login import login_required
from api.server import *
from . import api


@api.route('/')
@login_required
def index():
    return "api"


@api.route('/getWorkList/', methods=['POST'])
@login_required
def getWorkList():
    user_name = session.get('user_name')
    form_data = request.form.to_dict()
    if form_data.get('query_date'):
        d = form_data.get('query_date')
    else:
        d = datetime.datetime.now().strftime('%Y-%m-%d')
    return queryWorkListByName(user_name, d)


@api.route('/getUserList/', methods=['POST'])
@login_required
def getUserList():
    form_data = request.form.to_dict()
    print(form_data)
    # user_name = session.get('user_name')
    # d = datetime.datetime.now().strftime('%Y-%m-%d')
    form_data['employee_type'] = '用户'
    return queryUserList(form_data)


@api.route('/addUserTask/', methods=['get', 'post'])
@login_required
def addUserTask():
    form_data = request.form.to_dict()
    addUserTaskService(form_data)
    # user_name = session.get('user_name')
    # d = datetime.datetime.now().strftime('%Y-%m-%d')
    return redirect('/')


@api.route('/getWorkListByName/', methods=['get', 'post'])
@login_required
def getWorkListByName():
    form_data = request.form.to_dict()
    if form_data.get('query_date'):
        d = form_data.get('query_date')
    else:
        d = datetime.datetime.now().strftime('%Y-%m-%d')
    return queryWorkListByName(form_data['user_name'], d)


@api.route('/addWorkConclusion/', methods=['get', 'post'])
@login_required
def addWorkConclusion():
    form_data = request.form.to_dict()
    form_data['user_name'] = session.get('user_name')
    form_data['data_time'] = datetime.datetime.now().strftime('%Y-%m-%d')
    addWorkConclusionServise(form_data)
    return redirect('/')


@api.route('/getWorkConclusion/', methods=['get', 'post'])
@login_required
def getWorkConclusion():
    user_name = session.get('user_name')
    form_data = request.form.to_dict()
    if form_data.get('query_date'):
        d = form_data.get('query_date')
    else:
        d = datetime.datetime.now().strftime('%Y-%m-%d')
    return queryWorkConclusion(user_name, d)


# userCommit

@api.route('/userCommit/', methods=['get', 'post'])
@login_required
def userCommit():
    form_data = request.form.to_dict()
    userCommitServise(form_data)
    return redirect('/')


# register_new

@api.route('/register_new/', methods=['post'])
def registerNew():
    form_data = request.form.to_dict()
    if addUserAccountServices(form_data):
        return redirect('/')
    else:
        return '用户名重复'


# user_modify
@api.route('/user_modify/', methods=['post'])
def user_modify():
    form_data = request.form.to_dict()
    if modifyUserAccountServices(form_data):
        return redirect('/')
    else:
        return '密码错误'
