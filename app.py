from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import connect_db, db, User


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///hashingexercise'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret'

app.app_context().push()

connect_db(app)
# db.create_all()


@app.route('/')
def homepage():
    """Redirect to /register"""

    return redirect('/register')


@app.route('/register')
def register():
    """Show registration form"""

    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register_user():
    """Register user then redirect to /secret"""


@app.route('/login')
def login():
    return render_template("login-form.html")


@app.route('/login', methods=['POST'])
def login_user():
    return redirect('/secret')


@app.route('/secret')
def secret_page():
    """Return the text You made it!"""

    return render_template('secret.html')
