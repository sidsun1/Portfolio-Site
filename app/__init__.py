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
    return render_template('education.html', title="Hobbies", url=os.getenv("URL"))

@app.route('/map')
def map():
    return render_template('map.html', title="Hobbies", url=os.getenv("URL"))
