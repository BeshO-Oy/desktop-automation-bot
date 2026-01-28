"""API client for fetching blog posts from JSONPlaceholder."""
import requests
from typing import List, Dict, Optional
import time

class APIClient:
    """Client for interacting with JSONPlaceholder API."""
    
    def __init__(self, base_url: str = "https://jsonplaceholder.typicode.com"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def fetch_posts(self, limit: int = 10) -> List[Dict]:
        """
        Fetch blog posts from the API.
        
        Args:
            limit: Maximum number of posts to fetch
            
        Returns:
            List of post dictionaries
        """
        try:
            response = self.session.get(f"{self.base_url}/posts", timeout=10)
            response.raise_for_status()
            posts = response.json()
            
            # Return only the first 'limit' posts
            return posts[:limit]
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching posts: {e}")
            # Return empty list on error (graceful degradation)
            return []
    
    def get_post(self, post_id: int) -> Optional[Dict]:
        """Fetch a single post by ID."""
        try:
            response = self.session.get(f"{self.base_url}/posts/{post_id}", timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching post {post_id}: {e}")
            return None
