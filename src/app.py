"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Vehicle, Favorite_Character, Favorite_Planet, Favorite_Vehicle
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors as a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Endpoints

@app.route('/users', methods=['GET'])
def get_users():
    try:
        # Query all records from the model
        query_results = User.query.all()
        print(query_results)
        results = list(map(lambda item: item.serialize(), query_results))

        if results:
            response_body = {
            "msg": "ok",
            "results": results
            }
            return jsonify(response_body), 200
        return jsonify({"msg": "Users not found"}), 404
    
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@app.route('/characters', methods=['GET'])
def get_characters():
    try:
        # Query all records from the model
        query_results = Character.query.all()
        results = list(map(lambda item: item.serialize(), query_results))

        if results:
            response_body = {
            "msg": "ok",
            "results": results
            }
            return jsonify(response_body), 200
        return jsonify({"msg": "Characters not found"}), 404
    
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@app.route('/characters/<int:character_id>', methods=['GET'])
def get_character(character_id):
    try:

        query_character = Character.query.filter_by(id=character_id).first()

        if query_character is None:
            return jsonify({"msg": "Character not found"}), 404
    
        response_body = {
            "msg": "ok",
            "result": query_character.serialize()
        }
        
        return jsonify(response_body), 200
    
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@app.route('/planets', methods=['GET'])
def get_planets():
    try:
        query_results = Planet.query.all()
        results = list(map(lambda item: item.serialize(), query_results))
        
        if results:
            response_body = {
                "msg": "ok",
                "results": results
            }
            return jsonify(response_body), 200
        return jsonify({"msg": "Planets not found"}), 404

    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    try:

        query_planet = Planet.query.filter_by(id=planet_id).first()
        
        if query_planet is None:
                return jsonify({"msg": "Planet not found"}), 404

        response_body = {
            "msg": "ok",
            "result": query_planet.serialize()
        }
        
        return jsonify(response_body), 200

    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500
    

@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    try:
        # Query all records from the model
        query_results = Vehicle.query.all()
        results = list(map(lambda item: item.serialize(), query_results))

        if results:
            response_body = {
            "msg": "ok",
            "results": results
            }
            return jsonify(response_body), 200
        return jsonify({"msg": "Vehicles not found"}), 404
    
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@app.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
    try:

        query_vehicle = Vehicle.query.filter_by(id=vehicle_id).first()

        if query_vehicle is None:
            return jsonify({"msg": "Vehicle not found"}), 404
    
        response_body = {
            "msg": "ok",
            "result": query_vehicle.serialize()
        }
        
        return jsonify(response_body), 200
    
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@app.route('/favorites', methods=["POST"])
def add_favorite():
    try:
        user_id = request.json.get("user_id")

        if not user_id:
            return jsonify({"msg": "User not found"}), 404
        
        character_id = request.json.get("character_id")
        planet_id = request.json.get("planet_id")
        vehicle_id = request.json.get("vehicle_id")

        if character_id:
            new_favorite = Favorite_Character(user_id=user_id, character_id=character_id)
            db.session.add(new_favorite)
            db.session.commit()

            favorite = {
                "id": new_favorite.id,
                "character": new_favorite.character_id,
                "user": new_favorite.user_id
            }
            return jsonify(favorite), 201
        
        elif planet_id:
            new_favorite = Favorite_Planet(user_id=user_id, planet_id=planet_id)
            db.session.add(new_favorite)
            db.session.commit()

            favorite = {
                "id": new_favorite.id,
                "planet": new_favorite.planet_id,
                "user": new_favorite.user_id
            }
            return jsonify(favorite), 201
        
        elif vehicle_id:
            new_favorite = Favorite_Vehicle(user_id=user_id, vehicle_id=vehicle_id)
            db.session.add(new_favorite)
            db.session.commit()

            favorite = {
                "id": new_favorite.id,
                "vehicle": new_favorite.vehicle_id,
                "user": new_favorite.user_id
            }
            return jsonify(favorite), 201
        else:
            return jsonify({"msg": "Insufficient data"}), 404
          
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@app.route('/favorites/<int:user_id>', methods=["GET"])
def get_user_favorites(user_id):
    try:
        # Get user's favorites
        favorite_characters = Favorite_Character.query.filter_by(user_id=user_id).all()
        favorite_planets = Favorite_Planet.query.filter_by(user_id=user_id).all()
        favorite_vehicles = Favorite_Vehicle.query.filter_by(user_id=user_id).all()

        # Serialize favorites
        favorite_characters_serialized = [fav.serialize() for fav in favorite_characters]
        favorite_planets_serialized = [fav.serialize() for fav in favorite_planets]
        favorite_vehicles_serialized = [fav.serialize() for fav in favorite_vehicles]

        # If no favorites, return 404
        if not favorite_characters_serialized and not favorite_planets_serialized and not favorite_vehicles_serialized:
            return jsonify({"msg": "You have no favorites"}), 404

        # Combine all favorites into a single dictionary
        results = {
            "favorite_characters": favorite_characters_serialized,
            "favorite_planets": favorite_planets_serialized,
            "favorite_vehicles": favorite_vehicles_serialized
        }

        return jsonify(results), 200
    
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500
    

@app.route('/favorite/character/<int:user_id>/<int:character_id>', methods=['DELETE'])
def delete_favorite_character(user_id, character_id):
    try:
        # Find the favorite in the database
        favorite_character = Favorite_Character.query.filter_by(user_id=user_id, character_id=character_id).first()

        if not favorite_character:
            return jsonify({"msg": "Favorite character not found"}), 404

        # Delete the favorite
        db.session.delete(favorite_character)
        db.session.commit()

        return jsonify({"msg": "Favorite character deleted"}), 200
    
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@app.route('/favorite/planet/<int:user_id>/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(user_id, planet_id):
    try:
        # Find the favorite in the database
        favorite_planet = Favorite_Planet.query.filter_by(user_id=user_id, planet_id=planet_id).first()

        if not favorite_planet:
            return jsonify({"msg": "Favorite planet not found"}), 404

        # Delete the favorite
        db.session.delete(favorite_planet)
        db.session.commit()

        return jsonify({"msg": "Favorite planet deleted"}), 200
    
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@app.route('/favorite/vehicle/<int:user_id>/<int:vehicle_id>', methods=['DELETE'])
def delete_favorite_vehicle(user_id, vehicle_id):
    try:
        # Find the favorite in the database
        favorite_vehicle = Favorite_Vehicle.query.filter_by(user_id=user_id, vehicle_id=vehicle_id).first()

        if not favorite_vehicle:
            return jsonify({"msg": "Favorite vehicle not found"}), 404

        # Delete the favorite
        db.session.delete(favorite_vehicle)
        db.session.commit()

        return jsonify({"msg": "Favorite vehicle deleted"}), 200
    
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
