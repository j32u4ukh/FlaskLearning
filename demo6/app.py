from flask import Flask
from flask import url_for, redirect, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello world'
    # return render_template('abc.html')

@app.route('/user/<username>')
def username(username):
    return f'I am {username}.'

@app.route('/para/<user>')
def para(user):
    return render_template('abc.html', user_template=user)

@app.route('/age/<int:age>')
def userage(age):
    return 'I am ' + str(age) + ' years old.'

@app.route('/a')
def url_for_a():
    return 'here is /a'

@app.route('/b')
def b():
    #  所得結果為'/a'
    route = url_for('url_for_a')
    #  會將使用者引導到'/a'這個路由
    return redirect(route)