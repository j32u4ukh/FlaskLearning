from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token, verify_jwt_in_request, get_jwt_identity

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'secret_key'
jwt = JWTManager(app)

@app.route("/access_token")
def access_token():
    # 假設這裡有身份驗證的邏輯，並成功驗證使用者
    user = {
        "id": 1,
        "username": "user123"
    }
    
    token = create_access_token(identity=user["username"])
    return {"access_token": token}

@app.route("/get_jwt", methods=["POST"])
def get_jwt():
    verify_jwt_in_request()    
    token = get_jwt_identity()
    return {"token": token}
