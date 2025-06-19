import os
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', title="Siddharth Sundar", url=os.getenv("URL"))

# TODO: Add respective html files for each sub route below

@app.route('/work')
def work():
    return render_template('work.html', title="Experience", url=os.getenv("URL"))

@app.route('/hobbies')
def hobbies():
    return render_template('hobbies.html', title="Hobbies", url=os.getenv("URL"))

@app.route('/education')
def education():
    return render_template('education.html', title="Education", url=os.getenv("URL"))

@app.route('/map')
def map():
    locations = [
        {"name": "New York", "lat": 40.7128, "lon": -74.0060, "images": ["img1.jpg", "img2.jpg"]},
        {"name": "Los Angeles", "lat": 34.0522, "lon": -118.2437, "images": ["img1.jpg"]},
        {"name": "Chicago", "lat": 41.8781, "lon": -87.6298, "images": ["img1.jpg", "img2.jpg","img3.jpg"]},
    ]

    mapSettings = {
        "customIcon": "static/img/fav_icon.svg",
        "minZoom": 2,
        "maxZoom": 100,
    }
    return render_template('map.html', locations=locations, mapSettings=mapSettings, title="Map", url=os.getenv("URL"))
