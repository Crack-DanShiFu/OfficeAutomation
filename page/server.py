import hashlib

from model.model import *


def hex_md5(s):
    m = hashlib.md5()
    m.update(s.encode('UTF-8'))
    return m.hexdigest()


def login_validation_server(u, p):
    if p is not None:
        p = hex_md5(p)
    users = db.session().query(Users).filter_by(name=u, password=p).first()
    if users is not None:
        return True, users
    return False, None
