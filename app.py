from flask import Flask, render_template, request, redirect, url_for
from models import db, Shipment
from datetime import datetime
import os

app = Flask(__name__)

# Use PostgreSQL if DATABASE_URL is set (Render sets this automatically)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///shipment.db').replace('postgres://', 'postgresql://')
print("⚠️ Using DB:", app.config['SQLALCHEMY_DATABASE_URI'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secretkey'

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/track', methods=['POST'])
def track():
    tracking_code = request.form['tracking_code']
    shipment = Shipment.query.filter_by(tracking_code=tracking_code).first()
    if not shipment:
        return render_template('track.html', error="Tracking code not found.")
    return render_template('track.html', shipment=shipment)

@app.route('/admin')
def admin():
    shipments = Shipment.query.all()
    return render_template('admin.html', shipments=shipments)

@app.route('/admin/add', methods=['POST'])
def add_shipment():
    data = request.form
    shipment = Shipment(
        tracking_code=data['tracking_code'],
        sender_name=data['sender_name'],
        sender_contact=data['sender_contact'],
        receiver_name=data['receiver_name'],
        receiver_contact=data['receiver_contact'],
        takeoff_location=data['takeoff_location'],
        current_location=data['current_location'],
        destination=data['destination'],
        status=data['status'],
        expected_delivery=datetime.strptime(data['expected_delivery'], '%Y-%m-%d'),
        item_description=data['item_description']
    )
    db.session.add(shipment)
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/admin/edit/<tracking_code>', methods=['GET', 'POST'])
def edit_delivery(tracking_code):
    shipment = Shipment.query.filter_by(tracking_code=tracking_code).first()
    if not shipment:
        return "Shipment not found", 404

    if request.method == 'POST':
        shipment.sender_name = request.form['sender_name']
        shipment.sender_contact = request.form['sender_contact']
        shipment.receiver_name = request.form['receiver_name']
        shipment.receiver_contact = request.form['receiver_contact']
        shipment.takeoff_location = request.form['takeoff_location']
        shipment.current_location = request.form['current_location']
        shipment.destination = request.form['destination']
        shipment.status = request.form['status']
        shipment.expected_delivery = datetime.strptime(request.form['expected_delivery'], '%Y-%m-%d')
        shipment.item_description = request.form['item_description']
        db.session.commit()
        return redirect(url_for('admin'))

    return render_template('edit_delivery.html', shipment=shipment)

if __name__ == '__main__':
    app.run(debug=True)
