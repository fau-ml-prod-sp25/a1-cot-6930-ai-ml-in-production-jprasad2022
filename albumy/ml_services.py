import os
import json
from dotenv import load_dotenv
from google.cloud import vision
from google.oauth2 import service_account

# Load environment variables
load_dotenv()

class MLService:
    def __init__(self):
        # Get the project root directory
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        creds_path = os.path.join(base_dir, 'google-credentials.json')
        
        if not os.path.exists(creds_path):
            print(f"Warning: Google credentials not found at {creds_path}. ML features disabled.")
            self.client = None
        else:
            try:
                credentials = service_account.Credentials.from_service_account_file(creds_path)
                self.client = vision.ImageAnnotatorClient(credentials=credentials)
                print("ML Service initialized successfully!")
            except Exception as e:
                print(f"Error initializing ML service: {e}")
                self.client = None
    
    def generate_alt_text(self, image_path):
        """Generate alt text for an image using Google Vision"""
        if not self.client:
            return "Image"
        
        try:
            with open(image_path, "rb") as image_file:
                content = image_file.read()
            
            image = vision.Image(content=content)
            
            # Get image labels for description
            response = self.client.label_detection(image=image, max_results=5)
            labels = response.label_annotations
            
            if labels:
                # Create a simple description from top labels
                top_labels = [label.description.lower() for label in labels[:3]]
                alt_text = "Image containing " + ", ".join(top_labels)
                return alt_text
            
            return "Image"
        except Exception as e:
            print(f"Error generating alt text: {e}")
            return "Image"
    
    def detect_objects(self, image_path):
        """Detect objects and labels for search functionality"""
        if not self.client:
            return []
        
        try:
            with open(image_path, "rb") as image_file:
                content = image_file.read()
            
            image = vision.Image(content=content)
            
            # Get labels
            response = self.client.label_detection(image=image, max_results=10)
            labels = response.label_annotations
            
            # Extract labels with good confidence
            tags = [label.description.lower() for label in labels if label.score > 0.7]
            
            return tags
            
        except Exception as e:
            print(f"Error detecting objects: {e}")
            return []

# Create a global instance
ml_service = MLService()