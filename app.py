from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from utils.data_reader import get_products

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.sqlite3"
db = SQLAlchemy(app)
products = get_products()


@app.route("/")
def route_index():
    return render_template("index.html", products=products)


if __name__ == "__main__":
    app.run(debug=True)
