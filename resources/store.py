import uuid
from flask import abort,request
from flask_smorest import Blueprint
from flask.views import MethodView
from schemas import StoreSchema
from db import db
import models
from sqlalchemy.exc import SQLAlchemyError,IntegrityError

blp = Blueprint("stores",__name__,description="Operation on Stores")

@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200,StoreSchema)
    def get(self,store_id):
        store = models.StoreModel.query.get_or_404(store_id)
        return store

    def delete(self,store_id):
        store = models.StoreModel.query.get_or_404(store_id)

        db.session.delete(store)
        db.session.commit()

        return {"message":"Store Deleted."}

@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200,StoreSchema(many=True))
    def get(self):
        return models.StoreModel.query.all()
    
    @blp.arguments(StoreSchema)
    @blp.response(200,StoreSchema)
    def post(self,store_data):
        store = models.StoreModel(**store_data)

        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(500,message="A store with that name already exists.")
        except SQLAlchemyError:
            abort(500,message="An error occured.")

        return store