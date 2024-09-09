from flask import Flask, render_template
import sqlite3

app = Flask(__name__)
connection = sqlite3.connect("pets.db",check_same_thread=False)

@app.route("/")
@app.route("/hello")
def get_hello():
    return "<p>Hello there, World!</p>"

@app.route("/list")
def get_list():
    cursor = connection.cursor()
    cursor.execute("select * from pets")
    rows = cursor.fetchall()
    rows = [list(row) for row in rows]    
    print(rows)
    return render_template("list.html", prof={"name":"Dr. D", "class":"ADSD"}, rows=rows)   

@app.route("/delete/<id>")
def get_delete(id):
    cursor = connection.cursor()
    cursor.execute("""delete from pets where id = ?""",(id,))
    connection.commit()
    return f"<p>Deleted ID={[id]}!</p>"

@app.route("/goodbye")
def get_goodbye():
    return "<p>Goodbye, then! Have a nice day!</p>"