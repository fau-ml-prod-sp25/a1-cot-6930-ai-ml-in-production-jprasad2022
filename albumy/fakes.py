# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li <withlihui@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
import os
import random

from PIL import Image
from faker import Faker
from flask import current_app
from sqlalchemy.exc import IntegrityError

from albumy.extensions import db
from albumy.models import User, Photo, Tag, Comment, Notification

fake = Faker()


def fake_admin():
    admin = User(name='Admin User',
                 username='admin',
                 email='admin@helloflask.com',
                 bio=fake.sentence(),
                 website='http://example.com',
                 confirmed=True)
    admin.set_password('helloflask')
    notification = Notification(message='Hello, welcome to Albumy.', receiver=admin)
    db.session.add(notification)
    db.session.add(admin)
    db.session.commit()


def fake_user(count=10):
    for i in range(count):
        user = User(name=fake.name(),
                    confirmed=True,
                    username=fake.user_name(),
                    bio=fake.sentence(),
                    location=fake.city(),
                    website=fake.url(),
                    member_since=fake.date_this_decade(),
                    email=fake.email())
        user.set_password('123456')
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_follow(count=30):
    for i in range(count):
        user = User.query.get(random.randint(1, User.query.count()))
        user.follow(User.query.get(random.randint(1, User.query.count())))
    db.session.commit()


def fake_tag(count=20):
    for i in range(count):
        tag = Tag(name=fake.word())
        db.session.add(tag)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_photo(count=30):
    # photos
    upload_path = current_app.config['ALBUMY_UPLOAD_PATH']
    for i in range(count):
        print(f"Generating photo {i + 1}/{count}")

        filename = 'random_%d.jpg' % i
        
        try:
            # Download a random photo from Lorem Picsum
            import requests
            response = requests.get(f'https://picsum.photos/800/800?random={i}', timeout=10)
            if response.status_code == 200:
                # Save the downloaded image
                with open(os.path.join(upload_path, filename), 'wb') as f:
                    f.write(response.content)
            else:
                # Fallback to colored square if download fails
                r = lambda: random.randint(128, 255)
                img = Image.new(mode='RGB', size=(800, 800), color=(r(), r(), r()))
                img.save(os.path.join(upload_path, filename))
        except Exception as e:
            print(f"Failed to download image {i}: {e}")
            # Fallback to colored square
            r = lambda: random.randint(128, 255)
            img = Image.new(mode='RGB', size=(800, 800), color=(r(), r(), r()))
            img.save(os.path.join(upload_path, filename))

        photo = Photo(
            description=fake.text(),
            filename=filename,
            filename_m=filename,
            filename_s=filename,
            author=User.query.get(random.randint(1, User.query.count())),
            timestamp=fake.date_time_this_year()
        )

        # tags
        for j in range(random.randint(1, 5)):
            tag = Tag.query.get(random.randint(1, Tag.query.count()))
            if tag not in photo.tags:
                photo.tags.append(tag)

        db.session.add(photo)
    db.session.commit()


def fake_collect(count=50):
    for i in range(count):
        user = User.query.get(random.randint(1, User.query.count()))
        user.collect(Photo.query.get(random.randint(1, Photo.query.count())))
    db.session.commit()


def fake_comment(count=100):
    # Realistic photo comments
    photo_comments = [
        "Amazing shot! Love the composition.",
        "Beautiful capture! The lighting is perfect.",
        "Wow, this is stunning! Great work.",
        "Love the colors in this photo!",
        "This is incredible! Where was this taken?",
        "Such a beautiful moment captured!",
        "The details in this photo are amazing.",
        "Great perspective! Really unique angle.",
        "This made my day! Thanks for sharing.",
        "Absolutely gorgeous! Well done.",
        "I love everything about this photo!",
        "The mood in this shot is perfect.",
        "Breathtaking view! Thanks for sharing this.",
        "This is art! Beautiful work.",
        "Love the way you captured the light here.",
        "So peaceful and serene. Beautiful shot!",
        "This photo tells such a great story.",
        "The composition is spot on! Great eye.",
        "What camera did you use for this? It's amazing!",
        "This deserves to be framed! Excellent work.",
        "I can feel the atmosphere through this photo.",
        "Perfect timing on this shot!",
        "The contrast is beautiful. Well edited!",
        "This is why I love photography. Stunning!",
        "You have such a great eye for detail.",
        "This photo speaks volumes. Love it!",
        "The depth of field is perfect here.",
        "Such a creative shot! Keep it up!",
        "This brings back memories. Beautiful capture.",
        "The symmetry in this photo is satisfying!",
        "Nature at its finest! Great shot.",
        "I could stare at this all day. Mesmerizing!",
        "This is desktop wallpaper material!",
        "The golden hour lighting is magical here.",
        "You've really captured the essence of the moment.",
        "This photo has such a calming effect.",
        "Masterfully done! The framing is perfect.",
        "I love the minimalist approach here.",
        "The textures in this photo are incredible.",
        "This evokes so much emotion. Beautiful work!"
    ]
    
    for i in range(count):
        comment = Comment(
            author=User.query.get(random.randint(1, User.query.count())),
            body=random.choice(photo_comments),
            timestamp=fake.date_time_this_year(),
            photo=Photo.query.get(random.randint(1, Photo.query.count()))
        )
        db.session.add(comment)
    db.session.commit()
