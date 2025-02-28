from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session, make_response
from flask_login import login_user, logout_user, login_required, current_user
from models.user import User

auth_routes = Blueprint("auth_routes", __name__)

USERS = {
    "admin": User(id=1, username="admin", password="password123", role="admin"),
    "user": User(id=2, username="user", password="userpass", role="user")
}

@auth_routes.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = USERS.get(username)

        if user and user.password == password:
            login_user(user)
            return redirect(url_for("dashboard"))  # Redirect to an existing route

        flash("Invalid username or password", "danger")

    return render_template("login.html") 


@auth_routes.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()  # Logs out user from Flask-Login
    session.clear()  # Clears all session data
    
    # Manually remove the session cookie
    response = make_response(redirect(url_for('auth_routes.login')))
    response.set_cookie('session', '', expires=0)  # Delete session cookie
    response.set_cookie('remember_token', '', expires=0)  # Delete Flask-Login remember token
    return response


