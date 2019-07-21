from flask import Flask, render_template
from exts import db
import config

from model.model import *

app = Flask(__name__)

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


@app.errorhandler(404)
def miss(e):
    return render_template('404.html')


@app.errorhandler(500)
def error(e):
    return render_template('500.html')


if __name__ == '__main__':
    app.run()
