from flask import Flask

app = Flask(__name__)

@app.route("/")
@app.route("/hello")
def hello_world():
    return "<p>Hello there, Big World!</p>"

@app.route("/goodbye")
def goodbye():
    return "<p>Goodbye, then! Have a truly nice day!</p>"