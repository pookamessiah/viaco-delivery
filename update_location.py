from flask import Flask
from model import db, Shipment

app = Flask(__name__)

# Make sure this matches your Render DATABASE_URL
import os
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    tracking_code = "HGVGgjF576"  # Replace with your real code
    shipment = Shipment.query.filter_by(tracking_code=tracking_code).first()
    
    if shipment:
        print(f"✅ Found shipment: {shipment.tracking_code}")
        shipment.current_location = "Warsaw"  # Change to new location
        db.session.commit()
        print("✅ Current location updated to:", shipment.current_location)
    else:
        print("❌ Shipment not found.")
