import flask
app = flask.Flask(__name__)

@app.route("/")
@app.route("/hello")
def hello():
    print(flask.url_for("hello"))
    return "Hello, World!"

if __name__ == '__main__':
    app.run()