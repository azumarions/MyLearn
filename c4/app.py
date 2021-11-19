from logging import PercentStyle
from os import O_RANDOM
from re import T
from flask import Flask, render_template, request, session, redirect, jsonify, current_app, g

import sqlite3
import json
from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm.exc import NoResultFound

import qrcode as qr
from PIL import Image
import base64
from io import BytesIO
import pickle

from sqlalchemy.orm.session import Session


app = Flask(__name__)
app.secret_key = b'random string...'

engine = create_engine('sqlite:///sample.sqlite3')

# get QRCode data.
def get_qrdata(s):
    qr_img = qr.make(s)

    byte_buf = BytesIO()
    qr_img.save(byte_buf, format="png")
    qr_data = byte_buf.getvalue()
    b64_data = 'data:image/png;base64,' + base64.b64encode(qr_data).decode("utf-8")
    return b64_data

# base model
Base = declarative_base()

# model class
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    password = Column(String(255))

    def to_dict(self):
        return {
            'id': int(self.id),
            'name': str(self.name),
            'password': str(self.password)
        }

class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer(), ForeignKey('users.id'))
    message = Column(String(255))
    created = Column(DateTime())

    user = relationship('User')
    
    def to_dict(self):
        return {
            'id': int(self.id),
            'user_id': int(self.user_id),
            'message': str(self.message),
            'created': str(self.created),
            'user': str(self.user.name)
        }

# get Model-list Dictionary
def get_by_list(arr):
    res = []
    for item in arr:
        res.append(item.to_dict())
    return res

# access top page.
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html',
    login = False,
    title = 'Messages',
    message = 'not logined....',
    data = [])

# post message
@app.route('/post', methods=['POST'])
def post_msg():
    id = request.form.get('id')
    msg = request.form.get('message')
    created = datetime.now()
    Session = sessionmaker(bind=engine)
    ses = Session()
    msg_obj = Message(user_id=id, message=msg, created=created)
    ses.add(msg_obj)
    ses.commit()
    ses.close()
    return 'True'

# get messages.
@app.route('/messages', methods=['POST'])
def get_msg():
    Session = sessionmaker(bind=engine)
    ses = Session()
    re = ses.query(Message).join(User).order_by(Message.created.desc())[:10]
    msgs = get_by_list(re)
    return jsonify(msgs)

# get QRcode Data
@app.route('/qr', methods=['POST'])
def get_qr():
    id = request.form.get('id')
    Session = sessionmaker(bind=engine)
    ses = Session()
    re = ses.query(Message).filter(Message.id == id).one()
    dic = re.to_dict()
    dic['qr'] = get_qrdata(re.message)
    return jsonify(dic)

# login form sended.
@app.route('/login', methods=['POST'])
def login_post():
    name = request.form.get('name')
    pswd = request.form.get('password')

    Session = sessionmaker(bind=engine)
    ses = Session()
    n = ses.query(User).filter(User.name == name).count()
    if n == 0:
        usr = User(name=name, password=pswd)
        ses.add(usr)
        ses.commit()
        flg = str(usr.id)
    else:
        usr = ses.query(User).filter(User.name == name).one()
        if pswd == usr.password:
            flg = str(usr.id)
        else:
            flg = 'False'
    ses.close()
    return flg

if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost', port=5001)