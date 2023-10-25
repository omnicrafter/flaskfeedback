from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import connect_db, db, User
from forms import UserForm, RegistrationForm, LoginForm


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


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Show registration form/Process Registration Form and send to /secret"""
    form = RegistrationForm()
    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data

        u = User.register(username, password)
        hashed_pw = u.password

        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User(username=username, password=hashed_pw,
                        email=email, first_name=first_name, last_name=last_name)
        db.session.add(new_user)
        db.session.commit()
        session['user_id'] = new_user.id
        flash(f"Thanks for signing up, {form.username.data}!")

        return redirect('/secret')
    else:
        return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            flash(f'Welcome Back, {user.username}!')
            session['user_id'] = user.id
            return redirect('/secret')
        else:
            form.username.errors = ['Invalid username/password']

    return render_template("login.html", form=form)


@app.route('/secret')
def secret_page():
    """Return the text You made it!"""
    if 'user_id' not in session:
        flash('Please log in to view this page')
        return redirect('/login')

    return render_template('secret.html')


@app.route('/logout')
def logout_user():
    """Clear session to log out user"""

    session.pop('user_id')
    flash('bye bye')
    return redirect('/')
