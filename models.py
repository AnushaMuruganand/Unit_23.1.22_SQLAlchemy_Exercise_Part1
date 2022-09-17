"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS8Pe2gx8Z68Cs0vGplXvVBmSSKiA7yfijA4A&usqp=CAU"


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """ User. """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    first_name = db.Column(db.String(50), nullable=False, unique=True)

    last_name = db.Column(db.String(50), nullable=False, unique=True)

    image_url = db.Column(db.Text, nullable=False, default = DEFAULT_IMAGE_URL)

    # Adding a "property" class, which allows us to create a property for this class so we can access as "User.propertyname". "propertyname" is same as the function name we define here. Here we access this as "User.full_name"
    @property
    def full_name(self):
        """Return full name of user."""

        return f"{self.first_name} {self.last_name}"


