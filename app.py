from flask import Flask, render_template
from routes.product_routes import product_routes
from routes.order_routes import order_routes
from routes.report_routes import report_routes

app = Flask(__name__)

app.register_blueprint(product_routes)
app.register_blueprint(order_routes)
app.register_blueprint(report_routes)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/products")
def products():
    return render_template("product_list.html")

@app.route("/orders")
def orders():
    return render_template("order_list.html")

@app.route("/reports")
def reports():
    return render_template("reports.html")

@app.route("/user-management")
def user_management():
    return render_template("user_management.html")

@app.route("/settings")
def settings():
    return render_template("settings.html")

if __name__ == "__main__":
    app.run(debug=True)
