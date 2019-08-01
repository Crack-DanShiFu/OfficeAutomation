import datetime
import json

from model.model import *


def queryWorkListByName(user_name, query_data):
    work_list = db.session().query(WorkList) \
        .filter(WorkList.completion_time.ilike(query_data + '%')) \
        .filter_by(user_name=user_name) \
        .all()
    return json.dumps([i.to_json() for i in work_list*10], ensure_ascii=False)
