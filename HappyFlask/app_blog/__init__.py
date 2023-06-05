import os

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

#  取得啟動文件資料夾路徑
root = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

#  新版本的部份預設為 None，會有異常，再設置 True 即可。
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

#  設置資料庫為 sqlite3
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' +  os.path.join(root, 'static\\data\\data_register.sqlite')
app.config['SECRET_KEY'] = 'your key'

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

#  很重要，一定要放這邊
from app_blog.author import view