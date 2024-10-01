from flask import Flask, render_template, request, redirect, url_for
from peewee import *

# Initialize database connection
db = SqliteDatabase('pets.db')

# Define models
class Kind(Model):
    kind_name = CharField()
    food = CharField()
    noise = CharField()

    class Meta:
        database = db

class Pet(Model):
    name = CharField()
    age = IntegerField()
    owner = CharField()
    kind = ForeignKeyField(Kind, backref='pets')

    class Meta:
        database = db

# Create tables if they don't exist
db.connect()
db.create_tables([Pet, Kind])

app = Flask(__name__)

# List of pets, showing related kind information
@app.route("/")
@app.route("/list")
def get_list():
    pets = Pet.select().join(Kind)
    return render_template("list.html", pets=pets)

# Create a new pet with a dropdown to select kind
@app.route("/create", methods=['GET', 'POST'])
def get_post_create():
    if request.method == 'GET':
        kinds = Kind.select()
        return render_template("create.html", kinds=kinds)
    
    if request.method == 'POST':
        data = dict(request.form)
        kind = Kind.get_by_id(data["kind_id"])
        Pet.create(name=data["name"], age=int(data["age"]), owner=data["owner"], kind=kind)
        return redirect(url_for('get_list'))

# Update an existing pet, allows kind to be changed
@app.route("/update/<id>", methods=['GET', 'POST'])
def get_update(id):
    pet = Pet.get_or_none(Pet.id == id)
    if not pet:
        return "Pet not found"
    
    if request.method == 'GET':
        kinds = Kind.select()
        return render_template("update.html", pet=pet, kinds=kinds)
    
    if request.method == 'POST':
        data = dict(request.form)
        kind = Kind.get_by_id(data["kind_id"])
        Pet.update({Pet.name: data["name"],
                    Pet.age: int(data["age"]),
                    Pet.owner: data["owner"],
                    Pet.kind: kind}).where(Pet.id == id).execute()
        return redirect(url_for('get_list'))

# Delete a pet
@app.route("/delete/<id>")
def get_delete(id):
    Pet.delete_by_id(id)
    return redirect(url_for('get_list'))

# List of kinds
@app.route("/kind/list")
def list_kinds():
    kinds = Kind.select()
    return render_template("kind_list.html", kinds=kinds)

# Create a new kind
@app.route("/kind/create", methods=['GET', 'POST'])
def create_kind():
    if request.method == 'POST':
        data = dict(request.form)
        Kind.create(kind_name=data["kind_name"], food=data["food"], noise=data["noise"])
        return redirect(url_for('list_kinds'))
    return render_template("kind_create.html")

# Update an existing kind
@app.route("/kind/update/<id>", methods=['GET', 'POST'])
def update_kind(id):
    kind = Kind.get_or_none(Kind.id == id)
    if not kind:
        return "Kind not found"
    
    if request.method == 'POST':
        data = dict(request.form)
        Kind.update({Kind.kind_name: data["kind_name"],
                     Kind.food: data["food"],
                     Kind.noise: data["noise"]}).where(Kind.id == id).execute()
        return redirect(url_for('list_kinds'))
    
    return render_template("kind_update.html", kind=kind)

# Delete a kind, with integrity error handling
@app.route("/kind/delete/<id>")
def delete_kind(id):
    try:
        Kind.delete_by_id(id)
    except IntegrityError:
        kinds = Kind.select()
        error_message = "Cannot delete kind as it is associated with pets. Please delete the pets first."
        return render_template("kind_list.html", kinds=kinds, error_message=error_message)
    return redirect(url_for('list_kinds'))

if __name__ == "__main__":
    app.run(debug=True)
