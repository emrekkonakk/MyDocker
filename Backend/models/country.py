from db import db


class Country(db.Model):
    __tablename__ = "country"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    # Relationship to City
    cities = db.relationship('City', backref='country', lazy=True)

    def getcount(self):
        return str(self.id)

    @classmethod
    def add_country(cls, name):
        existing_country = cls.query.filter_by(name=name).first()
        if not existing_country:
            new_country = cls(name=name)
            db.session.add(new_country)
            db.session.commit()
            return new_country
        return existing_country


def register_commands(app):
    @app.cli.command("add-country")
    def add_country():
        country_name = input("Enter country name: ")
        if country_name:
            country = Country.add_country(country_name)
            if country:
                print(f"Added new country: {country.name}")
            else:
                print("Country already exists.")
        else:
            print("No country name provided.")
