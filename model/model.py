from exts import db


class User(db.Model):
    __tableName__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    password = db.Column(db.String(255))
