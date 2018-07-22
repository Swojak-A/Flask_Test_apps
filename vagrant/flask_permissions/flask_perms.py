# This file contains an example Flask-User application.
# To keep the example simple, we are applying some unusual techniques:
# - Placing everything in one file
# - Using class-based configuration (instead of file-based configuration)
# - Using string-based templates (instead of file-based templates)

import datetime
from flask import Flask, request, render_template, flash, redirect, url_for
from flask_babelex import Babel
from flask_sqlalchemy import SQLAlchemy
from flask_user import current_user, login_required, roles_required, UserManager, UserMixin


# Class-based application configuration
class ConfigClass(object):
    """ Flask application config """

    # Flask settings
    SECRET_KEY = 'This is an INSECURE secret!! DO NOT use this in production!!'

    # Flask-SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = 'sqlite:///perms_test.db'  # File-based SQL database
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Avoids SQLAlchemy warning

    # Flask-Mail SMTP server settings
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = 'online.menu.071@gmail.com'
    MAIL_PASSWORD = 'Misutsuruzu1'
    MAIL_DEFAULT_SENDER = '"Online Menu" <online.menu.071@gmail.com>'

    # Flask-User settings
    USER_APP_NAME = "Online Menu Test"  # Shown in and email templates and page footers
    USER_ENABLE_EMAIL = True  # Enable email authentication
    USER_ENABLE_USERNAME = False  # Disable username authentication
    USER_EMAIL_SENDER_NAME = USER_APP_NAME
    USER_EMAIL_SENDER_EMAIL = 'online.menu.071@gmail.com'


""" Flask application factory """

# Create Flask app load app.config
app = Flask(__name__)
app.config.from_object(__name__ + '.ConfigClass')

# Initialize Flask-BabelEx
babel = Babel(app)

# Initialize Flask-SQLAlchemy
db = SQLAlchemy(app)

auths = db.Table('authorizations',
                 db.Column('user_id', db.Integer, db.ForeignKey("users.id")),
                 db.Column('restaurant_id', db.Integer, db.ForeignKey("restaurants.id")))

# Define the User data-model.
# NB: Make sure to add flask_user UserMixin !!!
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')

    # User authentication information. The collation='NOCASE' is required
    # to search case insensitively when USER_IFIND_MODE is 'nocase_collation'.
    email = db.Column(db.String(255, collation='NOCASE'), nullable=False, unique=True)
    email_confirmed_at = db.Column(db.DateTime())
    password = db.Column(db.String(255), nullable=False, server_default='')

    # User information
    first_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')
    last_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')

    # Define the relationship to Role via UserRoles
    roles = db.relationship('Role', secondary='user_roles')
    authorization = db.relationship("Restaurant", secondary=auths, backref=db.backref('authorizations', lazy="dynamic"))

# Define the Role data-model
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

# Define the UserRoles association table
class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))

class Restaurant(db.Model):
    __tablename__ = 'restaurants'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)

# class Restaurant_Auth(db.Model):
#     __tablename__ = 'restaurant_auth'
#     id = db.Column(db.Integer(), primary_key=True)
#     user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
#     restaurant_id = db.Column(db.Integer(), db.ForeignKey('restaurants.id', ondelete='CASCADE'))

# Setup Flask-User and specify the User data-model
user_manager = UserManager(app, db, User)

# The Home page is accessible to anyone
@app.route('/')
def home_page():
    return "main page"

# The Members page is only accessible to authenticated users
@app.route('/members')
@login_required  # Use of @login_required decorator
def member_page():
    return "login required"

# The Admin page requires an 'Admin' role.
@app.route('/admin')
@roles_required('Admin')  # Use of @roles_required decorator
def admin_page():
    return "admin only"

@app.route('/restaurant/new', methods=['GET', 'POST'])
@login_required
def newRestaurant():
    if request.method == "POST":
        newRestaurant = Restaurant(name=request.form['restaurant-name'])
        db.session.add(newRestaurant)

        owner_role = Role.query.filter_by(id=2).one()
        current_user.roles.append(owner_role)
        current_user.authorization.append(newRestaurant)
        db.session.add(current_user)
        db.session.commit()

        return redirect(url_for('member_page'))

    return render_template("newrestaurant.html")

@app.route('/restaurant/<int:restaurant_id>/edit')
# @roles_required('Owner')
def editRestaurant(restaurant_id):
    print(current_user.authorization)
    editedRestaurant = Restaurant.query.filter_by(id=restaurant_id).one()
    if editedRestaurant in current_user.authorization:
        print(True)

    return "name: {}".format(editedRestaurant.name)


# Start development web server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5070, debug=True)