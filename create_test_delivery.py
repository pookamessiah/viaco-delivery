from app import db
from models import Delivery

new_delivery = Delivery(
    tracking_id="VIA6728DF",
    sender_name="David Nowak",
    receiver_name="Agnieszka Zaremba",
    status="In Transit",
    origin="London",
    destination="Leszka Bialego 9 m26 Łódź, 92-414 Poland.",
    current_location="Warsaw Chopin Airport in Poland",
    expected_delivery="2025-07-29",
    package_details="iPhone 15 Pro Max and Gifts"
)

db.session.add(new_delivery)
db.session.commit()
print("✅ Test delivery added")
