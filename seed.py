from app import app, db
from models import Product, Location, ProductMovement

with app.app_context():
    db.drop_all()
    db.create_all()

    # Products
    p1 = Product(product_id="P1", name="Laptop")
    p2 = Product(product_id="P2", name="Mouse")
    p3 = Product(product_id="P3", name="Keyboard")

    # Locations
    l1 = Location(location_id="L1", name="Warehouse A")
    l2 = Location(location_id="L2", name="Warehouse B")

    db.session.add_all([p1, p2, p3, l1, l2])
    db.session.commit()

    # Movements
    moves = [
        ProductMovement(product_id="P1", to_location="L1", qty=10),
        ProductMovement(product_id="P2", to_location="L1", qty=25),
        ProductMovement(product_id="P1", from_location="L1", to_location="L2", qty=2),
        ProductMovement(product_id="P3", to_location="L2", qty=15),
    ]
    db.session.add_all(moves)
    db.session.commit()

    print("✅ Database seeded with test data!")
