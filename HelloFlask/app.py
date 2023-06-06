import os
import sys

import click
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import (LoginManager, UserMixin, current_user, login_required,
                         login_user, logout_user)
from flask_sqlalchemy import SQLAlchemy
from markupsafe import escape
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
WIN = sys.platform.startswith('win')
if WIN:  # 如果是 Windows 系統，使用三個斜線
    prefix = 'sqlite:///'
else:  # 否則使用四個斜線
    prefix = 'sqlite:////'
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 關閉對模型修改的監控
app.config['SECRET_KEY'] = 'dev'  # 等同於 app.secret_key = 'dev'
db = SQLAlchemy(app)  # 初始化擴展，傳入程序實例 app
login_manager = LoginManager(app)  # 實例化擴展類

# 如果未登錄的用戶訪問 @login_required 對應的 URL，Flask-Login 會把用戶重定向到登錄頁面，並顯示一個錯誤提示。
# 為了讓這個重定向操作正確執行，我們還需要把 login_manager.login_view 的值設為我們程序的登錄視圖端點（函數名）
login_manager.login_view = 'login'

# 利用下方指令，生成資料庫以及相關表格(附帶 --drop，則先刪除原本的，再建立新的。)
# $ flask initdb
@app.cli.command()  # 注冊為命令，可以傳入 name 參數來自定義命令
@click.option('--drop', is_flag=True, help='Create after drop.')  # 設置選項
def initdb(drop):
    """Initialize the database."""
    if drop:  # 判斷是否輸入了選項
        click.echo("Drop database.")
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')  # 輸出提示信息

# 利用下方指令，建立用戶(第一位會是管理員)
# $ flask admin
# Username: Henry Lee
# Password: (因設置 hide_input=True，因此看不到輸入的內容)
# Repeat for confirmation: (因設置 hide_input=True，因此看不到輸入的內容)
# 使用 click.option() 裝飾器設置的兩個選項分別用來接受輸入用戶名和密碼。
@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
def admin(username, password):
    """Create user."""
    db.create_all()

    user = User.query.first()
    if user is not None:
        click.echo('Updating user...')
        user.username = username
        user.set_password(password)  # 設置密碼
    else:
        click.echo('Creating user...')
        user = User(username=username, name='Admin')
        user.set_password(password)  # 設置密碼
        db.session.add(user)

    db.session.commit()  # 提交數據庫會話
    click.echo('Done.')

# 利用下方指令，初始化資料庫數據
# $ flask forge
@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()

    # 全局的兩個變量移動到這個函數內
    # name = 'Henry Li'
    # user = User(name=name)
    # db.session.add(user)

    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]

    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')

# Flask-Login 提供了一個 current_user 變量，注冊這個函數的目的是，當程序運行後，
# 如果用戶已登錄， current_user 變量的值會是當前用戶的用戶模型類記錄。
@login_manager.user_loader
def load_user(user_id):  # 創建用戶加載回調函數，接受用戶 ID 作為參數
    user = User.query.get(int(user_id))  # 用 ID 作為 User 模型的主鍵查詢對應的用戶
    return user  # 返回用戶對象

class User(db.Model, UserMixin):
    """
    繼承 UserMixin 會讓 User 類擁有幾個用於判斷認證狀態的屬性和方法，其中最常用的是 is_authenticated 屬性：如果當前用戶已經登錄，
    那麽 current_user.is_authenticated 會返回 True ，否則返回 False。
    有了 current_user 變量和這幾個驗證方法和屬性，我們可以很輕松的判斷當前用戶的認證狀態。
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))  # 用戶名
    password_hash = db.Column(db.String(128))  # 密碼散列值

    def set_password(self, password):  # 用來設置密碼的方法，接受密碼作為參數
        self.password_hash = generate_password_hash(password)  # 將生成的密碼保持到對應字段

    def validate_password(self, password):  # 用於驗證密碼的方法，接受密碼作為參數
        return check_password_hash(self.password_hash, password)  # 返回布爾值

class Movie(db.Model):  # 表名將會是 movie
    id = db.Column(db.Integer, primary_key=True)  # 主鍵
    title = db.Column(db.String(60))  # 電影標題
    year = db.Column(db.String(4))  # 電影年份

@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)

@app.errorhandler(404)  # 傳入要處理的錯誤代碼
def page_not_found(e):  # 接受異常對象作為參數
    return render_template('404.html'), 404  # 返回模板和狀態碼

# flask run --debug --reload --debugger
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':  # 判斷是否是 POST 請求
        if not current_user.is_authenticated:
            return redirect(url_for('index'))  # 重定向回主頁
        
        # 獲取表單數據
        title = request.form.get('title')  # 傳入表單對應輸入字段的 name 值
        year = request.form.get('year')
        # 驗證數據
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')  # 顯示錯誤提示
            return redirect(url_for('index'))  # 重定向回主頁
        
        # 保存表單數據到數據庫
        movie = Movie(title=title, year=year)   # 創建記錄
        db.session.add(movie)                   # 添加到數據庫會話
        db.session.commit()                     # 提交數據庫會話
        flash('Item created.')                  # 顯示成功創建的提示
        return redirect(url_for('index'))       # 重定向回主頁
    else:
        movies = Movie.query.all()
        return render_template('index.html', movies=movies)

@app.route('/user/<name>')
def user_page(name):
    return f'User: {escape(name)}'

@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def edit(movie_id):
    # get_or_404() 方法，它會返回對應主鍵的記錄，如果沒有找到，則返回 404 錯誤響應。
    movie = Movie.query.get_or_404(movie_id)

    if request.method == 'POST':  # 處理編輯表單的提交請求
        title = request.form['title']
        year = request.form['year']

        if not title or not year or len(year) != 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id))  # 重定向回對應的編輯頁面

        movie.title = title  # 更新標題
        movie.year = year  # 更新年份
        db.session.commit()  # 提交數據庫會話
        flash('Item updated.')
        return redirect(url_for('index'))  # 重定向回主頁
    
    else:
        return render_template('edit.html', movie=movie)  # 傳入被編輯的電影記錄
    
@app.route('/movie/delete/<int:movie_id>', methods=['POST'])  # 限定只接受 POST 請求
@login_required
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)  # 獲取電影記錄
    db.session.delete(movie)  # 刪除對應的記錄
    db.session.commit()  # 提交數據庫會話
    flash('Item deleted.')
    return redirect(url_for('index'))  # 重定向回主頁

@app.route('/login', methods=['GET', 'POST'])
def login():
    # POST
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))

        user = User.query.first()
        # 驗證用戶名和密碼是否一致
        if username == user.username and user.validate_password(password):
            login_user(user)  # 登入用戶
            flash('Login success.')
            return redirect(url_for('index'))  # 重定向到主頁

        flash('Invalid username or password.')  # 如果驗證失敗，顯示錯誤消息
        return redirect(url_for('login'))  # 重定向回登錄頁面
    
    # GET
    else:
        return render_template('login.html')
    
@app.route('/logout')
# @login_required 用於視圖保護：在 Web 程序中，有些頁面或 URL 不允許未登錄的用戶訪問，而頁面上有些內容則需要對未登陸的用戶隱藏，這就是認證保護。
@login_required  
def logout():
    logout_user()  # 登出用戶
    flash('Goodbye.')
    return redirect(url_for('index'))  # 重定向回首頁

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']

        if not name or len(name) > 20:
            flash('Invalid input.')
            return redirect(url_for('settings'))

        current_user.name = name
        # current_user 會返回當前登錄用戶的數據庫記錄對象
        # 等同於下面的用法
        # user = User.query.first()
        # user.name = name
        db.session.commit()
        flash('Settings updated.')
        return redirect(url_for('index'))

    return render_template('settings.html')