from flask import Flask,request
from db import stores,items
import uuid

app = Flask(__name__)

@app.get("/store")
def get_stores():
    return {"stores": list(stores.values())}

@app.get("/items")
def get_all_items():
    return {"items": list(items.values())}

@app.post("/store")
def create_store():
    store_data = request.get_json()
    store_id = uuid.uuid4().hex
    store = {**store_data,"id": store_id}
    stores[store_id] = store
    return store, 201

@app.post("/item")
def create_item():
    item_data = request.get_json()
    if item_data["store_id"] not in stores:
        return {"msg":"Store doesn't exist in the database."},404
    item_id = uuid.uuid4().hex
    item = {**item_data,"item_id":item_id}
    items[item_id] = item
    return item, 201
    

@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        return {"msg":"Store doesn't exist in the database."},404
    

@app.get("/item/<string:item_id>")
def get_items_in_store(item_id):
    try:
        return items[item_id]
    except KeyError:
        return {"msg":"Item not found."}, 404

if __name__ == "__main__":
    app.run(debug=True) 