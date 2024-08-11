from flask import current_app
from flask_restful import Resource, reqparse, abort
from models.city import City
from models.country import Country
from db import db


class CityListResource(Resource):
    def get(self, country_id=None):
        if country_id:
            cities = City.query.filter_by(country_id=country_id).all()
            if cities:
                return [{'id': city.id,
                         'name': city.name,
                        'country_id': city.country_id} for city in cities], 200
            else:
                return {'message': 'No cities found for this country'}, 404
        else:
            cities = City.query.all()
            return [{'id': city.id, 'name': city.name, 'country_id': city.country_id} for city in cities], 200

    def post(self, country_id):
        if not Country.query.get(country_id):
            return {'message': 'Country not found'}, 404

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True,
                            help="Name cannot be blank!")
        args = parser.parse_args()

        if City.query.filter_by(name=args['name'], country_id=country_id).first():
            return {'message': 'City with the same name already exists in this country'}, 409

        city = City(name=args['name'], country_id=country_id)
        db.session.add(city)
        db.session.commit()
        return {'message': 'City created', 'id': city.id}, 201


class SingleCityResource(Resource):
    def get(self, country_id, city_id):
        city = City.query.filter_by(id=city_id, country_id=country_id).first()
        if not city:
            return {'message': 'City not found in this country'}, 404
        return {'id': city.id,
                'name': city.name, 'country_id': city.country_id}, 200

    def delete(self, city_id):
        city = City.query.get(city_id)
        if not city:
            return {'message': 'City not found'}, 404
        db.session.delete(city)
        db.session.commit()
        return {'message': 'City deleted'}, 204
