#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/30 10:31
# @Function: 
# @Author  : Tricky

from flask import Blueprint
from flask_restful import Api

from Views import HelloWorld

main = Blueprint('main', __name__)
api = Api(main)

api.add_resource(HelloWorld, '/hello')



from . import Views