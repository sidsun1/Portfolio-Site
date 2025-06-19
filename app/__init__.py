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
    m = folium.Map(  location=[40.7128, -74.0060], zoom_start=3,min_zoom=3)

    # Adding markers with title
    folium.Marker(
        location=[45.3288, -121.6625],
        tooltip="Mount Hood",
        popup=getPopupContent("Mount Hood"),
        icon=folium.Icon(icon="cloud"),
    ).add_to(m)

    # Adding another marker different icon
    folium.Marker(
        location=[47.6062, -122.3321],
        tooltip="Seattle",
        popup=getPopupContent("Seattle", image_url=[
            "https://media.cntraveler.com/photos/5fc6818f3cfe1de2cab79372/4:3/w_4000,h_3000,c_limit/Amsterdam-GettyImages-840603854.jpg"]),
        icon=folium.Icon(icon="star", color="orange", prefix='fa'),
    ).add_to(m)
    
    # another marker with images
    folium.Marker(
        location=[34.0522, -118.2437],
        tooltip="Los Angeles",
        popup=getPopupContent("Los Angeles", image_url=[
            "https://media.cntraveler.com/photos/5fc6818f3cfe1de2cab79372/4:3/w_4000,h_3000,c_limit/Amsterdam-GettyImages-840603854.jpg",
            "https://media.cntraveler.com/photos/5fc6818f3cfe1de2cab79372/4:3/w_4000,h_3000,c_limit/Amsterdam-GettyImages-840603854.jpg",
            "https://media.cntraveler.com/photos/5fc6818f3cfe1de2cab79372/4:3/w_4000,h_3000,c_limit/Amsterdam-GettyImages-840603854.jpg"
            ]),
        icon=folium.Icon(color="green"),
    ).add_to(m)

    
    m.get_root().html.add_child(folium.Element(setMapDetails(
        title="My Travel Map",
        description="Explore the places I've visited and the experiences I've had."))
        )

    map_html = m.get_root().render()
    return render_template('map.html', map_html=map_html, url=os.getenv("URL"))

# Function to set map details
def setMapDetails(title, description):
    with open(os.path.join(os.path.dirname(__file__), 'static', 'styles', 'map.css')) as f:
        style = f'<style>{f.read()}</style>'
    title_html = f'''
    {style}
    <div class="map-details">
        <h2>{title}</h2>
        <p>{description}</p>
    </div>
    '''
    return title_html

# Function to create a popup with images and title
def getPopupContent(title, image_url=[], size=100):
    html = f'''<h4 style="text-align: center; margin-bottom: 10px;">{title}</h4>'''

    count = len(image_url)
    if count == 0:
        return folium.Popup(html, max_width=300)

    # set up grid layout for images
    columns = min(3, count)
    html += f'<div style="display: grid; grid-template-columns: repeat({columns}, 1fr); gap: 5px;">'
    for url in image_url:
        html += f'''
        <img src="{url}" width="{size}" height="{size}" 
        style="border-radius: 10px; object-fit: cover;">'''
    html += '</div>'

    rows = (count + 2) // 3 
    title_height = 50 
    iframe_width = columns * size + (columns - 1) * 5 + 20
    iframe_height = rows * size + (rows - 1) * 5 + title_height

    iframe = folium.IFrame(html=html, width=iframe_width, height=iframe_height)
    popup = folium.Popup(iframe)
    return popup
