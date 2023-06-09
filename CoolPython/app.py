from datetime import datetime

from flask import Flask, make_response, request, session, g

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to gusss'

@app.route("/")
def index():
    # 嘗試獲取 first_access cookie
    first_access = request.cookies.get('first_access')

    # 沒有first_access cookie，是第一次來
    if first_access is None:        
        first_access = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        res = make_response('hello world')
        # 在響應頭里設置cookie，設置了過期時間(max_age) 60 秒
        expires_time = datetime(year=2023, month=6, day=7, hour=10, minute=20)
        # res.set_cookie('first_access', first_access, max_age=60)        
        res.set_cookie('first_access', first_access, expires=expires_time)        
        return res
    
    # 不是第一次來
    else:       
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"你第一次訪問這個網頁的時間是: {first_access}, now: {now}"

@app.route('/login/<string:username>')
def name_view(username):
    session['username'] = username
    return 'ok'

@app.route('/get_name')
def get_name():
    if 'username' not in session:
        return 'not login'
    else:
        return 'welcome ' + session['username']
    
@app.route("/logout")
def logout():
    try:
        # 刪除 username session
        session.pop('username')     
    except KeyError:
        pass
    session.clear()             # 清空所有session
    return "logout"

@app.route('/youhui')
def youhui():
    grade = request.args['grade']
    g.grade = grade
    return get_amount_by_grade()


def get_amount_by_grade():
    grade = g.grade
    if grade == 'a':
        return '100'
    else:
        return '80'

from admin import admin_blue
from user import user_blue

app.register_blueprint(admin_blue)
app.register_blueprint(user_blue)