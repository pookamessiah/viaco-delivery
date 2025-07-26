from app import db
from models import Delivery

new_delivery = Delivery(
    tracking_id="ABC123456",
    sender_name="Admin",
    receiver_name="Customer",
    status="In Transit",
    origin="London",
    destination="Lagos",
    current_location="Paris",
    expected_delivery="2025-07-30",
    package_details="iPhone 15 Pro"
)

db.session.add(new_delivery)
db.session.commit()
print("✅ Test delivery added")
