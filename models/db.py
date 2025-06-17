from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Users(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(240), nullable=False)


class Product(db.Model):
    __tablename__ = "products"
    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(500))
    image_path = db.Column(db.String(20))
    price = db.Column(db.Float)
    env_impact = db.Column(db.String(20))


class Link(db.Model):
    __tablename__ = "link"
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), primary_key=True)
    basket_id = db.Column(
        db.Integer, db.ForeignKey("baskets.basket_id"), primary_key=True
    )


class Basket(db.Model):
    __tablename__ = "baskets"
    id = db.Column(db.Integer, primary_key=True)
    basket_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(
        db.Integer, db.ForeignKey("products.product_id"), nullable=False
    )
    quantity = db.Column(db.Integer)
