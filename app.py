from flask import Flask,request
from db import stores,items
import uuid
from flask_smorest import abort

app = Flask(__name__)

## Get all stores
@app.get("/store")
def get_stores():
    return {"stores": list(stores.values())}

## Get all items
@app.get("/items")
def get_all_items():
    return {"items": list(items.values())}

## Create a store
@app.post("/store")
def create_store():
    store_data = request.get_json()
    if "name" not in store_data:
        abort(
            400,
            message="Bad request. Ensure 'name' is included in the JSON payload.",
        )
    for store in stores.values():
        if store_data["name"] == store["name"]:
            abort(400, message=f"Store already exists.")

    store_id = uuid.uuid4().hex
    store = {**store_data, "id": store_id}
    stores[store_id] = store

    return store

## Create a item
@app.post("/item")
def create_item():
    item_data = request.get_json()
    if (
        "price" not in item_data
        or "store_id" not in item_data
        or "name" not in item_data
    ):
        abort(
            400,
            message="Bad request. Ensure 'price', 'store_id', and 'name' are included in the JSON payload.",
        )
    for item in items.values():
        if (
            item_data["name"] == item["name"]
            and item_data["store_id"] == item["store_id"]
        ):
            abort(400, message=f"Item already exists.")

    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item

    return item
    
## Get a particular store
@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
         return abort(404,message="Store not found.")

## Create a particular item
@app.get("/item/<string:item_id>")
def get_items_in_store(item_id):
    try:
        return items[item_id]
    except KeyError:
        return abort(404,message="Item not found.")

if __name__ == "__main__":
    app.run(debug=True) 