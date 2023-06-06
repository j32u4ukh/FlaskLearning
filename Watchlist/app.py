from flask import Flask
from markupsafe import escape

app = Flask(__name__)

# flask run --debug --reload --debugger
@app.route('/')
def hello():
    return 'Hello'

@app.route('/user/<name>')
def user_page(name):
    return f'User: {escape(name)}'