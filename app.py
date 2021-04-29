"""Flask app for Cupcakes"""

from flask import Flask, request, jsonify, render_template
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)


@app.route('/api/cupcakes')
def list_cupcakes():
    """Get JSON data about all cupcakes."""

    cupcakes = Cupcake.query.all()
    serialized = [c.serialize_cupcake() for c in cupcakes]

    return (jsonify(cupcakes=serialized), 200)


@app.route('/api/cupcakes/<int:cupcake_id>')
def get_cupcake(cupcake_id):
    """Get data about a single cupcake."""

    cupcake = Cupcake.query.get(cupcake_id)
    serialized = cupcake.serialize_cupcake()
    return (jsonify(cupcake=serialized), 200)


@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    """Create a cupcake with flavor, size, rating and image data."""

    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json["image"]

    cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

    db.session.add(cupcake)
    db.session.commit()

    serialized = cupcake.serialize_cupcake()

    return (jsonify(cupcake=serialized), 201)

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):
    """Update a cupcake with the id passed in the URL."""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    cupcake.flavor = request.json["flavor"]
    cupcake.size = request.json["size"]
    cupcake.rating = request.json["rating"]
    cupcake.image = request.json["image"]
    db.session.commit()

    serialized = cupcake.serialize_cupcake()
    return (jsonify(cupcake=serialized), 200)

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):
    """Delete a cupcake with the id passed in the URL."""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = cupcake.serialize_deleted_cupcake()
    Cupcake.query.filter(Cupcake.id == cupcake_id).delete()
    db.session.commit()

    return (jsonify(cupcake = serialized), 200)


# ---------------------------------------------------------------------------------------------- #

@app.route('/')
def show_cupcakes():
    """Shows a list of all cupcakes and a form to add a cupcake."""

    return render_template("home.html")