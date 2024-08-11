from flask import current_app
from flask_restful import Resource, reqparse, abort
from models.restaurant import Restaurant
from models.city import City
from db import db


class RestaurantListResource(Resource):
    def get(self, city_id=None):
        if city_id:
            restaurants = Restaurant.query.filter_by(city_id=city_id).all()
            if restaurants:
                return [{'id': restaurant.id, 'name': restaurant.name,
                        'city_id': restaurant.city_id} for restaurant in restaurants], 200
            else:
                return {'message': 'No restaurants found in this city'}, 404
        else:
            abort(400, message="City ID is required for this endpoint.")

    def post(self, city_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help="Name cannot be blank!")
        args = parser.parse_args()

        if Restaurant.query.filter_by(name=args['name'], city_id=city_id).first():
            return {'message': 'Restaurant with the same name already exists in this city'}, 409

        try:
            restaurant = Restaurant(name=args['name'], city_id=city_id)
            db.session.add(restaurant)
            db.session.commit()
            return {'message': 'Restaurant created', 'id': restaurant.id}, 201
        except Exception as e:
            current_app.logger.error(f"Failed to create restaurant: {e}")
            return {'message': 'Internal Server Error'}, 500


class SingleRestaurantResource(Resource):
    def get(self, restaurant_id):
        restaurant = Restaurant.query.get(restaurant_id)
        if not restaurant:
            return {'message': 'Restaurant not found'}, 404
        return {'id': restaurant.id, 'name': restaurant.name,
                'city_id': restaurant.city_id}, 200

    def patch(self, restaurant_id):
        restaurant = Restaurant.query.get(restaurant_id)
        if not restaurant:
            return {'message': 'Restaurant not found'}, 404

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, store_missing=False)
        args = parser.parse_args()

        if 'name' in args:
            restaurant.name = args['name']

        try:
            db.session.commit()
            return {'message': 'Restaurant updated'}, 200
        except:
            db.session.rollback()
            return {'message': 'Failed to update restaurant'}, 500

    def delete(self, restaurant_id):
        restaurant = Restaurant.query.get(restaurant_id)
        if not restaurant:
            return {'message': 'Restaurant not found'}, 404

        db.session.delete(restaurant)
        db.session.commit()
        return {'message': 'Restaurant deleted'}, 204
