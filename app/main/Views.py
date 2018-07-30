#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/30 10:49
# @Function: 
# @Author  : Tricky
from flask import jsonify,request
from flask_restful import Resource,reqparse
from ..models.User import LocalAuth,Profile
from app import db
import uuid
from app.Util.Email import send_mail
from app.Util.MakeResponse import make_response
from app.Util.Code import Code

class HelloWorld(Resource):
    def get(self):
        a = 'hello,world'
        return make_response(Code.OK,data=a)