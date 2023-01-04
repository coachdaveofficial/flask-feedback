from flask import Flask, request, redirect, render_template, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from secret import secret
from models import db, connect_db, User
from forms import UserForm, LoginForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask-feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = secret

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
        db.session.add(user)
        db.session.commit()
        return redirect('/secret')

@app.route('/login', methods=["GET", "POST"])
def get_login_form():
    form = LoginForm()

    if not form.validate_on_submit():
        return render_template('login.html', form=form)
    
   

    user = User.authenticate(form.username.data, form.password.data)

    if user:
        return user.username
        return redirect('/secret')

        

@app.route('/secret')
def show_secret():
    return render_template('secret.html')