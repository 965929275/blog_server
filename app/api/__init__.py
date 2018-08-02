#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/1 20:19
# @Function: 
# @Author  : Tricky

from flask import Blueprint

api = Blueprint('app',__name__)

from . import v1