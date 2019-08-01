from model.model import *


def login_validation_server(u, p):
    users = db.session().query(Users).filter_by(name=u, password=p).first()
    if users is not None:
        return True, users
    return False, None
