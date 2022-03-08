from flask import Flask, render_template, request, jsonify, redirect
app = Flask(__name__)

from random import randrange

import certifi
import config

from pymongo import MongoClient
client = MongoClient(config.Mongo_key,tlsCAFile=certifi.where())
db = client.SOEUM


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/like')
def like():
    return render_template('like.html')


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


@app.route("/post", methods=["POST"])
def post():

    name_receive = request.form['name']
    pwd_receive = request.form['pwd']

    doc = {
        'name': name_receive,
        'pwd': pwd_receive
    }

    db.user.insert_one(doc)
    return redirect("/")


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)


