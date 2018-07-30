#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/26 9:08
# @Author  : Tricky
from flask import jsonify
from Code import Code


OK = 200
CREATED = 201
BAD_REQUEST = 400
UNAUTHORIZED = 401
FORBIDDEN = 403
NOT_FOUND = 404
INTERNAL_SERVER_ERROR = 500

msg = {
    OK: '请求成功',
    CREATED: '已创建。成功请求并创建了新的资源',
    BAD_REQUEST: '客户端请求的语法错误，服务器无法理解',
    UNAUTHORIZED: '请求要求用户的身份认证',
    FORBIDDEN: '服务器理解请求客户端的请求，但是拒绝执行此请求',
    NOT_FOUND: '未找到资源',
    INTERNAL_SERVER_ERROR: '服务器内部错误，无法完成请求'
}

def make_response(code=Code.OK, message=Code.msg[Code.OK],data=None):
    return jsonify(
        code = code,
        message = message,
        data = data
    )
