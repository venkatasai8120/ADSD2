from mongita import MongitaClientDisk
from bson.objectid import ObjectId

client = MongitaClientDisk()
pets_db = client.pets_db

# --------------------------------------
# PET FUNCTIONS
# --------------------------------------

def retrieve_pets():
    pets_collection = pets_db.pets_collection
    kind_collection = pets_db.kind_collection

    pets = list(pets_collection.find())

    for pet in pets:
        pet["id"] = str(pet["_id"])
        del pet["_id"]

        # ensure color exists
        pet["color"] = pet.get("color", "")

        kind = kind_collection.find_one({"_id": pet["kind_id"]})
        for tag in ["kind_name", "noise", "food"]:
            pet[tag] = kind[tag]

        del pet["kind_id"]

    return pets


def retrieve_pet(id):
    pets_collection = pets_db.pets_collection
    pet = pets_collection.find_one({"_id": ObjectId(id)})

    pet["id"] = str(pet["_id"])
    del pet["_id"]

    # ensure color exists
    pet["color"] = pet.get("color", "")

    return pet


def create_pet(data):
    pets_collection = pets_db.pets_collection

    data["kind_id"] = ObjectId(data["kind_id"])
    data["color"] = data.get("color", "")

    pets_collection.insert_one(data)


def update_pet(id, data):
    pets_collection = pets_db.pets_collection

    data["kind_id"] = ObjectId(data["kind_id"])
    data["color"] = data.get("color", "")

    pets_collection.update_one({"_id": ObjectId(id)}, {"$set": data})


def delete_pet(id):
    pets_collection = pets_db.pets_collection
    pets_collection.delete_one({"_id": ObjectId(id)})


# --------------------------------------
# KIND FUNCTIONS
# --------------------------------------

def retrieve_kinds():
    kinds = list(pets_db.kind_collection.find())
    for kind in kinds:
        kind["id"] = str(kind["_id"])
    return kinds


def create_kind(data):
    pets_db.kind_collection.insert_one(data)


def delete_kind(id):
    try:
        pets_db.kind_collection.delete_one({"_id": ObjectId(id)})
        return None
    except Exception as e:
        return str(e)


def retrieve_kind(id):
    kind = pets_db.kind_collection.find_one({"_id": ObjectId(id)})
    kind["id"] = str(kind["_id"])
    del kind["_id"]
    return kind


def update_kind(id, data):
    pets_db.kind_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
