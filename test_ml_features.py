#!/usr/bin/env python3
"""
Test script to verify ML features are working correctly
"""
import os
from albumy.ml_services import ml_service

def test_ml_service():
    """Test ML service functions"""
    print("Testing ML Service...")
    
    # Check if credentials exist
    if not os.path.exists('google-credentials.json'):
        print("❌ Google credentials file not found!")
        return False
    print("✅ Google credentials file found")
    
    # Test with a sample image
    test_images = [
        'uploads/1.jpg',
        'uploads/2.jpg',
        'uploads/3.jpg'
    ]
    
    # Find a test image
    test_image = None
    for img in test_images:
        if os.path.exists(img):
            test_image = img
            break
    
    if not test_image:
        print("⚠️  No test images found in uploads folder")
        print("   Upload some images through the web interface first")
        return False
    
    print(f"\nTesting with image: {test_image}")
    
    # Test alt text generation
    print("\n1. Testing Alt Text Generation:")
    alt_text = ml_service.generate_alt_text(test_image)
    print(f"   Generated alt text: '{alt_text}'")
    
    # Test object detection
    print("\n2. Testing Object Detection:")
    objects = ml_service.detect_objects(test_image)
    print(f"   Detected objects: {objects}")
    
    if alt_text == "Image" and len(objects) == 0:
        print("\n⚠️  ML features might not be working properly.")
        print("   Check your Google Cloud Vision API credentials.")
        return False
    
    print("\n✅ ML features are working correctly!")
    return True

if __name__ == "__main__":
    test_ml_service()