from flask import Blueprint, send_file

site = Blueprint('site', __name__)

@site.route('/')
def home():
    return send_file('static/home.html')