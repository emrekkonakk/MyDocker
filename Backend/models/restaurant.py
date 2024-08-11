from db import db
from models.city import City


class Restaurant(db.Model):
    __tablename__ = "restaurant"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    googlerating = db.Column(db.Float)
    userrating = db.Column(db.Float)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)
    googleratingtime = db.Column(db.DateTime)

    # Relationship to UserReview
    reviews = db.relationship('UserReview', backref='restaurant', lazy=True)

    def getrest0(self):
        return self.name

    def getgooglerate0(self):
        return str(self.googlerating)

    def getuserrate0(self):
        return str(self.userrating)

    def update_ratings(self):
        try:
            all_ratings = [review.rating for review in self.reviews if review.rating is not None]
            if all_ratings:
                self.userrating = sum(all_ratings) / len(all_ratings)
                db.session.commit()
        except Exception as e:
            print(f"Error updating restaurant rating: {e}")
            db.session.rollback()


def register_restaurant_commands(app):
    @app.cli.command("add-restaurant")
    def add_restaurant():
        city_name = input("Enter the name of the city for the restaurant: ")
        city = City.query.filter_by(name=city_name).first()
        if city:
            restaurant_name = input("Enter the name of the restaurant to add: ")
            existing_restaurant = Restaurant.query.filter_by(name=restaurant_name, city_id=city.id).first()
            if not existing_restaurant:
                new_restaurant = Restaurant(name=restaurant_name, city_id=city.id)
                db.session.add(new_restaurant)
                db.session.commit()
                print(f"Added new restaurant: {new_restaurant.name} to city: {city.name}")
            else:
                print(f"Restaurant '{restaurant_name}' already exists in {city_name}.")
        else:
            print("City not found. Please add the city first.")
