# encoding:utf8
from threading import Thread
from flask import current_app,render_template
from flask_mail import Message
from app import mail

# 异步发送邮件
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_mail(to, subject, templete, **kwargs):
    """
    :param to: 接收邮件的用户
    :param subject: 邮件主题
    :param templete: 模板
    :param kwargs: 其他参数收集
    :return:
    """
    app = current_app._get_current_object()
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(templete + '.txt', **kwargs)
    msg.html = render_template(templete + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr