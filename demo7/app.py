from flask_sqlalchemy import SQLAlchemy
from flask import Flask
 
db = SQLAlchemy()
 
app = Flask(__name__)

# windows 下使用三個反斜線(///)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///C:/Users/user/Documents/SQLite/test.db"
 
db.init_app(app)
 
@app.route('/create_db')
def index():
    db.create_all()
    return 'ok'
