#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/30 10:49
# @Function: 
# @Author  : Tricky
from flask import jsonify,request,current_app
from flask_restful import Resource,reqparse
from ..models.Articles import Articles
from app import db
import uuid
from app.Util.Email import send_mail
from app.Util.MakeResponse import make_response
from app.Util.Code import Code

class HelloWorld(Resource):
    def get(self):
        a = 'hello,world'
        return make_response(Code.OK,data=a)


class WriteArticle(Resource):
    def post(self):
        id = str(uuid.uuid4())
        title = request.json.get('title')
        content = request.json.get('content')
        body_html = request.json.get('body_html')
        user_id = '56defb16-2512-4b8f-aab8-72897fe13ef7'
        article = Articles(
            uuid = id,
            title = title,
            content = content,
            body_html= body_html,
            author_id = user_id
        )
        db.session.add(article)
        db.session.commit()
        return make_response()


class ViewArticles(Resource):
    def get(self):
        query = Articles.query.order_by(Articles.create_time.desc()).all()
        resp = [item.to_json() for item in query]
        return make_response(data=resp)

    def post(self):
        page = request.json.get('page')
        page = int(page)
        query = Articles.query
        pagination = query.order_by().paginate(
            page, per_page=current_app.config['FLASK_POSTS_PER_PAGE'], error_out=False)
        posts = pagination.items
        # print(posts)
        resp = [item.to_json() for item in posts]
        return make_response(data=resp)

