from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user

from watchlist import app, db
from watchlist.models import User, Movie

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