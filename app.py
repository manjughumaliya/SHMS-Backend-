from flask import Flask
from flask_cors import CORS
from config import Config
from database import db

from routes.admin_routes import admin_bp
from routes.otp_routes import otp_bp
from routes.student_routes import student_bp
from routes.warden_routes import warden_bp
from routes.parent_routes import parent_bp
from routes.entry_exit_routes import entry_exit_bp
from routes.notification_routes import notification_bp
from routes.leave_routes import leave_bp

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)

db.init_app(app)

app.register_blueprint(admin_bp, url_prefix="/api/admin")
app.register_blueprint(otp_bp, url_prefix="/api/otp")
app.register_blueprint(student_bp, url_prefix="/api/student")
app.register_blueprint(warden_bp, url_prefix="/api/warden") 
app.register_blueprint(parent_bp, url_prefix="/api/parent")
app.register_blueprint(entry_exit_bp, url_prefix="/api/entry-exit")
app.register_blueprint(notification_bp, url_prefix="/api/notifications")
app.register_blueprint(leave_bp, url_prefix="/api/leave")

@app.route("/")
def home():
    return {
        "message": "Smart Hostel Backend Running"
    }

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)