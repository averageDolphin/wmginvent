from flask import Flask, render_template, request, jsonify
from flask_login import LoginManager, login_required, current_user
from routes.product_routes import product_routes
from routes.order_routes import order_routes
from routes.report_routes import report_routes
from routes.auth_routes import auth_routes
from models.user import User
import csv


app = Flask(__name__)

app.register_blueprint(product_routes)
app.register_blueprint(order_routes)
app.register_blueprint(report_routes)
app.register_blueprint(auth_routes)

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)

@app.route("/reports")
@login_required
def reports():
    return render_template("reports.html", user=current_user)

@app.route("/orders")
@login_required
def orders():
    if request.accept_mimetypes.best == "application/json" or "curl" in request.user_agent.string:
        return jsonify({"error": "Unauthorized, login required"}), 401
    return render_template("order_list.html")

@app.route("/products")
@login_required
def products():
    return render_template("product_list.html")

@app.route("/user-management")
@login_required
def user_management():
    return render_template("user_management.html")

@app.route("/settings")
@login_required
def settings():
    return render_template("settings.html")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth_routes.login"
app.config['SECRET_KEY'] = 'supersecretkey'  
app.config['SESSION_TYPE'] = 'filesystem'  
app.config['SESSION_PERMANENT'] = False 
app.config['SESSION_COOKIE_HTTPONLY'] = True 
app.config['SESSION_COOKIE_SECURE'] = False 


def load_users_from_csv(file_path):
    users = {}
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            user = User(id=row['id'], username=row['username'], password=row['password'], role=row['role'])
            users[row['username']] = user
    return users

USERS = load_users_from_csv('data/users.csv')

@login_manager.user_loader
def load_user(user_id):
    for user in USERS.values():
        if user.get_id() == user_id:
            return user
    return None

if __name__ == "__main__":
    app.run(debug=True)
