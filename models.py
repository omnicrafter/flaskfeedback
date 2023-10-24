from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database"""
    db.app = app
    db.init_app(app)


class User(db.Model):
    """Site User."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)

    # add repr method
    def __repr__(self):
        return f"<User #{self.id}: {self.username}: {self.first_name} {self.last_name}: {self.email}>"


@classmethod
def register(cls, username, pwd):
    """Register user w/ hashed password and return user."""
    hashed = bcrypt.generate_password_pash(pwd)
    # turn bytestring into normal (unicode utf8) string
    hashed_utf8 = hashed.decode("utf8")

    return cls(username=username, password=hashed_utf8)
