# encoding:utf8
from app import db
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin

# 主表
class LocalAuth(db.Model):
    __tablename__ = 'user_local_auth'
    id = db.Column(db.String(128),primary_key=True,index=True)
    username = db.Column(db.String(64),unique=True,index=True)
    password = db.Column(db.String(64))
    email = db.Column(db.String(64),unique=True,index=True)
    def to_json(self):
        json_local_auth = {
            'username': self.username
        }
        return json_local_auth

# 用户信息表
class Profile(db.Model):
    __tablename__ = 'user_profile'
    id = db.Column(db.String(128),primary_key=True)
    username = db.Column(db.String(64),unique=True,index=True)
    phone_num = db.Column(db.String(11),index=True)
    email = db.Column(db.String(64),unique=True,index=True)
    nick_name = db.Column(db.String(32),unique=True)
    confirmed = db.Column(db.Boolean,default=False)
    register_time = db.Column(db.DateTime(),default=datetime.now)

    def to_json(self):
        json_profile = {
            'username': self.username
        }
        return json_profile

    # 生成令牌
    def generate_confirmation_token(self, expiration = 3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    # 检验令牌
    # @staticmethod
    # def confirm(token):
    #     s = Serializer(current_app.config['SECRET_KEY'])
    #     try:
    #         data = s.loads(token)
    #         print(data)
    #     except:
    #         print('load wrong')
    #         return False
    #     if data.get('confirm') != Profile.id:
    #         return False
    #     confirmed = True
    #     db.session.add(confirmed)
    #     db.session.commit()
    #     return True
    @staticmethod
    def confirm(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            token_data = s.loads(token)
        except:
            print('token 过期')
            return None
        user = Profile.query.filter_by(id=token_data.get('confirm')).first()
        return user