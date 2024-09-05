import sqlite3
from flask import Flask, render_template

app = Flask(__name__)
connection = sqlite3.connect("pets.db", check_same_thread=False)

@app.route("/")
@app.route("/hello")
def hello_world():
    return "<p>Hello there, Big World!</p>"

@app.route("/list")
def get_list():
    cursor = connection.cursor()
    cursor.execute("select * from pets")
    rows = cursor.fetchall()

    output = ""
    rows =[list(row) for row in rows]
    print(rows)
    return Flask.render_template("list.html", prof={"name":"Ryan", "class":"ADSD"}, rows=rows)
    
@app.route("/goodbye")
def goodbye():
    return "<p>Goodbye, then! Have a truly nice day!</p>"