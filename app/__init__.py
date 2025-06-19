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
    folium_map = folium.Map(  location=[40.7128, -74.0060], zoom_start=3,min_zoom=3)

    places = [
        {"location": [40.7128, -74.0060], "title": "New York", "images": [ "https://media.cntraveler.com/photos/5fc6818f3cfe1de2cab79372/4:3/w_4000,h_3000,c_limit/Amsterdam-GettyImages-840603854.jpg"]},
        {"location": [34.0522, -118.2437], "title": "Los Angeles", "images": []},
        {"location": [51.5074, -0.1278], "title": "London", "images": [           
            "https://media.cntraveler.com/photos/5fc6818f3cfe1de2cab79372/4:3/w_4000,h_3000,c_limit/Amsterdam-GettyImages-840603854.jpg",
            "https://media.cntraveler.com/photos/5fc6818f3cfe1de2cab79372/4:3/w_4000,h_3000,c_limit/Amsterdam-GettyImages-840603854.jpg",
            "https://media.cntraveler.com/photos/5fc6818f3cfe1de2cab79372/4:3/w_4000,h_3000,c_limit/Amsterdam-GettyImages-840603854.jpg"
        ]},
    ]

    add_markers(folium_map, places)

    folium_map.get_root().html.add_child(folium.Element(render_template("map_header.html", title="Places I've Visited", description="Explore the world through my travels!", url=os.getenv("URL"))))
    map_html = folium_map.get_root().render()
    return render_template('map.html', map_html=map_html, url=os.getenv("URL"))


def add_markers(fmap, places):
    for place in places:
        popupContent = render_template("popup.html", title=place["title"], images=place.get("images", []), url=os.getenv("URL"))
        
        imgs_count = len(place.get("images", []))
        if imgs_count == 0:
            popup = folium.Popup(popupContent, max_width=300)
        else:
            popup = folium.Popup(popupContent, min_width=300)

        marker = folium.Marker(
            location=place["location"],
            tooltip=place["title"],
            popup=popup,
            icon=folium.Icon(icon="star", color="orange", prefix='fa')
        )
        marker.add_to(fmap)