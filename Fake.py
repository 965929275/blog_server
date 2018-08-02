#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/2 18:05
# @Function: 生成文章假数据
# @Author  : Tricky
from faker import Faker
from app.models.Articles import Articles
from app import db
from app import create_app
from sqlalchemy.exc import IntegrityError
from uuid import uuid4

app = create_app('default')

def articles(count=50):
    with app.app_context():
        fake = Faker()
        i = 0
        while i < count:
            uuid = str(uuid4())
            articles = Articles(
                uuid = uuid,
                title = fake.user_name(),
                content = fake.text(),
                body_html = fake.text(),
                create_time= fake.past_date(),
                author_id = '56defb16-2512-4b8f-aab8-72897fe13ef7'
            )
            db.session.add(articles)
            try:
                db.session.commit()
                i += 1
            except IntegrityError:
                db.session.rollback()

articles()