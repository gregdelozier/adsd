from pprint import pprint
import mongita

from mongita import MongitaClientDisk
from bson.objectid import ObjectId

client = MongitaClientDisk()

pets_db = client.pets_db


def retrieve_pets():
    pet_collection = pets_db.pet_collection
    kind_collection = pets_db.kind_collection
    pets = list(pet_collection.find())
    for pet in pets:
        pet["id"] = str(pet["_id"])
        del pet["_id"]
        kind = kind_collection.find_one({"_id":pet["kind_id"]})
        for tag in ["kind_name","noise","food"]:
            pet[tag] = kind[tag]
        del pet["kind_id"]
        # pet["_id"] = ObjectId(pet["id"])
    return pets

def test_retrieve_pets():
    print("test retrieve_pets")
    pets = retrieve_pets()
    assert type(pets) is list
    assert type(pets[0]) is dict
    assert type(pets[0]['id']) is str
    pets[0]['id'] = '1'
    assert pets[0] == {'id': '1', 'name': 'Suzy', 'age': 3, 'owner': 'Greg', 'kind_name': 'Dog', 'food': 'Dog food', 'noise': 'Bark'}

def retrieve_pet(id):
    pet_collection = pets_db.pet_collection
    id = ObjectId(id)
    pet = pet_collection.find_one({"_id":id})
    pet["id"] = str(pet["_id"])
    del pet["_id"]
    return pet

def test_retrieve_pet():
    print("test retrieve_pet")
    pets = retrieve_pets()
    id = pets[0]["id"]
    pet = retrieve_pet(id)
    del pet["kind_id"]
    assert pet == {'id': id, 'name': 'Suzy', 'age': 3,  'owner': 'Greg'}    

def create_pet(data):
    pet_collection = pets_db.pet_collection
    data["kind_id"] = ObjectId(data["kind_id"])
    pet_collection.insert_one(data)

def delete_pet(id):
    pet_collection = pets_db.pet_collection
    pet_collection.delete_one({"_id":ObjectId(id)})

def test_create_and_delete_pet():
    kind_collection = pets_db.kind_collection
    kind = kind_collection.find_one({"kind_name":"Dog"})
    example_kind_id = str(kind["_id"])
    print("test create_and_delete_pet")
    pets = retrieve_pets()
    for pet in pets:
        if pet["name"] == "gamma":
            delete_pet(pet["id"])
    data = {
        "name":"gamma",
        "age":12,
        "kind_id":example_kind_id,
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
    pet_collection = pets_db.pet_collection
    data["kind_id"] = ObjectId(data["kind_id"])
    pet_collection.update_one({"_id":ObjectId(id)},{"$set":data})

def test_update_pet():
    print("test update_pet")
    pet_collection = pets_db.pet_collection
    # find the reference id
    pet_saved = pet_collection.find_one()
    id = str(pet_saved["_id"])

    # modify the record with the same kind_id
    kind_id = pet_saved["kind_id"]
    data = {
        "name":"gamma",
        "age":12,
        "kind_id": kind_id,
        "owner":"delta"
    }
    update_pet(id, data)

    # check that the update happened
    pet = retrieve_pet(id)
    assert pet["name"] == "gamma"
    assert pet["owner"] == "delta"

    # restore the original data and verify
    update_pet(id, pet_saved)
    pet = retrieve_pet(id)
    assert pet["name"] == "Suzy"
    assert pet["owner"] == "Greg"


def retrieve_kinds():
    kind_collection = pets_db.kind_collection
    kinds = list(kind_collection.find())
    for kind in kinds:
        kind["id"] = str(kind["_id"])
    return kinds

def test_retrieve_kinds():
    print('test retrieve_kinds')
    kinds = retrieve_kinds()
    assert type(kinds) is list
    assert type(kinds[0]) is dict
    assert type(kinds[0]["id"]) is str
    del kinds[0]["_id"]
    del kinds[0]["id"]
    assert kinds[0] == {'kind_name': 'Dog', 'food': 'Dog food', 'noise': 'Bark'}

def retrieve_kind(id):
    kind_collection = pets_db.kind_collection
    id = ObjectId(id)
    kind = kind_collection.find_one({"_id":id})
    kind["id"] = str(kind["_id"])
    del kind["_id"]
    return kind

def test_retrieve_kind():
    print('test retrieve_kind')
    kinds = retrieve_kinds()
    id = kinds[0]["id"]
    kind = retrieve_kind(id)
    assert kind == {'id':id, 'kind_name': 'Dog', 'food': 'Dog food', 'noise': 'Bark'}

def create_kind(data):
    kind_collection = pets_db.kind_collection
    kind_collection.insert_one(data)

def delete_kind(id):
    kind_collection = pets_db.kind_collection
    kind_collection.delete_one({"_id":ObjectId(id)})

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
    assert not found

def update_kind(id, data):
    kind_collection = pets_db.kind_collection
    kind_collection.update_one({"_id":ObjectId(id)},{"$set":data})

def test_update_kind():
    kinds = retrieve_kinds()
    id = kinds[0]["id"]
    kind_save = retrieve_kind(id)
    data = {
        "kind_name":"puppy",
        "food":"Puppy chow",
        "noise":"Yip"
    }
    update_kind(id, data)
    kind = retrieve_kind(id)
    assert kind == {'id': id, 'kind_name': 'puppy', 'food': 'Puppy chow', 'noise': 'Yip'}
    update_kind(id, kind_save)
    kind = retrieve_kind(id)
    assert kind == kind_save


def create_sample_database():
    pets_db = client.pets_db
    pets_db.drop_collection("kind_collection")
    kind_collection = pets_db.kind_collection
    kind_collection.insert_many([
        {
            "kind_name":'Dog', 
            "food":'Dog food', 
            "noise":'Bark'
        },
        {
            "kind_name":'Cat', 
            "food":'Cat food', 
            "noise":'Meow'
        },
        {
            "kind_name":'Fish', 
            "food":'Fish flakes', 
            "noise":'Blub'
        }
    ])
    kinds = list(kind_collection.find())
    pets_db.drop_collection("pet_collection")
    pet_collection = pets_db.pet_collection
    pets = [
        {'name':'Suzy', 'age':3, "kind_name":"Dog", 'owner':'Greg'},
        {'name':'Sandy', 'age':2, "kind_name":"Cat", 'owner':'Steve'},
        {'name':'Dorothy', 'age':1, "kind_name":"Dog", 'owner':'Elizabeth'},
        {'name':'Heidi', 'age':4, "kind_name":"Dog",'owner':'David'}
    ]
    for pet in pets:
        for kind in kinds:
            if kind["kind_name"] == pet["kind_name"]:
                pet["kind_id"] = kind["_id"]
        del pet["kind_name"]
        assert "kind_id" in pet.keys()

    pet_collection.insert_many(pets)
    
if __name__ == "__main__":
    create_sample_database()
    test_retrieve_pets()
    test_retrieve_pet()
    test_create_and_delete_pet()
    test_update_pet()
    test_retrieve_kinds()
    test_retrieve_kind()
    test_create_and_delete_kind()
    test_update_kind()
    print("done.")

