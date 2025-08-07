#!/usr/bin/env python
"""
Test Production Environment

This script tests the application in production mode by setting the RAILWAY_ENVIRONMENT variable.
"""

import os
import subprocess
import sys
import time

def test_production_mode():
    """Test the application in production mode"""
    print("\n🔍 Testing application in production mode\n")
    
    # Set the RAILWAY_ENVIRONMENT variable
    os.environ["RAILWAY_ENVIRONMENT"] = "production"
    
    # Verify the environment variable is set
    print(f"✅ RAILWAY_ENVIRONMENT set to: {os.environ.get('RAILWAY_ENVIRONMENT')}")
    
    # Test importing the main module
    try:
        import main
        print("✅ Successfully imported main module")
    except Exception as e:
        print(f"❌ Error importing main module: {e}")
        return False
    
    # Test the nova_speak function in production mode
    try:
        main.nova_speak("Testing production mode")
        print("✅ nova_speak function works in production mode")
    except Exception as e:
        print(f"❌ Error in nova_speak function: {e}")
        return False
    
    # Test the nova_listen function in production mode
    try:
        result = main.nova_listen()
        print(f"✅ nova_listen function works in production mode, returned: {result}")
    except Exception as e:
        print(f"❌ Error in nova_listen function: {e}")
        return False
    
    print("\n✅ All production mode tests passed!")
    print("The application should work correctly on Railway.")
    
    # Reset the environment variable
    del os.environ["RAILWAY_ENVIRONMENT"]
    
    return True

if __name__ == "__main__":
    test_production_mode()