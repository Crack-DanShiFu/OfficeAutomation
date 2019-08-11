import datetime
import hashlib
import json

from sqlalchemy import func

from model.model import *


def hex_md5(s):
    m = hashlib.md5()
    m.update(s.encode('UTF-8'))
    return m.hexdigest()


# .filter(WorkList.release_time.ilike(query_data + '%')) \

def queryWorkListByName(user_name, query_data):
    work_list = db.session().query(WorkList) \
        .filter_by(user_name=user_name) \
        .filter(WorkList.release_time.ilike(query_data + '%')) \
        .all()
    return json.dumps([i.to_json() for i in work_list], ensure_ascii=False)


#
def queryUserList(form_data):
    user_list = db.session().query(Users).filter_by(employee_type=form_data['employee_type'])
    if form_data.get('query_date'):
        d = form_data.get('query_date')
    else:
        d = datetime.datetime.now().strftime('%Y-%m-%d')

    conclusion_list = WorkConclusion.query.filter(
        WorkConclusion.data_time.ilike(d + '%'))
    work_List = db.session.query(WorkList.user_name, func.count(WorkList.id)).filter(
        WorkList.release_time.ilike(d + '%')).group_by(WorkList.user_name).all()
    temp_list = {}
    w_list = {}
    for c in conclusion_list:
        temp_list[c.get_info()['user_name']] = c.get_info()
    temp_list2 = [i.get_info() for i in user_list]

    for w in work_List:
        w_list[w[0]] = w[1]
    print(w_list)
    for c in temp_list2:
        if c['user_name'] in temp_list.keys():
            c['conclusion'] = temp_list[c['user_name']]['conclusion']
        else:
            c['conclusion'] = '未填写'
        if c['user_name'] in w_list:
            c['num_of_work'] = w_list[c['user_name']]
        else:
            c['num_of_work'] = '0'
            pass
    return json.dumps(temp_list2, ensure_ascii=False)


def addUserTaskService(form_data):
    id = form_data.get('id')
    form_data.pop('id')
    d = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    form_data['release_time'] = d
    for f in list(form_data.keys()):
        if form_data[f] is "":
            form_data.pop(f)
    temp = db.session().query(WorkList).filter_by(id=id)
    if id and temp:
        print("更新数据")
        WorkList.query.filter_by(id=id).update(form_data)
    else:
        print("添加数据")
        db.session.add(WorkList(**form_data))
    db.session.commit()


def addWorkConclusionServise(form_data):
    temp = WorkConclusion.query.filter(WorkConclusion.user_name.ilike(form_data['user_name']),
                                       WorkConclusion.data_time.ilike(form_data['data_time'] + '%')).first()
    if not temp:
        print('提交总结')
        db.session.add(WorkConclusion(**form_data))
    else:
        print('更新总结')
        print(form_data['data_time'])
        WorkConclusion.query.filter_by(user_name=form_data['user_name'],
                                       data_time=form_data['data_time']).update(form_data)
    db.session.commit()


def queryWorkConclusion(user_name, data_time):
    temp = db.session().query(WorkConclusion).filter_by(user_name=user_name,
                                                        data_time=data_time)
    return json.dumps([t.get_info() for t in temp], ensure_ascii=False)


def userCommitServise(form_data):
    id = form_data['id']
    for f in list(form_data.keys()):
        if form_data[f] is "":
            form_data.pop(f)
    WorkList.query.filter_by(id=id).update(form_data)
    db.session.commit()


def addUserAccountServices(form_data):
    form_data['password'] = hex_md5(form_data['password'])
    temp = db.session().query(Users).filter_by(name=form_data['name'])
    for t in temp:
        return False
    db.session.add(Users(**form_data))
    db.session.commit()
    return True


def modifyUserAccountServices(form_data):
    temp = db.session().query(Users).filter_by(name=form_data['name'], password=hex_md5(form_data['originalPw']))
    for i in temp:
        form_data['password'] = hex_md5(form_data['password'])
        form_data.pop('originalPw')
        Users.query.filter_by(name=form_data['name']).update(form_data)
        db.session.commit()
        return True
    return False
