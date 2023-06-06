import os
import sys

import click
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from markupsafe import escape

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
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':  # 判斷是否是 POST 請求
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
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)  # 獲取電影記錄
    db.session.delete(movie)  # 刪除對應的記錄
    db.session.commit()  # 提交數據庫會話
    flash('Item deleted.')
    return redirect(url_for('index'))  # 重定向回主頁