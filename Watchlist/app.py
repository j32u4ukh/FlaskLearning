import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from markupsafe import escape
import sys
import click

app = Flask(__name__)
WIN = sys.platform.startswith('win')
if WIN:  # 如果是 Windows 系統，使用三個斜線
    prefix = 'sqlite:///'
else:  # 否則使用四個斜線
    prefix = 'sqlite:////'
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 關閉對模型修改的監控
db = SQLAlchemy(app)  # 初始化擴展，傳入程序實例 app

@app.cli.command()  # 注冊為命令，可以傳入 name 參數來自定義命令
@click.option('--drop', is_flag=True, help='Create after drop.')  # 設置選項
def initdb(drop):
    """Initialize the database."""
    if drop:  # 判斷是否輸入了選項
        click.echo("Drop database.")
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')  # 輸出提示信息

@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()

    # 全局的兩個變量移動到這個函數內
    name = 'Henry Li'
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

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')

class User(db.Model):  # 表名將會是 user（自動生成，小寫處理）
    id = db.Column(db.Integer, primary_key=True)  # 主鍵
    name = db.Column(db.String(20))  # 名字


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
@app.route('/')
def index():
    movies = Movie.query.all()  # 讀取所有電影記錄
    return render_template('index.html', movies=movies)

@app.route('/user/<name>')
def user_page(name):
    return f'User: {escape(name)}'