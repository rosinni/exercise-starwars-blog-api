from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    favorite_character = db.relationship("Favorite_Character", backref = "user", lazy=True)
    favorite_planet = db.relationship("Favorite_Planet", backref = "user", lazy=True)
    favorite_vehicle = db.relationship("Favorite_Vehicle", backref = "user", lazy=True)

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "favorite_character": self.favorite_character,
            "favorite_planet": self.favorite_planet,
            "favorite_vehicle": self.favorite_vehicle
        }


class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    height = db.Column(db.Integer, nullable=False)
    mass = db.Column(db.Integer, nullable=False)
    hair_color = db.Column(db.String(50), nullable=False)
    skin_color = db.Column(db.String(50), nullable=False)
    eye_color = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    favorite_character = db.relationship("Favorite_Character", backref = "character", lazy=True)

    def __repr__(self):
        return '<Character %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "gender": self.gender,
            "favorite_character": self.favorite_character
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    climate = db.Column(db.String(50), nullable=False)
    diameter = db.Column(db.Integer, nullable=False)
    gravity = db.Column(db.Integer, nullable=False)
    orbital_period = db.Column(db.Integer, nullable=False)
    population = db.Column(db.Integer, nullable=False)
    rotation_period = db.Column(db.Integer, nullable=False)
    surface_water = db.Column(db.Integer, nullable=False)
    terrain = db.Column(db.String(50), nullable=False)
    favorite_planet = db.relationship("Favorite_Planet", backref = "planet", lazy=True)

    def __repr__(self):
        return '<Planet %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "diameter": self.diameter,
            "gravity": self.gravity,
            "orbital_period": self.orbital_period,
            "population": self.population,
            "rotation_period": self.rotation_period,
            "surface_water": self.surface_water,
            "terrain": self.terrain,
            "favorite_planet": self.favorite_planet
        }

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    cargo_capacity = db.Column(db.Integer, nullable=False)
    consumables = db.Column(db.String(50), nullable=False)
    cost_in_credits = db.Column(db.Integer, nullable=False)
    vehicle_class = db.Column(db.String(50), nullable=False)
    manufacturer = db.Column(db.String(50), nullable=False)
    passengers = db.Column(db.Integer, nullable=False)
    favorite_vehicle = db.relationship("Favorite_Vehicle", backref = "vehicle", lazy=True)

    def __repr__(self):
        return '<Vehicle %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "cargo_capacity": self.cargo_capacity,
            "consumables": self.consumables,
            "cost_in_credits": self.cost_in_credits,
            "vehicle_class": self.vehicle_class,
            "manufacturer": self.manufacturer,
            "passengers": self.passengers,
            "favorite_vehicle": self.favorite_vehicle
        }

class Favorite_Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey("character.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return '<Favorite_Character %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "character_id": self.character_id,
            "user_id": self.user_id
        }

class Favorite_Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    planet_id = db.Column(db.Integer, db.ForeignKey("planet.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return '<Favorite_Planet %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "planet_id": self.planet_id,
            "user_id": self.user_id
        }

class Favorite_Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey("vehicle.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return '<Favorite_Vehicle %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "vehicle_id": self.vehicle_id,
            "user_id": self.user_id
        }
