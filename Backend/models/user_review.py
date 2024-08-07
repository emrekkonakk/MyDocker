from Backend.db import db
from datetime import datetime
from models.user import User
from models.restaurant import Restaurant


class UserReview(db.Model):
    __tablename__ = "user_review"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    comment = db.Column(db.String(255))
    rating = db.Column(db.Float)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def get0(self):
        return f"Review by user {self.user_id}"

    @staticmethod
    def get_review(review_id):
        return UserReview.query.get(review_id)

    @staticmethod
    def get_reviews_by_restaurant(restaurant_id):
        return UserReview.query.filter_by(restaurant_id=restaurant_id).all()

    @classmethod
    def add_review(cls, user_id, restaurant_id, comment, rating):
        new_review = cls(user_id=user_id, restaurant_id=restaurant_id,
                         comment=comment, rating=rating, date=datetime.utcnow())

        db.session.add(new_review)
        db.session.commit()
        return new_review

    def update_review(self, comment=None, rating=None):
        if comment is not None:
            self.comment = comment
        if rating is not None:
            self.rating = rating
        db.session.commit()

    def delete_review(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_user_review(cls, review_id, user_id):
        return cls.query.filter_by(id=review_id, user_id=user_id).first()


def register_user_review_commands(app):
    @app.cli.command("add-review")
    def add_review():
        user_id_input = input("Enter user ID: ")
        try:
            user_id = int(user_id_input)
            user = User.query.get(user_id)
            if not user:
                print("User not found.")
                return
        except ValueError:
            print("Invalid user ID.")
            return

        restaurant_name = input("Enter restaurant name: ")
        restaurant = Restaurant.query.filter_by(name=restaurant_name).first()
        if not restaurant:
            print("No restaurant found with that name.")
            return

        comment = input("Enter comment: ")
        try:
            rating = float(input("Enter rating (0-10): "))
            if not (0 <= rating <= 10):
                print("Rating must be between 0 and 10.")
                return
        except ValueError:
            print("Invalid rating. Please enter a number between 0 and 10.")
            return

        review = UserReview(
            user_id=user_id,
            restaurant_id=restaurant.id,
            comment=comment,
            rating=rating,
            date=datetime.utcnow()
        )

        db.session.add(review)

        restaurant.update_ratings()

        db.session.commit()
        print("Review added successfully.")
