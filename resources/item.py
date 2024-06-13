import uuid
from flask import abort,request
from flask_smorest import Blueprint
from flask.views import MethodView
from schemas import ItemSchema,ItemUpdateSchema
import models
from db import db
from sqlalchemy.exc import SQLAlchemyError

blp = Blueprint("Items",__name__,description="Operation on items")

@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200,ItemSchema(many=True))
    def get(self):
        return models.ItemModel.query.all()
    
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200,ItemSchema)
    def post(self,item_data):
        item = models.ItemModel(**item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,message="An error occured.")

        return item
    
@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.response(200,ItemSchema)
    def get(self,item_id):
        item = models.ItemModel.query.get_or_404(item_id)
        return item
        
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200,ItemSchema)
    def put(self ,item_data,item_id):
        item = models.ItemModel.query.get(item_id)

        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            item = models.ItemModel(id=item_id,**item_data)

        db.session.add(item)
        db.session.commit()

        return item

    def delete(self,item_id):
        item = models.ItemModel.query.get_or_404(item_id)

        db.session.delete(item)
        db.session.commit()

        return {"message":"Item  deleted"}
        