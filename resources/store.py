import uuid
from flask import abort,request
from flask_smorest import Blueprint
from flask.views import MethodView
from db import stores
from schemas import StoreSchema

blp = Blueprint("stores",__name__,description="Operation on Stores")

@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200,StoreSchema)
    def get(self,store_id):
        try:
            return stores[store_id]
        except KeyError:
            return abort(404,message="Store not found.")

    def delete(self,store_id):
        try:
            del stores[store_id]
            return {"message":"Store Deleted"}
        except KeyError:
            abort(404,message="Item not found.")


@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200,StoreSchema(many=True))
    def get(self):
        return stores.values()
    
    @blp.arguments(StoreSchema)
    @blp.response(200,StoreSchema)
    def post(self,store_data):
        for store in stores.values():
            if store_data["name"] == store["name"]:
                abort(400, message=f"Store already exists.")

        store_id = uuid.uuid4().hex
        store = {**store_data, "id": store_id}
        stores[store_id] = store

        return store