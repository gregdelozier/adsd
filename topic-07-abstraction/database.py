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
    print("test retrieve_list")
    rows = retrieve_list()
    assert type(rows) is list

def retrieve_kinds():
    cursor = connection.cursor()
    cursor.execute("SELECT id, kind_name FROM kind")
    kinds = list(cursor.fetchall())
    return kinds

def test_retrieve_kinds():
    print("test retrieve_kinds")
    kinds = retrieve_kinds()
    assert kinds == [(1, 'Dog'), (2, 'Cat')]

def retrieve_pet(id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM pets WHERE id=?", (id,))
    pet = cursor.fetchone()
    return pet

def test_retrieve_pet():
    print("test retrieve_pet")
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
    print("test create_and_delete_pet")
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

def retrieve_list_kinds():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM kind")
    kinds = cursor.fetchall()
    return kinds

def test_retrieve_list_kinds():
    kinds = retrieve_list_kinds()
    assert type(kinds) is list
    for kind in kinds:
        assert type(kind[0]) is int
        assert type(kind[1]) is str
        assert type(kind[2]) is str
        assert type(kind[3]) is str

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
    data = {
        "kind_name":"bunny",
        "food":"carrot",
        "noise":"hophop"
    }
    create_kind(data)
    kinds = retrieve_list_kinds()
    found = False
    for kind in kinds:
        kind = list(kind)
        if "bunny" in kind and "carrot" in kind:
            found = True
            id = kind[0]
    assert found
    delete_kind(id)
    kinds = retrieve_kinds()
    found = False
    for kind in kinds:
        kind = list(kind)
        if "bunny" in kind and "carrot" in kind:
            found = True
    assert not found

def retrieve_kind(id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM kind WHERE id=?", (id,))
    kind = cursor.fetchone()
    return kind

def test_retrieve_kind():
    kind = retrieve_kind(1)
    assert kind == (1, 'Dog', 'Dog food', 'Bark')

def update_kind(id, data):
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE kind 
        SET kind_name=?, food=?, noise=? 
        WHERE id=?
    """, (data["kind_name"], data["food"], data["noise"], id))
    connection.commit()

def test_update_kind():
    pet = retrieve_kind(1)
    # (1, 'Dog', 'Dog food', 'Bark')
    data = {
        "kind_name":"puppy",
        "food":"Puppy chow",
        "noise":"Yip"
    }
    update_kind(1, data)
    pet = retrieve_kind(1)
    assert pet == (1, 'puppy', 'Puppy chow', 'Yip')
    data = {
        "kind_name":"Dog",
        "food":"Dog food",
        "noise":"Bark"
    }
    update_kind(1, data)
    pet = retrieve_kind(1)
    assert pet == (1, 'Dog', 'Dog food', 'Bark')


if __name__ == "__main__":
    test_retrieve_list()
    test_retrieve_pet()
    test_retrieve_kinds()
    test_create_and_delete_pet()
    test_update_pet()
    test_retrieve_list_kinds()
    test_create_and_delete_kind()
    test_retrieve_kind()
    test_update_kind()
    print("done.")

