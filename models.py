from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Shipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tracking_code = db.Column(db.String(20), unique=True, nullable=False)
    sender_name = db.Column(db.String(100))
    sender_contact = db.Column(db.String(100))
    receiver_name = db.Column(db.String(100))
    receiver_contact = db.Column(db.String(100))
    takeoff_location = db.Column(db.String(200))
    current_location = db.Column(db.String(200))
    destination = db.Column(db.String(200))
    status = db.Column(db.String(50))
    expected_delivery = db.Column(db.DateTime)
    item_description = db.Column(db.String(255))
