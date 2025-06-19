import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
import folium

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
    m = folium.Map(
        location=[45.35, -121.6972],
        zoom_start=3,
        min_zoom=3
    )
    
    folium.Marker(
        location=[45.3288, -121.6625],
        tooltip="Click me!",
        popup="Mt. Hood Meadows",
        icon=folium.Icon(icon="cloud"),
    ).add_to(m)

    folium.Marker(
        location=[45.3311, -121.7113],
        tooltip="Click me!",
        popup="Timberline Lodge",
        icon=folium.Icon(color="green"),
    ).add_to(m)

    map_html = m._repr_html_()
    return render_template('map.html', map_html=map_html, title="Map", url=os.getenv("URL"))
