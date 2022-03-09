import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = 'SPARTA'

from random import randrange

import certifi
import config

from pymongo import MongoClient
client = MongoClient(config.Mongo_key, tlsCAFile=certifi.where())
db = client.SOEUM


@app.route('/post')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        return render_template('post.html')

    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


@app.route('/like')
def like():
    return render_template('like.html')


@app.route('/')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)


@app.route('/update_like', methods=['POST'])
def update_like():
    action_receive = request.form["action_give"]
    #랜덤 숫자
    number = randrange(10)
    doc = {
        "number": number,
        "like": "test",
        "id": "test"
    }
    if action_receive == "like":
        db.likes.insert_one(doc)
    else:
        db.likes.insert_one(doc)
    return redirect("/like")


@app.route('/top5', methods=['GET'])
def get_top():

    number_list = list(db.likes.find({}, {'_id':False}).sort("number", -1).limit(5))

    # number_list = list(db.likes.find({}, {'_id':False}))

    # for rows in number_list:
    #     print(rows)
    return jsonify({'mynumber':number_list})


@app.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.user.find_one({'username': username_receive, 'password': pw_hash})

    if result is not None:
        payload = {
         'id': username_receive,
         'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    nickname_receive = request.form['nickname_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "username": username_receive,                               # 아이디
        "password": password_hash,                                  # 비밀번호
        "nick_name": nickname_receive                               # 이름
    }
    db.user.insert_one(doc)
    return jsonify({'result': 'success'})


@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.user.find_one({"username": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})


@app.route('/post', methods=['POST'])
def posting():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"username": payload["id"]})

        keyword_receive = request.form["keyword_give"]
        url_receive = request.form["url_give"]

        post_rist = list(db.post.find({}, {'_id': False}))
        count = len(post_rist) + 1

        doc = {
            "num": count,
            "keyword": keyword_receive,
            "url": url_receive,
            "username": user_info["username"]
        }
        db.post.insert_one(doc)
        return jsonify({'result': 'success', 'msg': '성공'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


@app.route("/posting", methods=["GET"])
def post_get():
    post_list = list(db.post.find({}, {'_id': False}))
    photo_list = list(db.post.find({}, {'_id': False}))
    return jsonify({'posts': post_list})



    my_string = 'https://i1.ytimg.com/vi//default.jpg'
    text = 'https://www.youtube.com/watch?v=4LIt_ICJyjk'
    out = text.split('=')
    index = my_string.find('/default.jpg')
    final_string = my_string[:index] + (out[1]) + my_string[index:]
    print(final_string)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)