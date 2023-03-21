from flask_pymongo import PyMongo
from flask import Flask, request, render_template, redirect, flash, jsonify
import hashlib
import datetime
import jwt

app = Flask(__name__, template_folder="templates")

app.config["MONGO_URI"] = "mongodb://localhost:27017/local"
mongo = PyMongo(app)
SECRET_KEY= 'BADABOGO'


@app.route('/')
def home():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route("/api/register", methods=["POST"])
def api_register():
    id = request.form.get('id')
    pswd1 = request.form.get('pswd1')
    pswd2 = request.form.get('pswd2')
    name = request.form.get('name')
    birth = request.form.get('yy')
    gender = request.form.get('gender')
    email = request.form.get('email')
    mobile = request.form.get('mobile')
    pw_hash = hashlib.sha256(pswd1.encode('utf-8')).hexdigest()

    if id == "":
        flash("아이디를 입력하세요.")
        return render_template("register.html")
    elif pswd1 == "":
        flash("비밀번호를 입력하세요.")
        return render_template("register.html")
    elif pswd2 == "":
        flash("비밀번호를 재입력히세요.")
        return render_template("register.html")
    elif name == "":
        flash("사용자이름을 입력하세요.")
        return render_template("register.html")
    elif birth == "":
        flash("생년월일을 입력하세요.")
    elif gender == "":
        flash("성별을 선택하세요.")
        return render_template("register.html")
    elif mobile == "":
        flash("휴대전화 번호를 입력하세요.")
        return render_template("register.html")

    result = mongo.db['signup'].find_one({'id':id})
    if result is not None:
        return jsonify({'result':'fail', 'msg':'이미 등록된 ID입니댜.'})
    else:
        mongo.db['signup'].insert_one({'id':id, 'pw':pw_hash, 'name':name, 'birth':birth, 'gender':gender, 'email':email, 'mobile':mobile})
        return jsonify({'result':'sucess'})

@app.route('/api/login', methods=['POST'])
def api_login():
    userid = request.form['userid']
    username = request.form['username']
    password = request.form['password']
    re_password = request.form['re_password']

    pw_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()

    result = mongo.db['signup'].find_one({'id':userid, 'pw':pw_hash})

    if result is not None:
        payload = {
            'id':userid,
            'exp':datetime.datetime.utcnow() + datetime.timedelta(seconds=90)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result':'success', 'token':token})
    else:
        return jsonify({'result':'fail', 'msg':'아이디 또는 비밀번호가 일치하지 않습니다.'})

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port='5000')