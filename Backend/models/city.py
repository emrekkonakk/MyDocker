from db import db
from models.country import Country


class City(db.Model):
    __tablename__ = "city"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=False)

    # Relationship to Restaurant
    restaurants = db.relationship('Restaurant', backref='city', lazy=True)

    def getcityid(self):
        return str(self.id)

    def getrate0(self):
        return "Sample rate information"


def register_city_commands(app):
    @app.cli.command("add-city")
    def add_city():
        country_name = input("Enter the name of the country for the city: ")

        country = Country.query.filter_by(name=country_name).first()
        if country:
            city_name = input("Enter the name of the city to add: ")
            existing_city = City.query.filter_by(name=city_name, country_id=country.id).first()
            if not existing_city:
                new_city = City(name=city_name, country_id=country.id)
                db.session.add(new_city)
                db.session.commit()
                print(f"Added new city: {new_city.name} to country: {country.name}")
            else:
                print(f"City '{city_name}' already exists in {country_name}.")
        else:
            print("Country not found. Please add the country first.")

# print(Country.query.filter_by(name='Utopia3').first().cities[0].name)
