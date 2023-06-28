import os
import time
from datetime import timedelta

from flask import Flask, Response, make_response, request, session, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=31)

# 设置session
@app.route('/')
def index():
    # 設置session
    session['username'] = 'name'
    # 如果設置了 session.permanent 為 True，那麽過期時間是31天
    session.permanent = True
    # 讀取 session
    result = session.get('username')
    print(f"result: {result}")
    # # 刪除 session
    # session['username'] = False
    return "ok"
 
# 1.設定 Cookie
@app.route("/set")
def setcookie():
    resp = make_response('Setting cookie!')
    resp.set_cookie(key='framework', value='flask', expires=time.time()+6*60)
    return resp
 
# 2.取得Cookie
@app.route("/get")
def getcookie():
    value = request.cookies.get('framework')
    return jsonify(framework=value)
 
# 3.刪除Cookie
@app.route('/del')
def del_cookie():
    res = Response('delete cookies')
    res.set_cookie(key='framework', value='', expires=0)
    return res