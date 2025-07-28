from app import app
from models import db, Delivery

with app.app_context():
    existing = Delivery.query.filter_by(tracking_code="HGVGgjF576").first()
    if existing:
        print("⚠️ Test delivery already exists.")
    else:
        delivery = Delivery(
            tracking_code="HGVGgjF576",
            package="Box of Gifts",
            sender_name="David Nowak",
            sender_phone="+447838319023",
            receiver_name="Agnieszka Zaremba",
            receiver_phone="+64275197241",
            current_location="London",
            takeoff_location="London",
            destination="Poland",
            expected_delivery="2025-07-28",
            status="In Transit"
        )

        db.session.add(delivery)
        db.session.commit()
        print("✅ Test delivery added.")
