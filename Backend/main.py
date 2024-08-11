from flask import Flask, render_template, request
from flask_restful import Api
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import os
import sys
from db import db
from resources.restaurantclass import RestaurantListResource, SingleRestaurantResource
from resources.cityclass import CityListResource, SingleCityResource
from resources.countryclass import CountryResource
from resources.userclass import UserResource
from resources.userreviewclass import ReviewResource, ReviewsListResource, UserReviewResource
from models.city import City, register_city_commands
from models.country import Country, register_commands
from models.restaurant import Restaurant, register_restaurant_commands
from models.user_review import UserReview, register_user_review_commands
from models.user import User, register_user_commands

from flask_cors import CORS


def create_app():
    print(sys.path)
    app = Flask(__name__)
    api = Api(app)
    CORS(app)

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", 'default_secret_key')
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL",
                                                      "mysql+pymysql://root:Bibendum1.@localhost/internship")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate = Migrate(app, db)

    api.add_resource(CountryResource, '/api/v1/countries', '/api/v1/countries/<int:country_id>')

    api.add_resource(CityListResource, '/api/v1/cities', '/api/v1/countries/<int:country_id>/cities')
    api.add_resource(SingleCityResource, '/api/v1/countries/<int:country_id>/cities/<int:city_id>',
                     '/api/v1/cities/<int:city_id>')

    api.add_resource(RestaurantListResource, '/api/v1/cities/<int:city_id>/restaurants')
    api.add_resource(SingleRestaurantResource, '/api/v1/restaurants/<int:restaurant_id>')

    api.add_resource(UserResource, '/api/v1/users', '/api/v1/users/<int:user_id>')

    api.add_resource(ReviewsListResource, '/api/v1/restaurants/<int:restaurantId>/userreviews')
    api.add_resource(ReviewResource, '/api/v1/userreviews/<int:userreviewId>')
    api.add_resource(UserReviewResource, '/api/v1/user/<int:userId>/userreviews/<int:reviewId>')

    with app.app_context():

        register_commands(app)
        register_city_commands(app)
        register_restaurant_commands(app)
        register_user_review_commands(app)
        register_user_commands(app)

    # Define routes
    @app.route('/')
    def index():
        param = request.args.get('param', "No parameter provided")
        return render_template('index.html', param=param)

    @app.route('/submit', methods=['POST'])
    def submit():
        user_input = request.form['user_input']
        param = request.args.get('param', "No parameter provided")
        return render_template('index.html', user_input=user_input, param=param)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
