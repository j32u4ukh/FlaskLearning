from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from watchlist import db


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
