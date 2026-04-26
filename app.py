from flask import Flask
from flask_cors import CORS
from config import Config
from database import db

from routes.admin_routes import admin_bp
from routes.otp_routes import otp_bp
from routes.student_routes import student_bp

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)

db.init_app(app)

app.register_blueprint(admin_bp, url_prefix="/api/admin")
app.register_blueprint(otp_bp, url_prefix="/api/otp")
app.register_blueprint(student_bp, url_prefix="/api/student")

@app.route("/")
def home():
    return {
        "message": "Smart Hostel Backend Running"
    }

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)