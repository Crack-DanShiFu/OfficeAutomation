from flask import flash
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Length, Required

from exts import db


class Users(db.Model, UserMixin):
    __tableName__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(10))
    cell_phone_number = db.Column(db.String(12))
    password = db.Column(db.Text)
    employee_type = db.Column(db.String(5))

    # 定义验证密码的函数confirm_password
    def confirm_password(self, password):
        return password == self.password

    def get_id(self):
        return self.id

    def get_info(self):
        json_data = {
            'id': self.id,
            'user_name': self.name,
            'employee_type': self.employee_type
        }
        return json_data


class WorkList(db.Model):
    __tableName__ = 'work_list'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    work_name = db.Column(db.String(50))  # 工作名
    work_content = db.Column(db.Text)  # 工作内容
    work_plan = db.Column(db.String(50))  # 工作计划
    user_name = db.Column(db.String(10))  # 用户名
    source = db.Column(db.String(10))  # 来源
    release_time = db.Column(db.DateTime)  # 管理员发布时间
    rate_of_progress = db.Column(db.String(50))  # 进度
    ######
    user_no = db.Column(db.String(10))  # 户号
    user_na = db.Column(db.String(10))  # 户名
    business_type = db.Column(db.String(20))  # 业务类型
    process_no = db.Column(db.String(20))  # 流程号
    capacity = db.Column(db.String(10))  # 容量
    Acceptance_time = db.Column(db.DateTime)  # 受理时间
    reply_time = db.Column(db.DateTime)  # 答复时间
    design_send_time = db.Column(db.DateTime)  # 设计发出时间
    design_complete_time = db.Column(db.DateTime)  # 设计完成时间
    construction_send_time = db.Column(db.DateTime)  # 施工发出时间
    construction_complete_time = db.Column(db.DateTime)  # 施工完成时间
    user_requirement = db.Column(db.String(50))  # 用户需求概况
    design_department = db.Column(db.String(10), default="23公司")  # 设计单位 (是否为集体企业)
    construction_department = db.Column(db.String(10), default="深圳")  # 施工单位(是否为集体企业)
    send_power_time = db.Column(db.DateTime)  # 送电时间
    address = db.Column(db.String(50))  # 地址
    state = db.Column(db.String(10), default="未提交")  # 地址

    ######

    def to_json(self):
        json_data = {
            'id': self.id,
            'work_name': self.work_name,
            'work_content': self.work_content,
            'work_plan': self.work_plan,
            'user_name': self.user_name,
            'source': self.source,
            'rate_of_progress': self.rate_of_progress,
            'release_time': str(self.release_time),
            ######
            'user_no': self.user_no,
            'user_na': self.user_na,
            'business_type': self.business_type,
            'process_no': self.process_no,
            'capacity': self.capacity,
            'Acceptance_time': str(self.Acceptance_time),
            'reply_time': str(self.reply_time),
            'design_send_time': str(self.design_send_time),
            'design_complete_time': str(self.design_complete_time),
            'construction_send_time': str(self.construction_send_time),
            'construction_complete_time': str(self.construction_complete_time),
            'user_requirement': self.user_requirement,
            'design_department': self.design_department,
            'construction_department': self.construction_department,
            'send_power_time': str(self.send_power_time),
            'address': self.address,
            'state': self.state,
        }
        return json_data


class WorkConclusion(db.Model):
    __tableName__ = 'work_Conclusion'
    user_name = db.Column(db.String(10), primary_key=True)  # 用户名
    data_time = db.Column(db.DateTime, primary_key=True)  # 用户名
    conclusion = db.Column(db.Text)

    def get_info(self):
        json_data = {
            'user_name': self.user_name,
            'data_time': str(self.data_time),
            'conclusion': self.conclusion
        }
        return json_data


class LoginForm(FlaskForm):
    name = StringField(
        label="昵称(账号)",
        description="昵称(账号)",
        validators=[
            DataRequired("请输入昵称(账号)"),
            Length(5, 10, message=u'长度位于5~10之间')
        ],

        render_kw={
            "class": "form-control input-lg",
            "placeholder": "昵称(账号)",
        }
    )
    pwd = PasswordField(
        label="密码",
        description="密码",
        validators=[
            DataRequired("请输入密码"),
            Length(5, 20, message=u'长度位于5~20之间')
        ],
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "密码",
        }
    )

    submit = SubmitField(
        label="登录",
        render_kw={
            "class": "btn btn-lg btn-success btn-block",
        }
    )

    # 最好在forms中验证账号
    def validate_name(self, field):
        name = field.data
        if Users.query.filter_by(name=name).count() == 0:
            flash('账号不存在', 'error')
            # raise ValidationError("")
