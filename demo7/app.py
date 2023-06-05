from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
 
db = SQLAlchemy()
 
app = Flask(__name__)

# windows 下使用三個反斜線(///)，後面再接絕對路徑
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///C:/Users/user/Documents/SQLite/test.db"
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "pool_pre_ping": True,
    "pool_recycle": 300,
    'pool_timeout': 900,
    'pool_size': 10,
    'max_overflow': 5,
}

# 是否將 SQL 指令印出?
app.config['SQLALCHEMY_ECHO'] = True

# 初始化
db.init_app(app)

# 模型( model )定義
class Product(db.Model):
    __tablename__ = 'product'
    pid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    img = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    state = db.Column(db.String(10), nullable=False)
    insert_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, onupdate=datetime.now, default=datetime.now)
 
    def __init__(self, name, price, img, description, state):
        self.name = name
        self.price = price
        self.img = img
        self.description = description
        self.state = state

@app.route('/')
def index():
    db.create_all()
    # Add List data
    p1 = Product('Isacc', 5555, 'https://picsum.photos/id/1048/1200/600', '', '')
    p2 = Product('Dennis', 9999,'https://picsum.photos/id/1049/1200/600', '', '')
    p3 = Product('Joey', 7777, 'https://picsum.photos/id/1033/1200/600', '', '')
    p4 = Product('Fergus', 6666,'https://picsum.photos/id/1041/1200/600', '', '')
    p6 = Product('Jerry', 4444, 'https://picsum.photos/id/1044/1200/600', '', '')
    p = [p1, p2, p3, p4, p6]
    
    db.session.add_all(p)
    db.session.commit()
    return 'ok'