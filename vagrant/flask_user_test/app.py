from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_user import login_required, UserManager, UserMixin, SQLAlchemyAdapter

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db/test.db"
app.config['SECRET_KEY'] = "ss_key"
app.config['CSRF_ENABLED'] = True
app.config['USER_ENABLE_EMAIL'] = False

db = SQLAlchemy(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='1')
    active = db.Column(db.Boolean(), nullable=False, server_default='0')

user_manager = UserManager(app, db, User)

@app.route('/')
def mainPage():
    return "<h1>Home Page</h1>"

@app.route('/restricted')
@login_required
def restricted():
    return "This is restircted for users only"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5050", debug=True)