from flask import Flask, jsonify, request
from flask_jwt_extended import (JWTManager, create_access_token,
                                jwt_required)

app = Flask(__name__)
jwt = JWTManager()
 
# 設定 JWT 密鑰
app.config['JWT_SECRET_KEY'] = 'this-should-be-change'
jwt.init_app(app)

@app.route('/login', methods=['POST'])
def login(): 
    username = request.json.get('username', None) 
    password = request.json.get('password', None) 
 
    if username != 'test' or password != 'test': 
        return jsonify({"msg": "Bad username or password"}), 401
 
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

@app.route('/protected', methods=['GET', 'POST'])
@jwt_required
def protected(): 
    return jsonify(msg='ok')
