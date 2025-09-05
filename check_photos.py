#!/usr/bin/env python
from albumy import create_app, db
from albumy.models import Photo

app = create_app()

with app.app_context():
    photos = Photo.query.limit(5).all()
    print(f"Total photos in database: {Photo.query.count()}")
    print("\nFirst 5 photos:")
    for photo in photos:
        print(f"  Photo {photo.id}:")
        print(f"    filename: {photo.filename}")
        print(f"    alt_text: {photo.alt_text}")
        print(f"    detected_objects: {photo.detected_objects}")
        print(f"    description: {photo.description}")
        print()