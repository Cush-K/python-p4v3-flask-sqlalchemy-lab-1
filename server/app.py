# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

@app.route("/earthquakes/<int:id>", methods=['GET'])
def event(id):
    earthquake = Earthquake.query.get(id)
    
    if earthquake:
        response = {
            "id":earthquake.id,
            "location":earthquake.location,
            "magnitude":earthquake.magnitude,
            "year":earthquake.year,            
        }
        return jsonify(response), 200
    else:
         return jsonify({"message": f"Earthquake {id} not found."}), 404

@app.route("/earthquakes/magnitude/<float:mag>", methods=['GET'])  # Accept magnitude as a float
def power(mag):
    earthquakes = Earthquake.query.filter_by(magnitude=mag).all()
    
    if not earthquakes:
        return jsonify({"count": 0, "quakes": []}), 200
    
    quake_list = []
    for quake in earthquakes:
        quake_data = {
            "id": quake.id,
            "location": quake.location,
            "magnitude": quake.magnitude,
            "year": quake.year
        }
        quake_list.append(quake_data)
    
    response = {
        "count": len(earthquakes),
        "quakes": quake_list
    }
    
    return jsonify(response), 200



if __name__ == '__main__':
    app.run(port=5555, debug=True)
