import uuid
from flask import abort,request
from flask_smorest import Blueprint
from flask.views import MethodView
from db import items
from schemas import ItemSchema,ItemUpdateSchema

blp = Blueprint("Items",__name__,description="Operation on items")

@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200,ItemSchema(many=True))
    def get(self):
        return items.values()
    
    @blp.arguments(ItemSchema)
    @blp.response(200,ItemSchema)
    def post(self,item_data):
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
    
@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.response(200,ItemSchema)
    def get(self,item_id):
        try:
            return items[item_id]
        except KeyError:
            return abort(404,message="Item not found.")
        
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200,ItemSchema)
    def put(self ,item_data,item_id):
        try:
            item = items[item_id]
            item.update(item_data)
            return item
        except KeyError:
            abort(400,message = "Item not found")

    def delete(self,item_id):
        try:
            del items[item_id]
            return {"message":"Item Deleted"}
        except KeyError:
            abort(404,message="Item not found.")