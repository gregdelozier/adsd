from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
connection = sqlite3.connect("pets.db", check_same_thread=False)
connection.execute("PRAGMA foreign_keys = 1")

# List of pets, showing related kind information
@app.route("/")
@app.route("/list")
def get_list():
    cursor = connection.cursor()
    cursor.execute("""
        SELECT pets.id, pets.name, pets.age, pets.owner, kind.kind_name, kind.food, kind.noise 
        FROM pets 
        JOIN kind ON pets.kind_id = kind.id
    """)
    rows = cursor.fetchall()
    return render_template("list.html", rows=rows)

# Create a new pet with a dropdown to select kind
@app.route("/create", methods=['GET', 'POST'])
def get_post_create():
    cursor = connection.cursor()
    
    if request.method == 'GET':
        cursor.execute("SELECT id, kind_name FROM kind")
        kinds = cursor.fetchall()
        return render_template("create.html", kinds=kinds)
    
    if request.method == 'POST':
        data = dict(request.form)
        try:
            data["age"] = int(data["age"])
        except:
            data["age"] = 0
        
        cursor.execute("""
            INSERT INTO pets (name, age, kind_id, owner) 
            VALUES (?, ?, ?, ?)
        """, (data["name"], data["age"], data["kind_id"], data["owner"]))
        connection.commit()
        return redirect(url_for('get_list'))

# Update an existing pet, allows kind to be changed
@app.route("/update/<id>", methods=['GET', 'POST'])
def get_update(id):
    cursor = connection.cursor()
    
    if request.method == 'GET':
        cursor.execute("SELECT * FROM pets WHERE id=?", (id,))
        pet = cursor.fetchone()
        cursor.execute("SELECT id, kind_name FROM kind")
        kinds = cursor.fetchall()
        
        if pet is None:
            return "Pet not found"
        
        return render_template("update.html", pet=pet, kinds=kinds)
    
    if request.method == 'POST':
        data = dict(request.form)
        try:
            data["age"] = int(data["age"])
        except:
            data["age"] = 0
        
        cursor.execute("""
            UPDATE pets 
            SET name=?, age=?, kind_id=?, owner=? 
            WHERE id=?
        """, (data["name"], data["age"], data["kind_id"], data["owner"], id))
        connection.commit()
        return redirect(url_for('get_list'))

# Delete a pet
@app.route("/delete/<id>")
def get_delete(id):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM pets WHERE id = ?", (id,))
    connection.commit()
    return redirect(url_for('get_list'))

# List of kinds
@app.route("/kind/list")
def list_kinds():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM kind")
    kinds = cursor.fetchall()
    return render_template("kind_list.html", kinds=kinds)

# Create a new kind
@app.route("/kind/create", methods=['GET', 'POST'])
def create_kind():
    if request.method == 'POST':
        data = dict(request.form)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO kind (kind_name, food, noise) VALUES (?, ?, ?)", 
                       (data["kind_name"], data["food"], data["noise"]))
        connection.commit()
        return redirect(url_for('list_kinds'))
    return render_template("kind_create.html")

# Update an existing kind
@app.route("/kind/update/<id>", methods=['GET', 'POST'])
def update_kind(id):
    cursor = connection.cursor()
    
    if request.method == 'POST':
        data = dict(request.form)
        cursor.execute("""
            UPDATE kind 
            SET kind_name=?, food=?, noise=? 
            WHERE id=?
        """, (data["kind_name"], data["food"], data["noise"], id))
        connection.commit()
        return redirect(url_for('list_kinds'))
    
    cursor.execute("SELECT * FROM kind WHERE id=?", (id,))
    kind = cursor.fetchone()
    if kind is None:
        return "Kind not found"
    return render_template("kind_update.html", kind=kind)

# Delete a kind, with integrity error handling
@app.route("/kind/delete/<id>")
def delete_kind(id):
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM kind WHERE id = ?", (id,))
        connection.commit()
        return redirect(url_for('list_kinds'))
    except sqlite3.IntegrityError:
        cursor.execute("SELECT * FROM kind")
        kinds = cursor.fetchall()
        error_message = "Cannot delete kind as it is associated with pets. Please delete the pets first."
        return render_template("kind_list.html", kinds=kinds, error_message=error_message)

if __name__ == "__main__":
    app.run(debug=True)
