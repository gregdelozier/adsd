from flask import Flask, render_template, request, redirect, url_for
import dataset

# Connect to the SQLite database using dataset
db = dataset.connect('sqlite:///pets.db')

app = Flask(__name__)

# List of pets, showing related kind information
@app.route("/")
@app.route("/list")
def get_list():
    # Use dataset to fetch all pets and join kinds
    pets_table = db['pets']
    kinds_table = db['kind']
    
    pets = pets_table.all()
    pet_list = []
    
    # Create a list of pets with kind information by manually joining
    for pet in pets:
        kind = kinds_table.find_one(id=pet['kind_id'])
        pet_list.append({
            'id': pet['id'],
            'name': pet['name'],
            'age': pet['age'],
            'owner': pet['owner'],
            'kind_name': kind['kind_name'],
            'food': kind['food'],
            'noise': kind['noise']
        })
    
    return render_template("list.html", pets=pet_list)

# Create a new pet with a dropdown to select kind
@app.route("/create", methods=['GET', 'POST'])
def get_post_create():
    kinds_table = db['kind']
    
    if request.method == 'GET':
        kinds = kinds_table.all()  # Get all kinds
        return render_template("create.html", kinds=kinds)
    
    if request.method == 'POST':
        data = dict(request.form)
        pets_table = db['pets']
        pets_table.insert({
            'name': data['name'],
            'age': int(data['age']),
            'owner': data['owner'],
            'kind_id': int(data['kind_id'])
        })
        return redirect(url_for('get_list'))

# Update an existing pet, allows kind to be changed
@app.route("/update/<id>", methods=['GET', 'POST'])
def get_update(id):
    pets_table = db['pets']
    kinds_table = db['kind']
    
    pet = pets_table.find_one(id=id)
    if not pet:
        return "Pet not found"
    
    if request.method == 'GET':
        kinds = kinds_table.all()
        return render_template("update.html", pet=pet, kinds=kinds)
    
    if request.method == 'POST':
        data = dict(request.form)
        pets_table.update({
            'id': id,
            'name': data['name'],
            'age': int(data['age']),
            'owner': data['owner'],
            'kind_id': int(data['kind_id'])
        }, ['id'])
        return redirect(url_for('get_list'))

# Delete a pet
@app.route("/delete/<id>")
def get_delete(id):
    pets_table = db['pets']
    pets_table.delete(id=id)
    return redirect(url_for('get_list'))

# List of kinds
@app.route("/kind/list")
def list_kinds():
    kinds_table = db['kind']
    kinds = kinds_table.all()
    return render_template("kind_list.html", kinds=kinds)

# Create a new kind
@app.route("/kind/create", methods=['GET', 'POST'])
def create_kind():
    kinds_table = db['kind']
    
    if request.method == 'POST':
        data = dict(request.form)
        kinds_table.insert({
            'kind_name': data['kind_name'],
            'food': data['food'],
            'noise': data['noise']
        })
        return redirect(url_for('list_kinds'))
    
    return render_template("kind_create.html")

# Update an existing kind
@app.route("/kind/update/<id>", methods=['GET', 'POST'])
def update_kind(id):
    kinds_table = db['kind']
    kind = kinds_table.find_one(id=id)
    
    if not kind:
        return "Kind not found"
    
    if request.method == 'POST':
        data = dict(request.form)
        kinds_table.update({
            'id': id,
            'kind_name': data['kind_name'],
            'food': data['food'],
            'noise': data['noise']
        }, ['id'])
        return redirect(url_for('list_kinds'))
    
    return render_template("kind_update.html", kind=kind)

# Delete a kind, with integrity error handling
@app.route("/kind/delete/<id>")
def delete_kind(id):
    kinds_table = db['kind']
    pets_table = db['pets']
    
    if pets_table.find_one(kind_id=id):
        kinds = kinds_table.all()
        error_message = "Cannot delete kind as it is associated with pets. Please delete the pets first."
        return render_template("kind_list.html", kinds=kinds, error_message=error_message)
    
    kinds_table.delete(id=id)
    return redirect(url_for('list_kinds'))

if __name__ == "__main__":
    app.run(debug=True)
