import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
from pathlib import Path
import json

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
    return render_template('hobbies.html', title="Hobbies", url=os.getenv("URL"))

@app.route('/education')
def education():
    return render_template('education.html', title="Education", url=os.getenv("URL"))

@app.route('/map')
def map():
    return render_template('map.html', title="Map", url=os.getenv("URL"))
