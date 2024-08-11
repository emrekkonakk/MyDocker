from flask import current_app
from flask_restful import Resource, reqparse
from models.user import User
from db import db


class UserResource(Resource):
    def get(self, user_id=None):
        try:
            if user_id:
                user = User.query.get(user_id)
                if not user:
                    return {'message': 'User not found'}, 404
                return {'id': user.id, 'name': user.name}, 200
            else:
                users = User.query.all()
                return [{'id': user.id,
                         'name': user.name} for user in users], 200
        except Exception as e:
            current_app.logger.error(f"Server Error: {e}")
            return {'message': 'Internal Server Error'}, 500

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help="Name cannot be blank!")
        args = parser.parse_args()

        if User.query.filter_by(name=args['name']).first():
            return {'message': 'A user with that name already exists'}, 409

        try:
            user = User(name=args['name'])
            db.session.add(user)
            db.session.commit()
            return {'message': 'User created', 'id': user.id}, 201
        except Exception as e:
            current_app.logger.error(f"Failed to create user: {e}")
            return {'message': 'Internal Server Error'}, 500

    def delete(self, user_id):
        try:
            user = User.query.get(user_id)
            if not user:
                return {'message': 'User not found'}, 404

            db.session.delete(user)
            db.session.commit()
            return {'message': 'User deleted'}, 204
        except Exception as e:
            current_app.logger.error(f"Failed to delete user: {e}")
            return {'message': 'Internal Server Error'}, 500
