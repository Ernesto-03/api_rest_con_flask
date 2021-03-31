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
from models import db, UserFav, People, Planet, Vehicle
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)




@app.route('/user', methods=['GET'])
def handle_hello():
    response_body = {
        "msg": "Hello, this is your GET /user response "
    }
    return jsonify(response_body), 200



@app.route('/userfav', methods=['GET'])
def list_userfav():
    userfav = UserFav.query.all()
    response_body = {
        "msg": "Hello, this is your GET /userfav ",
        "data": userfav
    }
    return jsonify(response_body), 200



@app.route('/people', methods=['GET'])
def list_people():
    people = People.query.all()
    response_body = {
        "msg": "Hello, this is your GET /people ",
        "data": people
    }
    return jsonify(response_body), 200   



@app.route('/planet', methods=['GET'])
def list_planet():
    planet = Planet.query.all()
    response_body = {
        "msg": "Hello, this is your GET /planet ",
        "data": planet
    }
    return jsonify(response_body), 200    



@app.route('/vehicle', methods=['GET'])
def list_vehicle():
    vehicle = Vehicle.query.all()
    response_body = {
        "msg": "Hello, this is your GET /vehicle ",
        "data": vehicle
    }
    return jsonify(response_body), 200  



@app.route('/addAll', methods=['POST'])
def addAll():
    body = request.get_json()
    people = body['people']
    planet = body['planet']
    vehicle = body['vehicle']
    
    for p in people:
        people1 = People(
            name= p["Character Name"],
            height = p["Character height"],
            mass = p["Character mass"],
            hair_color = p["Character hair color"],
            skin_color = p["Character skin color"],
            eye_color = p["Character eye color"],
            birth_year = p["Character birth year"],
            gender = p["Character gender"]
        )
        db.session.add(people1)

    for p in planet:
        planet1 = Planet(
            planet_name = pl["Planet name"],
            rotation_period = pl["rotation period"],
            orbital_period = pl["orbital period"],
            diameter = pl["diameter"],
            climate = pl["climate"],
            gravity = pl["gravity"],
            terrain = pl["terrain"],
            population = pl["population"]

        )
        db.session.add(planet1)

    for p in vehicle:
        vehicle1 = Vehicle(
            vehicle_name = v["vehicle name"],
            model = v["model"],
            passenger = v["passenger"],
            consumable = v["consumable"],
            starship_class = v["starship class"],
            lenght = v["lenght"],
            cargo_capacity = v["cargo capacity"],
            hyperdrive_rating = v["hyperdrive rating"]

        )
        db.session.add(vehicle1) 

        
        db.session.commit()
    


#user1 = Person(username="my_super_username", email="my_super@email.com")
#db.session.add(user1)
#db.session.commit()

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
