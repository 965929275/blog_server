#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/1 15:40
# @Function: 文章模型
# @Author  : Tricky
from app import db
from datetime import datetime
from User import Profile

class Articles(db.Model):
    __tablename__ = 'articles'
    uuid = db.Column(db.String(64),primary_key=True,comment='主键')
    title = db.Column(db.String(64),unique=True,comment='标题')
    content = db.Column(db.Text,comment='正文')
    body_html = db.Column(db.Text,comment='markdown源文本')
    create_time = db.Column(db.DateTime,index=True,default=datetime.utcnow,comment='创建时间')
    update_time = db.Column(db.DateTime,index=True,default=datetime.utcnow,comment='更新时间')
    num_of_view = db.Column(db.Integer,default=0,comment='浏览次数')

    # author_id = db.Column(db.String(128),db.ForeignKey('user_profile.id'))

    def to_json(self):
        json_articles = {
            'article_uuid':self.article_uuid,
            'title':self.title,
            'content':self.content,
            'summary':self.summary,
            'create_time':self.create_time,
            'update_time':self.update_time,
            'num_of_view':self.num_of_view
        }
        return json_articles

