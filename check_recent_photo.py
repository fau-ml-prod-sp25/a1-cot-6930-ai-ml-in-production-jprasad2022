#!/usr/bin/env python
from albumy import create_app, db
from albumy.models import Photo
import os

app = create_app()

with app.app_context():
    # Get the most recent photo
    latest_photo = Photo.query.order_by(Photo.id.desc()).first()
    
    if latest_photo:
        print(f"Latest Photo ID: {latest_photo.id}")
        print(f"Author: {latest_photo.author.username}")
        print(f"Filename: {latest_photo.filename}")
        print(f"Filename_s: {latest_photo.filename_s}")
        print(f"Filename_m: {latest_photo.filename_m}")
        print(f"Alt text: {latest_photo.alt_text}")
        print(f"Detected objects: {latest_photo.detected_objects}")
        print(f"Timestamp: {latest_photo.timestamp}")
        
        # Check if files exist
        upload_path = app.config['ALBUMY_UPLOAD_PATH']
        print(f"\nFile check:")
        print(f"Original exists: {os.path.exists(os.path.join(upload_path, latest_photo.filename))}")
        print(f"Small exists: {os.path.exists(os.path.join(upload_path, latest_photo.filename_s))}")
        print(f"Medium exists: {os.path.exists(os.path.join(upload_path, latest_photo.filename_m))}")
    else:
        print("No photos found in database")