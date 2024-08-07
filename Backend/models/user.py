from Backend.db import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    reviews = db.relationship('UserReview', backref='user', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.name}>'

    @classmethod
    def add_user(cls, name):
        existing_user = cls.query.filter_by(name=name).first()
        if not existing_user:
            new_user = cls(name=name)
            db.session.add(new_user)
            db.session.commit()
            return new_user
        return existing_user


def register_user_commands(app):
    @app.cli.command("add-user")
    def add_user():
        user_name = input("Enter user name: ")
        if user_name:
            user = User.add_user(user_name)
            if user:
                print(f"Added new user: {user.name}")
            else:
                print("User already exists.")
        else:
            print("No user name provided.")
