from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt(app)

@app.route('/')
def index_page():
    #Render the Homepage.
    return render_template('index.html')


@app.route('/register/user', methods=['POST'])
def register_user():
    #Registers the user in the DB based on form data.
    email = request.form['email']
    # Checks if email already exists in the database
    if User.get_by_email({'email': email}):
        flash("Email already in use.", 'register')
        return redirect('/')
    
    #Handles validation of registration.
    if not User.validate_user(request.form):
        return redirect('/')
    
    #Hashes the password before saving in DB.
    hashed_password = bcrypt.generate_password_hash(request.form['password'])
    #Prepares dictionary with hashed password for DB save
    data = {
        "first_name": request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        "password" : hashed_password}
    #Saves user in DB.
    user_id = User.save_user(data)
    #Adds user id to session data
    session['user_id'] = user_id
    flash('Registration successful.', 'register')

    return redirect("/dashboard")


@app.route('/login', methods=['POST'])
def login():
    #Handels user login.
    #Prepares dictionary for email query.
    data = { "email" : request.form["email"] }
    #Gets user data based on email.
    user_in_db = User.get_by_email(data)
    #Checks if user is in DB.
    if not user_in_db:
        flash("Invalid Email/Password", 'login')
        return redirect("/")
    #Checks if password matches DB.
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password", 'login')
        return redirect('/')
    #Adds user id to session data.
    session['user_id'] = user_in_db.id

    return redirect("/dashboard")


@app.route('/dashboard')
def dashboard_page():
    #Checks if user id is logged in.
    if session.get('user_id') is None:
        return redirect('/')
    #Gets user info by id in session.
    user = User.get_by_id({'id': session['user_id']})
    recipes = Recipe.get_all_recipes()

    return render_template('recipes.html', user=user, recipes = recipes)


@app.route('/logout')
def user_logout():
    #Clears session and redirects to homepage.
    session.clear()

    return redirect('/')