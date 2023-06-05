from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
 
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
db = SQLAlchemy(app)

# ==========================================================================================
# 模型( model )定義
# ==========================================================================================
class Product(db.Model):
    __tablename__ = 'product'
    pid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    img = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    state = db.Column(db.String(10), nullable=False)
    insert_time = db.Column(db.DateTime, default=datetime.now, nullable=False)
    update_time = db.Column(db.DateTime, onupdate=datetime.now, default=datetime.now, nullable=False)
 
    db_product_addtocar = db.relationship("AddToCar", backref="product")
 
    def __init__(self, name, price, img, description, state):
        self.name = name
        self.price = price
        self.img = img
        self.description = description
        self.state = state
 
class User(db.Model):
    __tablename__ = 'user'
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(10), nullable=False)
    insert_time = db.Column(db.DateTime, default=datetime.now, nullable=False)
    update_time = db.Column(
        db.DateTime, onupdate=datetime.now, default=datetime.now, nullable=False)
 
    db_user_atc = db.relationship("AddToCar", backref="user")
 
    def __init__(self, name, password, role):
        self.name = name
        self.password = password
        self.role = role
 
class AddToCar(db.Model):
    __tablename__ = 'addtocar'
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    state = db.Column(db.String(5), nullable=False)
    insert_time = db.Column(db.DateTime, default=datetime.now, nullable=False)
    update_time = db.Column(db.DateTime, onupdate=datetime.now, default=datetime.now, nullable=False) 
    uid = db.Column(db.Integer, db.ForeignKey('user.uid'), nullable=False)
    pid = db.Column(db.Integer, db.ForeignKey('product.pid'), nullable=False)
 
    def __init__(self, uid, pid, quantity, state):
        self.uid = uid
        self.pid = pid
        self.quantity = quantity
        self.state = state
# ==========================================================================================

@app.route('/')
def index():
    db.create_all()
    # 查看
    query = AddToCar.query.first()
    print("query.product.name:", query.product.name)  
    print("query.user.name:", query.user.name)  
    return 'ok'