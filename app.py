from flask import Flask, render_template, request, make_response
from utils.data_reader import read_json
from os import path
from models.db import db, Users, Product, Basket


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.sqlite3"
db.init_app(app)


with app.app_context():
    db.create_all()
    products = read_json("data/products.json")

    for product in products:
        query = Product.query.filter_by(**product).first()

        if not query:
            db.session.add(Product(**product))
    db.session.commit()


@app.route("/")
def route_index():
    products = Product.query.all()
    return render_template("index.html", products=products)


@app.route("/product/<int:product_id>")
def route_product(product_id):
    products = Product.query.all()
    return render_template("product.html", product=products[product_id - 1])


@app.route("/added", methods=["GET", "POST"])
def add_to_cart():
    if request.method == "POST":
        user_id = request.cookies.get("user")
        product_id = request.form["product_id"]
        name = request.form["name"]
        price = request.form["price"]
        quantity = request.form["quantity"]

        with app.app_context():
            if not user_id:
                resp = make_response("You must be logged in to perform this action.")
            else:
                db.session.add(
                    Basket(
                        user_id=user_id,
                        product_id=product_id,
                        name=name,
                        price=price,
                        quantity=quantity,
                    )
                )
                resp = make_response("Added to cart.")
                db.session.commit()
    return resp


@app.route("/basket")
def route_basket():
    user = request.cookies.get("user")
    baskets = Basket.query.filter_by(user_id=user)
    products = Product.query.all()
    total_price = 0

    for basket in baskets:
        total_price += basket.price * basket.quantity

    return render_template(
        "basket.html", baskets=baskets, products=products, total_price=total_price
    )


@app.route("/removed", methods=["GET", "POST"])
def remove_from_cart():
    if request.method == "POST":
        basket_id = request.form["basket_id"]
        my_basket = db.session.get(Basket, basket_id)
        db.session.delete(my_basket)
        resp = make_response("Removed from cart.")
        db.session.commit()
    return resp


@app.route("/removed_all", methods=["GET", "POST"])
def remove_all_from_cart():
    if request.method == "POST":
        user = request.cookies.get("user")
        baskets = Basket.query.filter_by(user_id=user)

        for basket in baskets:
            db.session.delete(basket)

        resp = make_response("Removed all items from cart")
        db.session.commit()
    return resp


@app.route("/checkout")
def route_checkout():
    return render_template("checkout.html")


@app.route("/validated", methods=["GET", "POST"])
def validate_checkout():
    if request.method == "POST":
        first_name = request.form.get("first_name", "").strip()
        surname = request.form.get("surname", "").strip()
        card_number = request.form.get("card_number", "").strip()
        security_code = request.form.get("security_code", "").strip()
        exp_month = request.form.get("exp_month", "").strip()
        exp_year = request.form.get("exp_year", "").strip()

        if any(
            x == ""
            for x in [
                first_name,
                surname,
                card_number,
                security_code,
                exp_month,
                exp_year,
            ]
        ):
            return make_response("Fields cannot be empty.")

        clean_card_number = card_number.replace("-", "").replace(" ", "")

        if not clean_card_number.isdigit():
            return make_response("Card number must contain only numbers.")

        if len(clean_card_number) != 12:
            return make_response("Card number must be be 12 digits.")

        if not security_code.isdigit():
            return make_response("Security code must only contain numbers.")

        if not exp_month.isdigit():
            return make_response("Expiry month must only contain numbers.")

        if not exp_year.isdigit():
            return make_response("Expiry year must only contain numbers.")

        return make_response("Payment processed successfully!")


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
                resp = make_response("Account created.")
    return resp


@app.route("/login", methods=["GET", "POST"])
def login():
    if (
        request.method == "POST"
        and "username" in request.form
        and "password" in request.form
    ):
        username = request.form["username"]
        password = request.form["password"]

        with app.app_context():
            user = Users.query.filter_by(username=username).first()

            if not user:
                resp = make_response("User does not exist.")
            elif user.password == password:
                resp = make_response("Welcome User!")
                resp.set_cookie("user", str(user.user_id))
            else:
                resp = make_response("Invalid username or password.")
        return resp


if __name__ == "__main__":
    app.run(debug=True, port=8000)
