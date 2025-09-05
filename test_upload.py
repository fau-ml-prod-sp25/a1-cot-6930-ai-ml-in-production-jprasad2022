#!/usr/bin/env python
from albumy import create_app, db
from albumy.models import Photo, User

app = create_app()

with app.app_context():
    # Count photos before and show the latest ones
    total_photos = Photo.query.count()
    print(f"Total photos in database: {total_photos}")
    
    # Get photos uploaded by admin (you)
    admin = User.query.filter_by(username='admin').first()
    if admin:
        admin_photos = Photo.query.filter_by(author=admin).order_by(Photo.id.desc()).limit(5).all()
        print(f"\nPhotos by admin user:")
        for photo in admin_photos:
            print(f"  ID: {photo.id}, Filename: {photo.filename}, Alt text: {photo.alt_text}")
    
    # Get the 5 most recent photos
    recent_photos = Photo.query.order_by(Photo.id.desc()).limit(5).all()
    print(f"\n5 Most recent photos:")
    for photo in recent_photos:
        print(f"  ID: {photo.id}, Author: {photo.author.username}, Filename: {photo.filename}")