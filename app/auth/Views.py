# encoding:utf8
from flask import jsonify,request
from flask_restful import Resource,reqparse
from ..models.User import LocalAuth,Profile
from app import db
import uuid
from app.Util.Email import send_mail
from app.Util.MakeResponse import make_response
from app.Util.Code import Code
from flask_login import login_required


class HelloWorld(Resource):
    def get(self):
        a = 'hello,world'
        return make_response(Code.OK,data=a)


class Register(Resource):
    def post(self):
        id = str(uuid.uuid4())
        username = request.json.get('username')
        password = request.json.get('password')
        email = request.json.get('email')
        user = LocalAuth.query.filter_by(username = username).first()
        user_mail = LocalAuth.query.filter_by(email = email).first()
        if user != None:
            return make_response(201,message='该用户名已被注册')
        elif user_mail != None:
            return make_response(201,message='该邮箱已被注册')
        else:
            user_local_auth = LocalAuth(
                id = id,
                username = username,
                password = password,
                email = email
            )
            user_profile = Profile(
                id = id,
                username = username,
                email = email
            )
            db.session.add(user_local_auth)
            db.session.add(user_profile)
            db.session.commit()
            token = user_profile.generate_confirmation_token()
            send_mail(user_local_auth.email, 'Confirm Your Account',
                      'auth/email/confirm', user=user_profile, token=token)
        return make_response(data=token)


class Login(Resource):
    def post(self):
        username = request.json.get('username')
        password = request.json.get('password')
        user = LocalAuth.query.filter_by(username = username).first()
        if user is not None and user.password == password:
            return make_response()
        elif user is not None and user.password != password:
            return make_response(Code.BAD_REQUEST,message='密码错误')
        elif user is None:
            return make_response(Code.BAD_REQUEST,message='该用户未注册')


class Logout(Resource):
    def get(self):
        pass


# 确认账户，通过邮箱与用户取得联系，发送确认链接给用户，从而确认用户
# 这里要加一个login_required的装饰器
class Confirm(Resource):
    method_decorators = [login_required]
    def __init__(self): # 获取token
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('token', type=str, required=True, location='args', help='access token error')
        self.args = self.parser.parse_args()

    def get(self):
        user = Profile.confirm(self.args.get('token'))
        user_local_auth = Profile.query.filter_by(username = user.username).first()
        user_local_auth.confirmed = True
        db.session.add(user_local_auth)
        db.session.commit()
        return make_response(Code.OK,data=user_local_auth.confirmed)


class ChangePwd(Resource):
    method_decorators = [login_required]
    def put(self):
        username = request.json.get('username')
        new_password = request.json.get('new_password')
        user_local_auth = LocalAuth.query.filter_by(username = username).first()
        user_local_auth.password = new_password
        db.session.add(user_local_auth)
        db.session.commit()
        return make_response()


# 重设密码，用户忘记密码，使用邮箱更改密码
class ResetPwd(Resource):
    method_decorators = [login_required]
    pass


# 重设邮箱，改变用户注册的邮箱
class ResetEmail(Resource):
    method_decorators = [login_required]
    pass


#