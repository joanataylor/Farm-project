from flask_app import app, bcrypt
from flask import render_template, request, redirect, session, flash

from flask_app.models.user_model import User


@app.route("/")
@app.route("/dashboard")
def register():
    return render_template('dashboard.html')

@app.route("/login")
def login():
    return render_template('login.html')


# *******- Check login credentials, creates user session - moves to next page -****************
@app.route("/login", methods=["POST"])
def login_user():

    logged_in_user = User.validate_login(request.form)
    
    if not logged_in_user:
        return redirect("/login")

    session['uid'] = logged_in_user.id
    session['fname'] = logged_in_user.first_name

    return redirect('/dashboard')

# *******- Checks to see if user in session before welcoming to new page -****************
@app.route("/register")
def welcome():
    # if not 'uid' in session:
    #     flash("ACCESS DENIED. User not logged in.")
    #     return redirect("/register")
    return render_template("index.html")


# *******- Registers a new user -****************

@app.route('/new_user', methods=['POST'])
def new_user():


    register_check = User.validate(request.form)
    if not register_check:
        return redirect('/register')

    hash = bcrypt.generate_password_hash(request.form['password'])

    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": hash
    }

    User.register(data)
    return redirect("/login")


# *******- Clears user from session (logout) -****************
@app.route("/logout")
def logout():
    session.clear()
    return redirect('/login')
