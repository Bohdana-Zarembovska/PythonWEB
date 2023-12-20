from flask import request
from flask_restful import Resource
from app.auth.models import User
from ..extensions import db
from .build_sch.user import UserSchema


class UsersApi(Resource):
    def get(self):
        schema = UserSchema(many=True)
        page = request.args.get('page', 1, type=int)
        
        users = User.query.paginate(page = page, per_page = 2)

        return {'users': schema.dump(users), 'page': users.page, 'pages': users.pages}
    
    def post(self):
        schema = UserSchema()

        new_user = schema.load(request.json)
        db.session.add(new_user)
        db.session.commit()

        return {'user': schema.dump(new_user)}, 201

class UserApi(Resource):
    def get(self, id):
        schema = UserSchema()
        user = User.query.filter_by(id=id).first_or_404()
        return {"user": schema.dump(user)}

    
    def put(self, id):
        schema = UserSchema(partial=True)
        user = User.query.filter_by(id=id).first_or_404()
        
        user = schema.load(request.json, instance=user)
        db.session.add(user)
        db.session.commit()
        
        return {"user": schema.dump(user)}
    
    def delete(self, id):
        schema = UserSchema()
        user = User.query.filter_by(id=id).first_or_404()
        
        db.session.delete(user)
        db.session.commit()
        
        return {"user": schema.dump(user)}