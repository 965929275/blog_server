#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/1 20:19
# @Function: 
# @Author  : Tricky
from . import api
@api.route('/hellov1')
def hello():
    return 'hello,v1'