import os
from flask import Flask, render_template, request, jsonify, json

app = Flask(__name__)


@app.route('/data')
def webapi():
    return render_template('data.html')


@app.route('/data/message', methods=['GET'])
def getDataMessage():
    if request.method == "GET":
        file_path = os.path.join(os.path.dirname(__file__), 'static/data/message.json')
        with open(file_path, 'r') as f:
            data = json.load(f)
            # print("text : ", data)
        f.close
        return jsonify(data)  # 直接回傳 data 也可以，都是 json 格式


@app.route('/data/message', methods=['POST'])
def setDataMessage():
    if request.method == "POST":
        data = {
            'appInfo': {
                'id': request.form['app_id'],
                'name': request.form['app_name'],
                'version': request.form['app_version'],
                'author': request.form['app_author'],
                'remark': request.form['app_remark']
            }
        }
        file_path = os.path.join(os.path.dirname(__file__), 'static/data/input.json')
        with open(file_path, 'w') as f:
            json.dump(data, f)
        f.close
        return jsonify(result='OK')


if __name__ == '__main__':
    current_directory = os.getcwd()
    print("當前資料夾：", current_directory)
    app.run()
