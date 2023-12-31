from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import connect_db, db, User, Feedback
from forms import UserForm, RegistrationForm, LoginForm, FeedbackForm
from sqlalchemy.exc import IntegrityError


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
    """Redirect to /login"""

    return redirect('/login')


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
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username Taken')
            return render_template('register.html', form=form)

        session['user_id'] = new_user.id
        flash(f"Thanks for signing up, {form.username.data}!", "success")

        return redirect('/secret')
    else:
        return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(f"/users/{session['user_id']}")
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            flash(f'Welcome Back, {user.username}!', 'primary')
            session['user_id'] = user.id
            return redirect(f'/users/{user.id}')
        else:
            form.username.errors = ['Invalid username/password']

    return render_template("login.html", form=form)


@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show user info"""
    if 'user_id' not in session:
        flash('Please log in to view this page', 'danger')
        return redirect('/login')

    user = User.query.get_or_404(user_id)
    feedbacks = Feedback.query.filter_by(user_id=user_id).all()
    return render_template('user.html', user=user, feedbacks=feedbacks)


@app.route('/secret')
def secret_page():
    """Return the text You made it!"""
    if 'user_id' not in session:
        flash('Please log in to view this page', 'danger')
        return redirect('/login')

    return render_template('secret.html')


@app.route('/logout')
def logout_user():
    """Clear session to log out user"""

    session.pop('user_id')
    flash('bye bye', 'info')
    return redirect('/')


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Delete a user"""

    if 'user_id' in session:
        correct_user = session['user_id']
        user = User.query.get_or_404(correct_user)

        db.session.delete(user)
        db.session.commit()
        session.pop('user_id')
        flash('User has been deleted', 'warning')
        return redirect('/login')
    else:
        flash('You do not have authorization to do this!')
        return redirect('/login')


@app.route('/users/<int:user_id>/feedback/add', methods=['GET', 'POST'])
def add_feedback(user_id):
    """Generate Feedback Form or Process New Feedback"""

    if 'user_id' not in session:
        flash("You don't have access to that page!", 'danger')
        return redirect('/login')

    form = FeedbackForm()
    user = User.query.get_or_404(user_id)

    if form.validate_on_submit():
        correct_user = session['user_id']

        title = form.title.data
        content = form.content.data
        user_id = correct_user

        new_feedback = Feedback(title=title, content=content, user_id=user_id)
        db.session.add(new_feedback)
        db.session.commit()
        flash('Your feedback has been saved!', 'success')
        return redirect(f'/users/{user_id}')
    else:
        return render_template('feedback.html', form=form, user=user)


@app.route('/feedback/<int:feedback_id>/update', methods=['GET', 'POST'])
def update_feedback(feedback_id):
    """Show update form and process feedback updating"""
    feedback = Feedback.query.get(feedback_id)
    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        user_id = session['user_id']
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.commit()
        return redirect(f'/users/{user_id}')

    return render_template('update_feedback.html', form=form, feedback=feedback)


@app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
def deleted_feedback(feedback_id):
    """Delete a Feedback"""

    if 'user_id' not in session:
        flash("Please login first", 'danger')
        return redirect('/login')

    feedback = Feedback.query.get_or_404(feedback_id)
    user_id = session['user_id']

    if feedback.user_id == session['user_id']:
        db.session.delete(feedback)
        db.session.commit()
        flash('Feedback deleted!', 'info')
        return redirect(f'/users/{user_id}')

    flash("You do not have permission to do this!", 'danger')
    return redirect(f'/users/{user_id}')
