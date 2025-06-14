from app import db


class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    image_path = db.Column(db.String)
    price = db.Column(db.Float)
    env_impact = db.Column(db.String)
