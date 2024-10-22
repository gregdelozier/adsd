from flask import Flask, render_template, request, redirect, url_for
import database

app = Flask(__name__)

# List of pets, showing related kind information
@app.route("/")
@app.route("/list")
def get_list():
    rows = database.retrieve_list()
    return render_template("list.html", rows=rows)

# Create a new pet with a dropdown to select kind
@app.route("/create", methods=['GET', 'POST'])
def get_post_create():

    if request.method == 'GET':
        kinds = database.retrieve_kinds()
        return render_template("create.html", kinds=kinds)
    
    if request.method == 'POST':
        data = dict(request.form)
        try:
            data["age"] = int(data["age"])
        except:
            data["age"] = 0
        database.create_pet(data)
        return redirect(url_for('get_list'))

# Update an existing pet, allows kind to be changed
@app.route("/update/<id>", methods=['GET', 'POST'])
def get_update(id):

    if request.method == 'GET':
        kinds = database.retrieve_kinds()
        pet = database.retrieve_pet(id)
        
        if pet is None:
            return "Pet not found"
        
        return render_template("update.html", pet=pet, kinds=kinds)
    
    if request.method == 'POST':
        data = dict(request.form)
        try:
            data["age"] = int(data["age"])
        except:
            data["age"] = 0
        
        database.update_pet(id, data)
        return redirect(url_for('get_list'))

# Delete a pet
@app.route("/delete/<id>")
def get_delete(id):
    database.delete_pet(id)
    return redirect(url_for('get_list'))

import sqlite3
from pprint import pprint

connection = sqlite3.connect("pets.db", check_same_thread=False)
connection.execute("PRAGMA foreign_keys = 1")

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
