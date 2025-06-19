from flask import Flask, render_template, request, make_response
from utils.data_reader import read_json
from utils.db_tools import fill_db
from models.db import db, Users, Product, Link, Basket


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.sqlite3"
db.init_app(app)

with app.app_context():
    fill_db(read_json("./data/products.json"), Product)


@app.route("/")
def route_index():
    products = Product.query.all()
    return render_template("index.html", products=products)


@app.route("/product/<int:product_id>")
def route_product(product_id):
    products = Product.query.all()
    return render_template("product.html", product=products[product_id - 1])


@app.route("/basket")
def route_basket():
    return render_template("basket.html")


@app.route("/checkout")
def route_checkout():
    return render_template("checkout.html")


@app.route("/account")
def route_account():
    return render_template("account.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if (
        request.method == "POST"
        and "username" in request.form
        and "password" in request.form
    ):
        username = request.form["username"]
        password = request.form["password"]

        with app.app_context():
            user = Users.query.filter_by(username=username).first()

            if user:
                resp = make_response("User already exists.")
            else:
                db.session.add(Users(username=username, password=password))
                db.session.commit()
                resp = make_response("Logged in.")
    return resp


if __name__ == "__main__":
    app.run(debug=True)
