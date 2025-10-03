from flask import render_template, request, redirect, url_for
from models import db, Product, Location, ProductMovement
from sqlalchemy import func

def init_routes(app):
    # ---------------- HOME ----------------
    @app.route("/")
    def home():
        return render_template("base.html")

    # ---------------- PRODUCTS ----------------
    @app.route("/products")
    def view_products():
        products = Product.query.all()
        return render_template("product.html", products=products)

    @app.route("/add_product", methods=["POST"])
    def add_product():
        product_id = request.form["product_id"]
        name = request.form["name"]
        new_product = Product(product_id=product_id, name=name)
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for("view_products"))

    # ---------------- LOCATIONS ----------------
    @app.route("/locations")
    def view_locations():
        locations = Location.query.all()
        return render_template("location.html", locations=locations)

    @app.route("/add_location", methods=["POST"])
    def add_location():
        location_id = request.form["location_id"]
        name = request.form["name"]
        new_location = Location(location_id=location_id, name=name)
        db.session.add(new_location)
        db.session.commit()
        return redirect(url_for("view_locations"))

    # ---------------- MOVEMENTS ----------------
    @app.route("/movements")
    def view_movements():
        movements = ProductMovement.query.all()
        products = Product.query.all()
        locations = Location.query.all()
        return render_template("movement.html", movements=movements, products=products, locations=locations)

    @app.route("/add_movement", methods=["POST"])
    def add_movement():
        product_id = request.form["product_id"]
        from_location = request.form.get("from_location") or None
        to_location = request.form.get("to_location") or None
        qty = int(request.form["qty"])
        new_move = ProductMovement(
            product_id=product_id,
            from_location=from_location,
            to_location=to_location,
            qty=qty
        )
        db.session.add(new_move)
        db.session.commit()
        return redirect(url_for("view_movements"))

    # ---------------- REPORT ----------------
    @app.route("/report")
    def report():
        products = Product.query.all()
        locations = Location.query.all()
        report = []

        for product in products:
            for location in locations:
                incoming = db.session.query(func.sum(ProductMovement.qty)).filter_by(
                    product_id=product.product_id, to_location=location.location_id
                ).scalar() or 0

                outgoing = db.session.query(func.sum(ProductMovement.qty)).filter_by(
                    product_id=product.product_id, from_location=location.location_id
                ).scalar() or 0

                balance = incoming - outgoing
                if balance != 0:
                    report.append({
                        "product": product.name,
                        "location": location.name,
                        "qty": balance
                    })

        return render_template("report.html", report=report)
