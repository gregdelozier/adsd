from flask import Flask

app = Flask(__name__)

@app.route("/")
@app.route("/hello")
def hello_world():
    return "<p>Hello there, World!</p>"

@app.route("/goodbye")
def goodbye():
    return "<p>Goodbye, then! Have a nice day!</p>"