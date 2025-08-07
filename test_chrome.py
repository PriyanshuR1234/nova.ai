#!/usr/bin/env python
"""
Test script for undetected-chromedriver

This script tests if undetected-chromedriver is working correctly.
"""

import os
import time

def test_undetected_chromedriver():
    """Test if undetected-chromedriver is working"""
    try:
        import undetected_chromedriver as uc
        print("✅ undetected-chromedriver module imported successfully")
        
        # Configure Chrome options
        options = uc.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        # Initialize Chrome driver with version matching
        print("Initializing Chrome driver...")
        driver = uc.Chrome(options=options, version_main=138)  # Set to match your Chrome version
        
        # Open a website
        print("Opening website...")
        driver.get("https://www.google.com")
        
        # Get the title
        title = driver.title
        print(f"Website title: {title}")
        
        # Close the driver
        driver.quit()
        
        print("✅ undetected-chromedriver is working correctly")
        return True
    except ImportError:
        print("❌ Failed to import undetected-chromedriver")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("\n🔍 Testing undetected-chromedriver\n")
    test_undetected_chromedriver()