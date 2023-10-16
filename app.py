from flask import Flask
from routes.site_routes import site
from routes.chatbot_routes import chatbot
app = Flask(__name__)
app.register_blueprint(site)
app.register_blueprint(chatbot)