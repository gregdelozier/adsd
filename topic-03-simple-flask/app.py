from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
connection = sqlite3.connect("pets.db",check_same_thread=False)


@app.route("/hello")
def get_hello():
    return "<p>Hello there, World!</p>"

@app.route("/")
@app.route("/list")
def get_list():
    cursor = connection.cursor()
    cursor.execute("select * from pets")
    rows = cursor.fetchall()
    rows = [list(row) for row in rows]    
    print(rows)
    return render_template("list.html", prof={"name":"Dr. D", "class":"ADSD"}, rows=rows)   

@app.route("/create", methods = ['GET', 'POST'])
def get_post_create():
    if request.method == "GET":
        return render_template("create.html")
    if request.method == "POST":
        data = dict(request.form)
        try:
            data["age"] = int(data["age"])
        except:
            data["age"] = 0
        print(data)
        cursor = connection.cursor()
        cursor.execute(f"""insert into pets (name, age, type, owner) values ('{data["name"]}', {data["age"]}, '{data["type"]}', '{data["owner"]}')""")
        connection.commit()
        return redirect(url_for('get_list'))

@app.route("/update/<id>", methods = ['GET'])
def get_update(id):
    cursor = connection.cursor()
    cursor.execute(f"select * from pets where id={id}")
    rows = cursor.fetchall()
    try:
        (id, name, xtype, age, owner) = rows[0]
        data = {
            "id":id,
            "name":name,
            "type":xtype,
            "age":age,
            "owner":owner
        }
        print([data])
    except:
        return "Data not found."
    return render_template("update.html", data=data)

@app.route("/update/<id>", methods = ['POST'])
def post_update(id):
    data = dict(request.form)
    try:
        data["age"] = int(data["age"])
    except:
        data["age"] = 0
    cursor = connection.cursor()
    cursor.execute("""update pets set name=?, age=?, type=?, owner=? where id=?""", (data["name"], data["age"], data["type"],data["owner"],id))
    connection.commit()
    return redirect(url_for('get_list'))

@app.route("/delete/<id>")
def get_delete(id):
    cursor = connection.cursor()
    cursor.execute("""delete from pets where id = ?""",(id,))
    connection.commit()
    return redirect(url_for('get_list'))

@app.route("/goodbye")
def get_goodbye():
    return "<p>Goodbye, then! Have a nice day!</p>"