from flask import Flask, request, render_template, redirect, flash, session
from models import db, connect_db, User, Feedback
from forms import UserRegisterForm, UserLoginForm, FeedbackForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "something_very_secret_here"

connect_db(app)
db.create_all()

@app.route('/')
def index():
    """ Redirect to /register. """
    return render_template('index.html')

@app.route('/register', methods=["GET", "POST"])
def register_user():
    """Renders user register form (GET) or handles user form submission (POST)"""
    form = UserRegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username, password, email, first_name, last_name)
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username taken.  Please pick another')
            return render_template('register_form.html', form=form)
        flash('Welcome! Successfully created your account!', 'primary')
        session["username"] = user.username

        return redirect(f'/users/{username}')
    else:
        return render_template("register_form.html", form=form)  
 

@app.route("/login", methods=["GET", "POST"])
def login():
    """Produce login form or handle login."""

    form = UserLoginForm()


    if form.validate_on_submit():
        name = form.username.data
        password = form.password.data

        # authenticate will return a user or False
        user = User.authenticate(name, password)

        if user:
            session["username"] = user.username  # keep logged in
            flash(f"Welcome back, {user.first_name} {user.last_name}!", 'primary')
            return redirect(f"/users/{user.username}")

        else:
            form.password.errors = ["Invalid name/password"]

    return render_template("login_form.html", form=form)
# end-login    

@app.route("/logout")
def logout():
    """Logs user out and redirects to index page."""


    session.pop("username")
    flash('Goodbye!','primary')

    return redirect("/")

@app.route("/users/<username>")
def user_info(username):
    """Example hidden page for logged-in users only."""

    if "username" not in session:
        flash("You must be logged in to view this page!",'danger')
        return redirect("/")

        # alternatively, can return HTTP Unauthorized status:
        #
        # from werkzeug.exceptions import Unauthorized
        # raise Unauthorized()

    else:
        user=User.query.filter_by(username=username).first()
        return render_template("user_info.html", user=user)

@app.route("/users/<username>/feedback/add", methods = ["GET", "POST"])
def create_feedback(username):
    """ Show feedback form or handle adding a feedback """
    if "username" not in session:
        flash("You must be logged in to view this page!",'danger')
        return redirect("/")
        
    form = FeedbackForm()
    title = form.title.data
    content = form.content.data
    if form.validate_on_submit():
        username = session["username"]
        feedback = Feedback(title=title, content=content, username=username)
        db.session.add(feedback)
        db.session.commit()
        flash('Thank you for your feedback!', 'primary')
        return redirect(f"/users/{username}")

    return render_template("feedback_form.html", form=form)

@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    """ Delete user and clear user info in session """
    user=User.query.get_or_404(username)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash(f'User {session["username"]} deleted','primary')    
        session.pop("username")
    else:
        flash("You have no permission to do that")
    return redirect("/")

@app.route("/feedback/<int:id>/update", methods = ["POST", "GET"])
def update_feedback(id):
    """ Update a specific piece of feedback  """
    
    if "username" not in session:
        flash("You must be logged in to view this page!",'danger')
        return redirect("/")
    feedback = Feedback.query.get_or_404(id)
    form = FeedbackForm(obj=feedback)
    if form.validate_on_submit():
        if feedback.username == session['username']:
            feedback.title = form.title.data
            feedback.content = form.content.data
            db.session.commit()
            flash('Thank you for your feedback!', 'primary')
            return redirect(f"/users/{session['username']}")

    return render_template("feedback_form.html", form=form)


@app.route("/feedback/<int:id>/delete")
def delete_feedback(id):
    """ Delete a specific piece of feedback """
    if 'username' not in session:
        flash("Please login/sign-up first!", "danger")
        return redirect('/')
    feedback=Feedback.query.get_or_404(id) 
    if feedback.username == session['username']:
        db.session.delete(feedback)
        db.session.commit()
        flash('Feedback was deleted','primary')    
    else: flash("You don't have permission to do that!", "danger")
    return redirect(f'/users/{session["username"]}')

