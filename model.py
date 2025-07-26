from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Shipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tracking_code = db.Column(db.String(100), unique=True, nullable=False)
    sender_name = db.Column(db.String(100), nullable=False)
    sender_contact = db.Column(db.String(100), nullable=False)
    receiver_name = db.Column(db.String(100), nullable=False)
    receiver_contact = db.Column(db.String(100), nullable=False)
    takeoff_location = db.Column(db.String(100), nullable=False)
    current_location = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(100), nullable=False)
    expected_delivery = db.Column(db.Date, nullable=False)
    item_description = db.Column(db.Text, nullable=False)
