from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import db, Shipment
from datetime import datetime
import os

app = Flask(__name__)

# Use PostgreSQL if DATABASE_URL is set (Render sets this automatically)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'sqlite:///shipment.db'
).replace('postgres://', 'postgresql://')
print("⚠️ Using DB:", app.config['SQLALCHEMY_DATABASE_URI'])

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'secretkey')

db.init_app(app)

# ✅ STEP 5: Initialize database tables
with app.app_context():
    db.create_all()
    print("✅ Database tables created (if not already present).")


def shipment_to_dict(s: Shipment):
    """Return a JSON-serializable dict for a Shipment."""
    return {
        "tracking_code": s.tracking_code,
        "sender_name": s.sender_name,
        "sender_contact": s.sender_contact,
        "receiver_name": s.receiver_name,
        "receiver_contact": s.receiver_contact,
        "takeoff_location": s.takeoff_location,
        "current_location": s.current_location,
        "destination": s.destination,
        "status": s.status,
        "expected_delivery": s.expected_delivery.strftime('%Y-%m-%d') if s.expected_delivery else None,
        "item_description": s.item_description
    }


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/track', methods=['GET', 'POST'])
def track():
    tracking_code = None
    as_json = request.args.get('json') == '1'

    if request.method == 'POST':
        tracking_code = request.form.get('tracking_code')
    else:
        tracking_code = request.args.get('q')

    if not tracking_code:
        return render_template('index.html')

    shipment = Shipment.query.filter_by(tracking_code=tracking_code).first()
    if not shipment:
        if as_json:
            return jsonify({"error": "Tracking code not found."}), 404
        return render_template('track.html', error="Tracking code not found.")

    if as_json:
        return jsonify(shipment_to_dict(shipment))

    return render_template('track.html', shipment=shipment)


@app.route('/track/<tracking_code>', methods=['GET'])
def track_direct(tracking_code):
    as_json = request.args.get('json') == '1'
    shipment = Shipment.query.filter_by(tracking_code=tracking_code).first()
    if not shipment:
        if as_json:
            return jsonify({"error": "Tracking code not found."}), 404
        return render_template('track.html', error="Tracking code not found.")
    if as_json:
        return jsonify(shipment_to_dict(shipment))
    return render_template('track.html', shipment=shipment)


@app.route('/admin')
def admin():
    shipments = Shipment.query.order_by(Shipment.id.desc()).all()
    return render_template('admin.html', shipments=shipments)


@app.route('/admin/add', methods=['POST'])
def add_shipment():
    data = request.form
    expected_delivery_raw = data.get('expected_delivery', '').strip()
    expected_delivery = None
    if expected_delivery_raw:
        try:
            expected_delivery = datetime.strptime(expected_delivery_raw, '%Y-%m-%d')
        except ValueError:
            expected_delivery = None

    shipment = Shipment(
        tracking_code=data.get('tracking_code'),
        sender_name=data.get('sender_name'),
        sender_contact=data.get('sender_contact'),
        receiver_name=data.get('receiver_name'),
        receiver_contact=data.get('receiver_contact'),
        takeoff_location=data.get('takeoff_location'),
        current_location=data.get('current_location'),
        destination=data.get('destination'),
        status=data.get('status'),
        expected_delivery=expected_delivery,
        item_description=data.get('item_description')
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
        shipment.sender_name = request.form.get('sender_name')
        shipment.sender_contact = request.form.get('sender_contact')
        shipment.receiver_name = request.form.get('receiver_name')
        shipment.receiver_contact = request.form.get('receiver_contact')
        shipment.takeoff_location = request.form.get('takeoff_location')
        shipment.current_location = request.form.get('current_location')
        shipment.destination = request.form.get('destination')
        shipment.status = request.form.get('status')

        expected_delivery_raw = request.form.get('expected_delivery', '').strip()
        if expected_delivery_raw:
            try:
                shipment.expected_delivery = datetime.strptime(expected_delivery_raw, '%Y-%m-%d')
            except ValueError:
                pass
        else:
            shipment.expected_delivery = None

        shipment.item_description = request.form.get('item_description')
        db.session.commit()
        return redirect(url_for('admin'))

    return render_template('edit_delivery.html', shipment=shipment)


@app.route('/admin/delete/<tracking_code>', methods=['POST'])
def delete_shipment(tracking_code):
    shipment = Shipment.query.filter_by(tracking_code=tracking_code).first()
    if not shipment:
        return redirect(url_for('admin'))
    db.session.delete(shipment)
    db.session.commit()
    return redirect(url_for('admin'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
# Create tables automatically if they don't exist
with app.app_context():
    db.create_all()
