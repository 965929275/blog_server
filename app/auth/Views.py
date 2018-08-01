# encoding:utf8
from flask import jsonify,request,url_for
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
    # method_decorators = [login_required]
    def __init__(self): # 获取token
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('token', type=str, required=True, location='args', help='access token error')
        self.args = self.parser.parse_args()

    def get(self):
        user = Profile.confirm(self.args.get('token'))
        user_profile = Profile.query.filter_by(username = user.username).first()
        user_profile.confirmed = True
        db.session.add(user_profile)
        db.session.commit()
        return make_response(Code.OK,data=user_profile.confirmed)


class ChangePwd(Resource):
    # method_decorators = [login_required]
    def put(self):
        username = request.json.get('username')
        new_password = request.json.get('new_password')
        user_local_auth = LocalAuth.query.filter_by(username = username).first()
        user_local_auth.password = new_password
        db.session.add(user_local_auth)
        db.session.commit()
        return make_response()


# 重设密码，用户忘记密码，使用邮箱更改密码
class ResetPwdEmail(Resource):
    # method_decorators = [login_required]
    def post(self):
        email = request.json.get('email')
        user = LocalAuth.query.filter_by(email=email).first()
        print(user)
        if user:
            token = user.generate_reset_token()
            print(token)
            send_mail(user.email, 'Reset Your Password', 'auth/email/reset_password', \
                      user=user, token=token, next=request.args.get('next'))
        return make_response()


# 确认重设密码token，然后跳转到重设密码页面
class ResetPwdConfirm(Resource):
    def __init__(self): # 获取token
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('token', type=str, required=True, location='args', help='access token error')
        self.args = self.parser.parse_args()

    def get(self):
        user = LocalAuth.confirm(self.args.get('token'))
        if user != None:
            url_for('auth.ResetPwdPage')
            print('tiaozhuan')
        else:
            return make_response(Code.BAD_REQUEST,message='该用户不存在')
        return make_response(Code.OK)


# 重设密码页面，从这里获得新密码并修改
class ResetPwdPage(Resource):
    def put(self):
        username = request.json.get('username')
        password = request.json.get('new_password')
        user = LocalAuth.query.filter_by(username=username).first()
        user.password = password
        db.session.add(user)
        db.session.commit()
        return make_response(Code.OK,message='change password success')


# 重设邮箱，改变用户注册(绑定)的邮箱
class ResetEmail(Resource):
    # method_decorators = [login_required]
    def post(self):
        username = request.json.get('username')
        email = request.json.get('email')
        new_email = request.json.get('new_email')
        global new_email
        user = LocalAuth.query.filter_by(username=username).first()
        token = user.generate_reset_token()
        send_mail(new_email,'Change Your Email','auth/email/reset_email', \
                          user=user, token=token, next=request.args.get('next'))
        return make_response()


class ResetEmailConfirm(Resource):
    def __init__(self): # 获取token
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('token', type=str, required=True, location='args', help='access token error')
        self.args = self.parser.parse_args()

    def get(self):
        user_local_auth = LocalAuth.confirm(self.args.get('token'))
        user_profile = Profile.query.filter_by(id=user_local_auth.id).first()
        user_local_auth.email = new_email
        user_profile.email = new_email
        print(new_email)
        db.session.add(user_local_auth)
        db.session.add(user_profile)
        db.session.commit()
        return make_response(Code.OK,message='修改邮箱成功')
        # user_profile = LocalAuth.confirm(self.args.get('token'))