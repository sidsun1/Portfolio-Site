# tests/test_app.py

import unittest
import os
import json
from pathlib import Path
os.environ['TESTING'] = 'true'

from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        about_me_path = Path('app/static/json-data/aboutMe.json')
        with open(about_me_path, 'r', encoding='utf-8') as f:
            about_me_data = json.load(f)
        
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert '<p class="intro">HI THERE!</p>' in html
    
        assert about_me_data["subtitle"] in html
        assert f'https://github.com/{about_me_data["github"]}' in html
        assert f'https://linkedin.com/in/{about_me_data["linkedin"]}' in html
        assert f'https://twitter.com/{about_me_data["twitter"]}' in html

    def test_timeline(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0

        # Page renders correctly
        page_response = self.client.get("/timeline")
        assert page_response.status_code == 200
        html = page_response.get_data(as_text=True)
        assert '<h2 class="timeline__title">Timeline Posts</h2>' in html
        assert'<div class="timeline-posts" id="timelinePosts"></div>' in html

        # Endpoint testing
        post_response= self.client.post("/api/timeline_post", data={
            "name": "John Doe",
            "email": "john@example.com", 
            "content": "Hello world, I'm John!"
        })
        assert post_response.status_code == 200
        post_json = post_response.get_json()
        assert post_json["name"] == "John Doe"
        assert post_json["email"] == "john@example.com"
        assert post_json["content"] == "Hello world, I'm John!"

        get_response = self.client.get("/api/timeline_post")
        assert get_response.status_code == 200
        get_json = get_response.get_json()
        assert len(get_json["timeline_posts"]) == 1
        assert get_json["timeline_posts"][0]["name"] == "John Doe"
        assert get_json["timeline_posts"][0]["email"] == "john@example.com"
        assert get_json["timeline_posts"][0]["content"] == "Hello world, I'm John!"

        delete_response = self.client.delete("/api/timeline_post/1")
        assert delete_response.status_code == 200
        delete_json = delete_response.get_json()
        assert delete_json["result"] == "success"

        get_response_after_delete = self.client.get("/api/timeline_post")
        assert get_response_after_delete.status_code == 200
        get_json_after_delete = get_response_after_delete.get_json()
        assert len(get_json_after_delete["timeline_posts"]) == 0

    def test_malformed_timeline_post(self):
        # POST request missing name
        response = self.client.post("/api/timeline_post", data={
            "email": "john@example.com", 
            "content": "Hello world, I'm John!"
        })
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html

        # POST request with empty content
        response = self.client.post("/api/timeline_post", data={
            "name": "John Doe", 
            "email": "john@example.com", 
            "content": ""
        })
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        # POST request with malformed email
        response = self.client.post("/api/timeline_post", data={
            "name": "John Doe", 
            "email": "not-an-email", 
            "content": "Hello world, I'm John!"
        })
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html