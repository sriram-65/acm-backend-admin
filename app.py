# #NPRCET@ACM

from flask import Flask
from routes.Eroutes import ERoutes
from routes.AuthRoutes import AuthRoutes
from routes.GalleryRoutes import GalleryRoutes
from routes.RecentEvents import RecentEvents
from routes.OutReach import OutReach
from flask_cors import CORS
from dotenv import load_dotenv
from datetime import timedelta
import os

app = Flask(__name__)

# ----------------------------
# Cookie-based session config
# ----------------------------
app.secret_key = os.getenv("SECERT_KEY")
app.permanent_session_lifetime = timedelta(days=50)

app.config.update(
    SESSION_COOKIE_SAMESITE="None", # Needed for cross-origin
    SESSION_COOKIE_SECURE=True,     # HTTPS required
    SESSION_PERMANENT=True
)

# ----------------------------
# CORS setup
# ----------------------------
CORS(app,
     resources={r"/*": {"origins": "https://acm-admin-frontend.vercel.app"}},
     supports_credentials=True)

# ----------------------------
# Load environment variables
# ----------------------------
load_dotenv()

# ----------------------------
# Register Blueprints
# ----------------------------
app.register_blueprint(ERoutes , url_prefix="/api/events")
app.register_blueprint(AuthRoutes , url_prefix="/api/auth")
app.register_blueprint(GalleryRoutes , url_prefix='/api/gallery')
app.register_blueprint(OutReach , url_prefix='/api/outreach')
app.register_blueprint(RecentEvents , url_prefix='/api/recent')

# ----------------------------
# Run the app
# ----------------------------
if __name__ == "__main__":
    app.run(debug=True)
