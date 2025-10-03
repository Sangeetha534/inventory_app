from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Product(db.Model):
    __tablename__ = "product"
    product_id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Location(db.Model):
    __tablename__ = "location"
    location_id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class ProductMovement(db.Model):
    __tablename__ = "product_movement"
    movement_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    from_location = db.Column(db.String(50), db.ForeignKey("location.location_id"), nullable=True)
    to_location = db.Column(db.String(50), db.ForeignKey("location.location_id"), nullable=True)
    product_id = db.Column(db.String(50), db.ForeignKey("product.product_id"), nullable=False)
    qty = db.Column(db.Integer, nullable=False)
