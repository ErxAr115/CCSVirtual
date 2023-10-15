from flask import Flask
from routes.site_routes import site
app = Flask(__name__)
app.register_blueprint(site)