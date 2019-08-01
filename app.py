from flask import Flask, render_template
from flask_login import LoginManager

from exts import db
import config
from model.model import Users

app = Flask(__name__)

app.config.from_object(config)
app.config['SECRET_KEY'] = 'secret!'
app.config['JSON_AS_ASCII'] = False
db.init_app(app)
with app.app_context():
    db.create_all()

# api
from api import api

app.register_blueprint(api, url_prefix='/api')
# page
from page import page

app.register_blueprint(page, url_prefix='/')


@app.errorhandler(404)
def miss(e):
    return render_template('404.html')


@app.errorhandler(500)
def error(e):
    return render_template('500.html')


login_manger = LoginManager()
# 配置用户认证信息
login_manger.init_app(app)
# 认证加密程度
login_manger.session_protection = 'strong'
# 登陆认证的处理视图
login_manger.login_view = 'page.login'
# 登陆提示信息
login_manger.login_message = u'对不起，您还没有登录'
login_manger.login_message_category = 'info'
from app import login_manger


@login_manger.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


if __name__ == '__main__':
    db.metadata.clear()
    app.run()
