import sqlite3
from pprint import pprint

connection = sqlite3.connect("pets.db", check_same_thread=False)
connection.execute("PRAGMA foreign_keys = 1")
connection.row_factory = sqlite3.Row  # Set row factory to return dictionaries

def retrieve_pets():
    cursor = connection.cursor()
    cursor.execute("""
        SELECT pets.id, pets.name, pets.age, pets.owner, kind.kind_name, kind.food, kind.noise 
        FROM pets 
        JOIN kind ON pets.kind_id = kind.id
    """)
    pets = cursor.fetchall()
    # Convert rows to list of dictionaries
    pets = [dict(pet) for pet in pets]
    for pet in pets:
        pet["id"] = str(pet["id"])
    return pets

def test_retrieve_pets():
    print("test retrieve_pets")
    pets = retrieve_pets()
    assert type(pets) is list
    assert type(pets[0]) is dict
    assert pets[0] == {'id': '1', 'name': 'Suzy', 'age': 3, 'owner': 'Greg', 'kind_name': 'Dog', 'food': 'Dog food', 'noise': 'Bark'}

def retrieve_pet(id):
    cursor = connection.cursor()
    id = int(id)
    cursor.execute("SELECT * FROM pets WHERE id=?", (id,))
    pet = dict(cursor.fetchone())
    pet["id"] = str(pet["id"])
    pet["kind_id"] = str(pet["kind_id"])
    return pet

def test_retrieve_pet():
    print("test retrieve_pet")
    pet = retrieve_pet("1")
    assert pet == {'id': '1', 'name': 'Suzy', 'age': 3, 'kind_id': "1", 'owner': 'Greg'}    

def create_pet(data):
    cursor = connection.cursor()
    cursor.execute("""
            INSERT INTO pets (name, age, kind_id, owner) 
            VALUES (?, ?, ?, ?)
        """, (data["name"], data["age"], int(data["kind_id"]), data["owner"]))
    connection.commit()

def delete_pet(id):
    cursor = connection.cursor()
    id = int(id)
    cursor.execute("DELETE FROM pets WHERE id = ?", (id,))
    connection.commit()

def test_create_and_delete_pet():
    print("test create_and_delete_pet")
    pets = retrieve_pets()
    for pet in pets:
        if pet["name"] == "gamma":
            delete_pet(pet["id"])
    data = {
        "name":"gamma",
        "age":12,
        "kind_id":"1",
        "owner":"delta"
    }
    create_pet(data)
    pets = retrieve_pets()
    found = False
    for pet in pets:
        if pet["name"] == "gamma" and pet["owner"] == "delta":
            assert pet["age"] == 12
            assert pet["kind_name"] == "Dog"
            found = True
            id = pet["id"]
    assert found
    delete_pet(id)
    pets = retrieve_pets()
    found = False
    for pet in pets:
        if pet["name"] == "gamma" and pet["owner"] == "delta":
            found = True
    assert not found

def update_pet(id, data):
    cursor = connection.cursor()
    id = int(id)
    cursor.execute("""
            UPDATE pets 
            SET name=?, age=?, kind_id=?, owner=? 
            WHERE id=?
        """, (data["name"], data["age"], int(data["kind_id"]), data["owner"], id))
    connection.commit()

def test_update_pet():
    print("test update_pet")
    pet = retrieve_pet(1)
    data = {
        "name":"gamma",
        "age":12,
        "kind_id":"1",
        "owner":"delta"
    }
    update_pet(1, data)
    pet = retrieve_pet("1")
    assert pet == {'id': '1', 'name': 'gamma', 'age': 12, 'kind_id': "1", 'owner': 'delta'}    

    data = {
        "name":"Suzy",
        "age":3,
        "kind_id":1,
        "owner":"Greg"
    }
    update_pet(1, data)
    pet = retrieve_pet("1")
    assert pet == {'id': '1', 'name': 'Suzy', 'age': 3, 'kind_id': "1", 'owner': 'Greg'}    


def retrieve_kinds():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM kind")
    kinds = cursor.fetchall()
    kinds = [dict(kind) for kind in kinds]
    for kind in kinds:
        kind["id"] = str(kind["id"])
    return kinds

def test_retrieve_kinds():
    print('test retrieve_kinds')
    kinds = retrieve_kinds()
    assert type(kinds) is list
    assert type(kinds[0]) is dict
    assert kinds[0] == {'id': '1', 'kind_name': 'Dog', 'food': 'Dog food', 'noise': 'Bark'}

def retrieve_kind(id):
    cursor = connection.cursor()
    id = int(id)
    cursor.execute("SELECT * FROM kind WHERE id=?", (id,))
    kind = dict(cursor.fetchone())
    kind["id"] = str(kind["id"])
    return kind

def test_retrieve_kind():
    print('test retrieve_kind')
    kind = retrieve_kind(1)
    assert kind == {'id': '1', 'kind_name': 'Dog', 'food': 'Dog food', 'noise': 'Bark'}

def create_kind(data):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO kind (kind_name, food, noise) VALUES (?, ?, ?)", 
                       (data["kind_name"], data["food"], data["noise"]))
    connection.commit()

def delete_kind(id):
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM kind WHERE id = ?", (id,))
        connection.commit()
        return None
    except sqlite3.IntegrityError:
        return "Cannot delete kind as it is associated with pets. Please delete the pets first."

def test_create_and_delete_kind():
    print("test create_and_delete_kind")
    data = {
        "kind_name":"bunny",
        "food":"carrot",
        "noise":"hophop"
    }
    create_kind(data)
    kinds = retrieve_kinds()
    found = False
    for kind in kinds:
        if kind["kind_name"] == "bunny" and kind["food"] == "carrot" :
            found = True
            kind_id = kind["id"]
    assert found
    delete_kind(kind_id)
    kinds = retrieve_kinds()
    found = False
    for kind in kinds:
        if kind["kind_name"] == "bunny" and kind["food"] == "carrot" :
            found = True
            kind_id = kind["id"]
    assert not found

def update_kind(id, data):
    cursor = connection.cursor()
    id = int(id)
    cursor.execute("""
        UPDATE kind 
        SET kind_name=?, food=?, noise=? 
        WHERE id=?
    """, (data["kind_name"], data["food"], data["noise"], id))
    connection.commit()

def test_update_kind():
    print("test update_kind")
    pet = retrieve_kind("1")
    data = {
        "kind_name":"puppy",
        "food":"Puppy chow",
        "noise":"Yip"
    }
    update_kind("1", data)
    kind = retrieve_kind("1")
    assert kind == {'id': '1', 'kind_name': 'puppy', 'food': 'Puppy chow', 'noise': 'Yip'}

    data = {
        "kind_name":"Dog",
        "food":"Dog food",
        "noise":"Bark"
    }
    update_kind("1", data)
    kind = retrieve_kind("1")
    assert kind == {'id': '1', 'kind_name': 'Dog', 'food': 'Dog food', 'noise': 'Bark'}


if __name__ == "__main__":
    test_retrieve_pets()
    test_retrieve_pet()
    test_create_and_delete_pet()
    test_update_pet()
    test_retrieve_kinds()
    test_retrieve_kind()
    test_create_and_delete_kind()
    test_update_kind()
    print("done.")

