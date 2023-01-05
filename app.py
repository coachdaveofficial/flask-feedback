from flask import Flask, request, redirect, render_template, flash, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
from secret import secret
from models import db, connect_db, User
from forms import UserForm, LoginForm
from sqlalchemy.exc import IntegrityError
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask-feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = secret
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


app.app_context().push()
connect_db(app)

db.create_all()

@app.route('/')
def homepage():
    return redirect('/register')

@app.route('/register', methods=["GET", "POST"])
def get_register_form():
    form = UserForm()

    if not form.validate_on_submit():
        return render_template('register.html', form=form)

    username = form.username.data
    password = form.password.data
    email = form.email.data
    first_name = form.first_name.data
    last_name = form.last_name.data


    user = User.register(username, password, email, first_name, last_name)
    
    

    

    if user:
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("Username already exists... please try again.", "error")
            return redirect('/register')

        session["username"] = user.username  # keep logged in
        return redirect(f'/users/{user.username}')

@app.route('/login', methods=["GET", "POST"])
def get_login_form():
    form = LoginForm()

    if not form.validate_on_submit():
        return render_template('login.html', form=form)
    
   

    user = User.authenticate(form.username.data, form.password.data)
    


    if user:
        session["username"] = user.username  # keep logged in
        return redirect(f'/users/{user.username}')
    
    flash("Invalid login... please try again.", "error")
    return render_template('login.html', form=form)

        

@app.route('/secret')
def show_secret():
    if "username" not in session:
        flash("You must be logged in to view!")
        return redirect("/")

    return render_template('secret.html')

@app.route("/logout")
def logout():
    """Logs user out and redirects to homepage."""

    session.pop("username")

    return redirect("/")

@app.route('/users/<string:username>')
def get_user_details(username):
    if "username" not in session:
        flash("You must be logged in to view!", "error")
        return redirect("/login")

    user = User.query.get_or_404(username)

    return render_template('user_details.html', user=user)