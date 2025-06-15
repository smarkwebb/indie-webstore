from flask import Flask, render_template
from models.products import Product
from utils.data_reader import read_json
from utils.db_tools import fill_db
from models.db import db


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.sqlite3"
db.init_app(app)

with app.app_context():
    fill_db(read_json("./data/products.json"), Product)


@app.route("/")
def route_index():
    products = Product.query.all()
    return render_template("index.html", products=products)


@app.route("/product/<productId>")
def route_product(productId):
    products = Product.query.all()
    return render_template("product.html", product=products[productId])


if __name__ == "__main__":
    app.run(debug=True)
