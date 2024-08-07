from flask import current_app
from flask_restful import Resource, reqparse
from models.country import Country
from Backend.db import db


class CountryResource(Resource):
    def get(self, country_id=None):
        try:
            if country_id:
                country = Country.query.get(country_id)
                if not country:
                    return {'message': 'Country not found'}, 404
                return {'id': country.id, 'name': country.name}, 200
            else:
                countries = Country.query.all()
                return [{'id': country.id, 'name': country.name} for country in countries], 200
        except Exception as e:
            current_app.logger.error(f"Server Error: {e}")
            return {'message': 'Internal Server Error'}, 500

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help="Name cannot be blank!")
        args = parser.parse_args()

        if Country.query.filter_by(name=args['name']).first():
            return {'message': 'Country with the same name already exists'}, 409

        try:
            country = Country(name=args['name'])
            db.session.add(country)
            db.session.commit()
            return {'message': 'Country created', 'id': country.id}, 201
        except Exception as e:
            current_app.logger.error(f"Failed to create country: {e}")
            return {'message': 'Internal Server Error'}, 500

    def delete(self, country_id):
        try:
            country = Country.query.get(country_id)
            if not country:
                return {'message': 'Country not found'}, 404

            db.session.delete(country)
            db.session.commit()
            return {'message': 'Country deleted'}, 204
        except Exception as e:
            current_app.logger.error(f"Failed to delete country: {e}")
            return {'message': 'Internal Server Error'}, 500
