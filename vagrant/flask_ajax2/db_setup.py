from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy


class ConfigClass(object):
    SECRET_KEY = 'This is an INSECURE secret!! DO NOT use this in production!!'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///fungus.db'  # File-based SQL database
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Avoids SQLAlchemy warning

app = Flask(__name__)
app.config.from_object(__name__ + '.ConfigClass')
db = SQLAlchemy(app)

class Fungus(db.Model):
    _tablename__ = "fungus"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=True)
    lat_name = db.Column(db.String(25))
    type = db.Column(db.String(25))
    edible = db.Column(db.Boolean)


db.create_all()

fly_amanita = Fungus(name="Fly Amanita",
                     lat_name="Amanita muscaria",
                     type="Amanita",
                     edible=False)
db.session.add(fly_amanita)
db.session.commit()

death_cap = Fungus(name="Death Cap",
                   lat_name="Amanita phalloides",
                   type="Amanita",
                   edible=False)
db.session.add(death_cap)
db.session.commit()

bay_bolete = Fungus(name="Bay Bolete",
                   lat_name="Imleria badia",
                   type="Imleria",
                   edible=True)
db.session.add(bay_bolete)
db.session.commit()

saffron_milk_cap = Fungus(name="Saffron Milk Cap",
                   lat_name="Lactarius deliciosus",
                   type="Lactarius",
                   edible=True)
db.session.add(saffron_milk_cap)
db.session.commit()

indigo_milk_cap = Fungus(name="Indigo Milk Cap",
                   lat_name="Lactarius indigo",
                   type="Lactarius",
                   edible=True)
db.session.add(indigo_milk_cap)
db.session.commit()