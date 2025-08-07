#!/usr/bin/env python
"""
Test script for Flask app

This script tests if the Flask app is working correctly.
"""

import os
import requests

def test_flask_app():
    """Test if the Flask app is working"""
    try:
        print("Testing Flask app...")
        # Try to connect to the local Flask app
        response = requests.get("http://localhost:5000")
        
        # Check if the response is successful
        if response.status_code == 200:
            print(f"✅ Flask app is running. Status code: {response.status_code}")
            return True
        else:
            print(f"❌ Flask app returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to Flask app. Make sure it's running on http://localhost:5000")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("\n🔍 Testing Flask app\n")
    test_flask_app()