from flask import current_app, request
from flask_restful import Resource, reqparse, abort
from models.user_review import UserReview
from models.restaurant import Restaurant
from db import db
import datetime


class ReviewResource(Resource):
    def get(self, userreviewId):
        user_review = UserReview.get_review(userreviewId)
        if not user_review:
            return {'message': 'User review not found'}, 404
        return user_review.serialize(), 200

    def patch(self, userreviewId):
        user_review = UserReview.get_review(userreviewId)
        if not user_review:
            return {'message': 'User review not found'}, 404

        parser = reqparse.RequestParser()
        parser.add_argument('comment', type=str, store_missing=False)
        parser.add_argument('rating', type=float, store_missing=False)
        args = parser.parse_args()

        comment = args.get('comment')
        rating = args.get('rating')

        user_review.update_review(comment, rating)
        return {'message': 'User review updated'}, 200

    def delete(self, userreviewId):
        user_review = UserReview.get_review(userreviewId)
        if not user_review:
            return {'message': 'User review not found'}, 404

        user_review.delete_review()
        return {'message': 'User review deleted'}, 204


class ReviewsListResource(Resource):
    def get(self, restaurantId):
        after = request.args.get('after')
        minrate = request.args.get('minrate', type=float)
        maxrate = request.args.get('maxrate', type=float)

        query = UserReview.query.filter(UserReview.restaurant_id == restaurantId)

        if after:
            date_after = datetime.datetime.strptime(after, '%Y-%m-%d')
            query = query.filter(UserReview.date > date_after)

        if minrate is not None:
            query = query.filter(UserReview.rating >= minrate)

        if maxrate is not None:
            query = query.filter(UserReview.rating <= maxrate)

        reviews = query.order_by(UserReview.rating.desc()).all()
        if not reviews:
            return {'message': 'No reviews found matching the criteria'}, 404

        return [{
            'id': review.id,
            'user_id': review.user_id,
            'comment': review.comment,
            'rating': review.rating,
            'date': review.date.isoformat()
        } for review in reviews], 200

    def post(self, restaurantId):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', required=True, type=int, help="User ID is required.")
        parser.add_argument('comment', type=str, required=True, help="Comment cannot be blank.")
        parser.add_argument('rating', type=float, required=True, help="Rating must be provided.")
        args = parser.parse_args()

        user_id = args['user_id']
        restaurant_id = restaurantId
        comment = args['comment']
        rating = args['rating']

        review = UserReview.add_review(user_id, restaurant_id, comment, rating)

        return {'message': 'User review added', 'id': review.id}, 201


class UserReviewResource(Resource):
    def get(self, userId, reviewId):
        review = UserReview.get_user_review(reviewId, userId)
        if not review:
            abort(404, message="User review not found.")
        return {
            'id': review.id,
            'user_id': review.user_id,
            'restaurant_id': review.restaurant_id,
            'comment': review.comment,
            'rating': review.rating,
            'date': review.date.isoformat()
        }, 200
