"""Blogly application."""

from flask import Flask, request, redirect, render_template, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route("/")
def home_page():
    """ Redirect to /users ROUTE """

    return redirect('/users')

@app.route("/users")
def list_users():
    """ List all users from the database """

    # "order_by()" orders the users by "last_name, first_name"
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template("listing.html", users = users)

@app.route("/users/new")
def show_user_form():
    """ Show form to create a new user """

    return render_template("user-form.html")


@app.route("/users/new", methods=['POST'])
def create_user():
    """ Create a new user and update the database """

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]
    image_url = image_url if image_url else None

    new_user = User(first_name = first_name, last_name = last_name, image_url = image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")

@app.route("/users/<int:user_id>")
def show_detail(user_id):
    """ Shows the details of the user, the user clicked on """

    user = User.query.get_or_404(user_id)
    return render_template("detail.html", user = user)

@app.route("/users/<int:user_id>/edit")
def show_edit(user_id):
    """ Show the edit page for a particular user """

    user = User.query.get_or_404(user_id)
    return render_template("edit.html", user = user)

@app.route("/users/<int:user_id>/edit", methods = ['POST'])
def edit_user(user_id):
    """Handle form submission for updating an existing user"""

    edit_user = User.query.get_or_404(user_id)
    edit_user.first_name = request.form["first_name"]
    edit_user.last_name = request.form["last_name"]
    edit_user.image_url = request.form["image_url"]

    db.session.add(edit_user)
    db.session.commit()

    return redirect("/users")

@app.route("/users/<int:user_id>/delete", methods = ['POST'])
def delete_user(user_id):
    """ Delete a user and update the database"""

    User.query.filter(User.id == user_id).delete()
    db.session.commit()

    return redirect("/users")


