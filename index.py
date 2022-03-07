from flask import Flask, render_template, request, jsonify, redirect
app = Flask(__name__)

import certifi
import config

from pymongo import MongoClient
client = MongoClient(config.Mongo_key, tlsCAFile=certifi.where())
db = client.SOEUM


@app.route('/')
def home():
    return render_template('index.html')


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