import os
import typing as t
from http import HTTPStatus
from flask import Flask, redirect, render_template, request
from flask.views import MethodView
from flask import Flask, jsonify, render_template, Response

app = Flask(__name__)

# 文件大小限制(超過 16M 大小的文件將無法上傳)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
UPLOAD_FOLDER = './upload'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

class ImageResponse(Response):
    default_mimetype = 'image/jpeg'

@app.route("/")
def index():
    return "ok"

class UserView(MethodView):
    def get(self):
        name = request.args['name']
        age = request.args['age']
        print(name, age)
        return 'ok'

    def post(self):
        # name = request.form['name']
        # age = request.form['age']
        # print(name, age)
        data = request.get_json()
        print("json:", data)
        return 'ok'
    
app.add_url_rule('/users', view_func=UserView.as_view('users'))

@app.route('/welcome')
def welcome():
    return render_template('welcome.html', name='小明')

@app.route('/login', methods=['GET', 'POST'])
def do_login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        name = request.form['name']
        password = request.form['password']
        if name == 'python':
            return render_template('index.html', name=name)
        else:
            return redirect('/login')

@app.route("/image")
def image():
    f = open("static/images/mikko.png", 'rb')
    resp = ImageResponse(f.read())
    return resp

@app.route('/uploadfile', methods=['POST', 'GET'])
def do_upload():
    if request.method == 'POST':
        # file = request.files['file']
        files = request.files.getlist('file')
        for file in files:
            if file and allowed_file(file.filename):
                # filename = secure_filename(file.filename)
                filename = file.filename
                file.save(os.path.join(UPLOAD_FOLDER, filename))

    return render_template('upload.html')