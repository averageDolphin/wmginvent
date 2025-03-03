from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session, make_response
from flask_login import login_user, logout_user, login_required, current_user
import csv
from models.user import User

auth_routes = Blueprint("auth_routes", __name__)

def load_users_from_csv(file_path):
    users = {}
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            user = User(id=row['id'], username=row['username'], password=row['password'], role=row['role'])
            users[row['username']] = user
    return users

USERS = load_users_from_csv('data/users.csv')

@auth_routes.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = USERS.get(username)

        # Redirect to dashboard if credentials correct
        if user and user.password == password:
            login_user(user)
            return redirect(url_for("dashboard"))

        flash("Invalid username or password", "danger")

    return render_template("login.html") 


@auth_routes.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()  # Logs out user from Flask-Login
    session.clear()  # Clears all session data
    
    response = make_response(redirect(url_for('auth_routes.login')))
    response.set_cookie('session', '', expires=0)  # Delete session cookie
    response.set_cookie('remember_token', '', expires=0)  # Delete Flask-Login remember token
    return response


