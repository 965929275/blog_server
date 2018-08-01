# encoding:utf8
from flask import Blueprint
from flask_restful import Api

from Views import HelloWorld,Register,Login,Logout,ChangePwd,Confirm,ResetPwdEmail,ResetEmail,ResetPwdConfirm,\
    ResetEmailConfirm

auth = Blueprint('auth', __name__)
api = Api(auth)

api.add_resource(HelloWorld, '/hello')
api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(ChangePwd, '/change_pwd')
api.add_resource(Confirm, '/confirm')
api.add_resource(ResetPwdEmail, '/reset_pwd')
api.add_resource(ResetPwdConfirm, '/reset_pwd_confirm')
api.add_resource(ResetEmail, '/reset_email')
api.add_resource(ResetEmailConfirm, '/reset_email_confirm')

from . import Views