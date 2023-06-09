import os
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


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

# Flask-Login 提供了一個 current_user 變量，注冊這個函數的目的是，當程序運行後，
# 如果用戶已登錄， current_user 變量的值會是當前用戶的用戶模型類記錄。
@login_manager.user_loader
def load_user(user_id):  # 創建用戶加載回調函數，接受用戶 ID 作為參數
    from watchlist.models import User
    user = User.query.get(int(user_id))  # 用 ID 作為 User 模型的主鍵查詢對應的用戶
    return user  # 返回用戶對象

# 如果未登錄的用戶訪問 @login_required 對應的 URL，Flask-Login 會把用戶重定向到登錄頁面，並顯示一個錯誤提示。
# 為了讓這個重定向操作正確執行，我們還需要把 login_manager.login_view 的值設為我們程序的登錄視圖端點（函數名）
login_manager.login_view = 'login'

@app.context_processor
def inject_user():
    from watchlist.models import User
    user = User.query.first()
    return dict(user=user)

from watchlist import views, errors, commands