from flask import Flask
from models import db
from config import Config
from routes import init_routes

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()

# Register routes
init_routes(app)

if __name__ == "__main__":
    from waitress import serve
    print("✅ Running with Waitress on http://127.0.0.1:5000")
    serve(app, host="0.0.0.0", port=5000)
