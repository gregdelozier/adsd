import sqlite3
from pprint import pprint

connection = sqlite3.connect("pets.db", check_same_thread=False)
connection.execute("PRAGMA foreign_keys = 1")

def retrieve_list():
    cursor = connection.cursor()
    cursor.execute("""
        SELECT pets.id, pets.name, pets.age, pets.owner, kind.kind_name, kind.food, kind.noise 
        FROM pets 
        JOIN kind ON pets.kind_id = kind.id
    """)
    rows = cursor.fetchall()
    return rows

def test_retrieve_list():
    rows = retrieve_list()
    assert type(rows) is list

def retrieve_kinds():
    cursor = connection.cursor()
    cursor.execute("SELECT id, kind_name FROM kind")
    kinds = list(cursor.fetchall())
    return kinds

def test_retrieve_kinds():
    kinds = retrieve_kinds()
    assert kinds == [(1, 'Dog'), (2, 'Cat')]

def retrieve_pet(id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM pets WHERE id=?", (id,))
    pet = cursor.fetchone()
    return pet

def test_retrieve_pet():
    pet = retrieve_pet(1)
    assert pet == (1, 'Suzy', 3, 1, 'Greg')

def create_pet(data):
    cursor = connection.cursor()
    cursor.execute("""
            INSERT INTO pets (name, age, kind_id, owner) 
            VALUES (?, ?, ?, ?)
        """, (data["name"], data["age"], data["kind_id"], data["owner"]))
    connection.commit()

def delete_pet(id):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM pets WHERE id = ?", (id,))
    connection.commit()

def test_create_and_delete_pet():
    data = {
        "name":"gamma",
        "age":12,
        "kind_id":1,
        "owner":"delta"
    }
    create_pet(data)
    rows = retrieve_list()
    found = False
    for row in rows:
        row = list(row)
        if "gamma" in row and "delta" in row:
            assert 12 in row
            assert "Dog" in row
            found = True
            id = row[0]
    assert found
    delete_pet(id)
    rows = retrieve_list()
    found = False
    for row in rows:
        row = list(row)
        if "gamma" in row and "delta" in row:
            found = True
    assert not found

def update_pet(id, data):
    cursor = connection.cursor()
    cursor.execute("""
            UPDATE pets 
            SET name=?, age=?, kind_id=?, owner=? 
            WHERE id=?
        """, (data["name"], data["age"], data["kind_id"], data["owner"], id))
    connection.commit()

def test_update_pet():
    pet = retrieve_pet(1)
    data = {
        "name":"gamma",
        "age":12,
        "kind_id":1,
        "owner":"delta"
    }
    update_pet(1, data)
    pet = retrieve_pet(1)
    assert pet == (1, 'gamma', 12, 1, 'delta')
    data = {
        "name":"Suzy",
        "age":3,
        "kind_id":1,
        "owner":"Greg"
    }
    update_pet(1, data)
    pet = retrieve_pet(1)
    assert pet == (1, 'Suzy', 3, 1, 'Greg')


if __name__ == "__main__":
    test_retrieve_list()
    test_retrieve_pet()
    test_retrieve_kinds()
    test_create_and_delete_pet()
    test_update_pet()
    print("done.")

