from flask import Flask, render_template
from routes.tv_routes import tv_routes
from routes.order_routes import order_routes

app = Flask(__name__)
app.register_blueprint(tv_routes)
app.register_blueprint(order_routes)


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
