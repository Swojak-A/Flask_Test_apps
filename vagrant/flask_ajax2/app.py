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



@app.route("/")
def hello():
	return render_template("index.html")

@app.route("/search_results", methods=['POST'])
def search_results():

    column = request.form['column'].lower()
    user_input = request.form['input'].lower()

    # print(column)
    # if column.lower() in ["name"]:
    #     pass
    # elif column.lower() in ["latin name","lat name","lat_name"]:
    #
    # elif column.lower() in ["type"]:
    #     pass

    if user_input and not column:
        if user_input in ["edible"]:
            fungi = Fungus.query.filter_by(edible=True).all()
        elif user_input in ["poisonous", "poisonus", "poison"]:
            fungi = Fungus.query.filter_by(edible=False).all()
        else:
            fungi = Fungus.query.filter((Fungus.name.like('%{}%'.format(user_input)) \
                                     | Fungus.type.like('%{}%'.format(user_input)) \
                                     | Fungus.lat_name.like('%{}%'.format(user_input)))).all()
    elif user_input and (column in ["name"]):
        fungi = Fungus.query.filter(Fungus.name.like('%{}%'.format(user_input))).all()
    elif user_input and (column in ["latin name","lat name","lat_name"]):
        fungi = Fungus.query.filter(Fungus.lat_name.like('%{}%'.format(user_input))).all()
    elif user_input and (column in ["type"]):
        fungi = Fungus.query.filter(Fungus.type.like('%{}%'.format(user_input))).all()
    elif user_input and (column in ["edible"]):
        print("user input: {}, column: {}".format(user_input, column))
        if user_input in ["true", "yes", "edible"]:
            fungi = Fungus.query.filter_by(edible=True).all()
        elif user_input in ["false", "no", "poisonous"]:
            fungi = Fungus.query.filter_by(edible=False).all()
    elif user_input and (column in ["poisonous"]):
        print("user input: {}, column: {}".format(user_input, column))
        if user_input in ["true", "yes", "poisonous"]:
            fungi = Fungus.query.filter_by(edible=False).all()
        elif user_input in ["false", "no", "edible"]:
            fungi = Fungus.query.filter_by(edible=True).all()
    else:
        fungi = Fungus.query.all()

    return render_template("search-response.html", items=fungi)


if __name__ == "__main__":
	app.run(host="0.0.0.0", port="5000", debug=True)