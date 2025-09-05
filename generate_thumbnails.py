#!/usr/bin/env python
import os
import json
from albumy import create_app, db
from albumy.models import Photo
from albumy.utils import resize_image
from albumy.ml_services import ml_service
from PIL import Image

app = create_app()

with app.app_context():
    photos = Photo.query.all()
    ml_updated = 0
    
    for photo in photos:
        print(f"Processing photo {photo.id}: {photo.filename}")
        
        # Generate thumbnails
        upload_path = app.config['ALBUMY_UPLOAD_PATH']
        image_path = os.path.join(upload_path, photo.filename)
        
        if os.path.exists(image_path):
            # Generate thumbnails if missing
            if not photo.filename_s or not photo.filename_m:
                # Open the original image
                with Image.open(image_path) as img:
                    # Save a copy for processing
                    img.save(image_path)
                
                # Generate small thumbnail (400px)
                with open(image_path, 'rb') as f:
                    filename_s = resize_image(f, photo.filename, app.config['ALBUMY_PHOTO_SIZE']['small'])
                    photo.filename_s = filename_s
                
                # Generate medium size (800px)
                with open(image_path, 'rb') as f:
                    filename_m = resize_image(f, photo.filename, app.config['ALBUMY_PHOTO_SIZE']['medium'])
                    photo.filename_m = filename_m
                
                print(f"  Created thumbnails: {filename_s} and {filename_m}")
            
            # Generate ML features if missing
            if not photo.alt_text or photo.alt_text == "Image" or not photo.detected_objects:
                try:
                    # Generate alt text
                    if not photo.alt_text or photo.alt_text == "Image":
                        photo.alt_text = ml_service.generate_alt_text(image_path)
                        print(f"  Alt text: {photo.alt_text}")
                    
                    # Detect objects
                    if not photo.detected_objects:
                        objects = ml_service.detect_objects(image_path)
                        photo.detected_objects = json.dumps(objects)
                        print(f"  Detected objects: {objects}")
                    
                    ml_updated += 1
                except Exception as e:
                    print(f"  ML processing error: {e}")
        else:
            print(f"  Warning: {image_path} not found")
    
    db.session.commit()
    print(f"\nDone! Updated {ml_updated} photos with ML features.")