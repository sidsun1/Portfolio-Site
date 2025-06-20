import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
from pathlib import Path
import json
import folium

load_dotenv()
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"))

@app.route('/work')
def work():
    path = Path('app/static/json-data/experiences.json')

    try:
        with open(path, 'r', encoding = 'utf-8') as f:
            experiences = json.load(f)
    except Exception as e:
        experiences = []
        print(f'Error loading experiences: {e}')

    # print(experiences)
    
    return render_template('work.html', title="Experience", experiences = experiences, url=os.getenv("URL"))

@app.route('/hobbies')
def hobbies():
    path = Path('app/static/json-data/hobbies.json')

    try:
        with open(path, 'r', encoding='utf-8') as f:
            hobbies = json.load(f)
    except Exception as e:
        hobbies = []
        print(f'Error loading hobbies: {e}')

    return render_template('hobbies.html', title="My Hobbies", description="These are the activities that keep me inspired and energized outside of my professional work.", hobbies=hobbies, url=os.getenv("URL"))

@app.route('/education')
def education():
    return render_template('education.html', title="Education", url=os.getenv("URL"))

@app.route('/map')
def map():
    path = Path('app/static/json-data/places.json')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            places = json.load(f)
    except Exception as e:
        places = []
        print(f'Error loading places: {e}')

    folium_map = folium.Map(location=[40.7128, -74.0060], zoom_start=3, min_zoom=3)
    add_markers(folium_map, places)

    # Save to static file
    map_path = os.path.join("app/static", "maps", "map.html")
    os.makedirs(os.path.dirname(map_path), exist_ok=True)
    folium_map.save(map_path)

    return render_template("map.html", places=places, title="Places I've Visited", description="The amazing places I've been to.", url=os.getenv("URL"))

def add_markers(folium_map, places):
    for place in places:
        marker = folium.Marker(
            location=place["location"],
            tooltip=place["title"],
            popup=folium.Popup(place["title"], max_width=300),
            icon=folium.Icon(icon="star", color="orange", prefix='fa'),
            options={"autoPan": False}
        )
        marker.add_to(folium_map)