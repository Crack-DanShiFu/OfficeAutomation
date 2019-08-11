import os
from datetime import timedelta

from flask import request, app, send_from_directory, abort, render_template, redirect, flash, url_for, session
from flask_login import login_required, login_user, logout_user
from is_safe_url import is_safe_url

from api.server import *
from page.server import *
from . import page


@page.route('/')
@login_required
def index():
    if session['employee_type'] == '管理员':
        return render_template('manage_user.html')
    else:
        return render_template('user.html')


@page.route('/register/')
def register_page():
    return render_template('register.html')


@page.route('/users/')
@login_required
def user_page():
    if session['employee_type'] == '管理员':
        return redirect(url_for('page.manage_user_page'))
    return render_template('user.html')


@page.route('/manage_user/')
@login_required
def manage_user_page():
    if session['employee_type'] == '用户':
        return redirect(url_for('page.user_page'))
    return render_template('manage_user.html')


@page.route('/modifyInfo/')
@login_required
def modify_info():
    user_name = session.get('user_name')
    return render_template('modify_info.html', data=user_name)


@page.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!')
    # session['employee_type']
    return redirect(url_for('page.login'))


@page.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    user_name = form.data.get('name')
    password = form.data.get('pwd')
    flag, user = login_validation_server(user_name, password)
    if flag:
        login_user(user, remember=True)
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=1)
        flash('Logged in successfully.')
        next = request.args.get('next')
        session['employee_type'] = user.employee_type
        session['user_name'] = user.name
        if user.employee_type == "管理员":
            return redirect(url_for('page.manage_user_page'))
        else:
            return redirect(url_for('page.user_page'))
    return render_template('login.html', form=form)
