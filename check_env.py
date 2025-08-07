#!/usr/bin/env python
"""
Check environment variables

This script checks if the environment variables are set correctly for both
local development and cloud deployment (Render and Railway).
"""

import os
import sys

def check_environment():
    """Check if environment variables are set correctly"""
    print("\n🔍 Checking environment variables\n")
    
    # Check deployment platform
    print("Deployment Platform Detection:")
    
    # Check if RENDER is set (for Render.com)
    render_env = os.environ.get('RENDER')
    if render_env:
        print(f"✅ RENDER is set to: {render_env}")
        print("   Running on Render.com platform")
    else:
        print("ℹ️ RENDER is not set")
    
    # Check if RAILWAY_ENVIRONMENT is set (for Railway.app)
    railway_env = os.environ.get('RAILWAY_ENVIRONMENT')
    if railway_env:
        print(f"✅ RAILWAY_ENVIRONMENT is set to: {railway_env}")
        print("   Running on Railway.app platform")
    else:
        print("ℹ️ RAILWAY_ENVIRONMENT is not set")
    
    # If neither is set, likely running locally
    if not render_env and not railway_env:
        print("ℹ️ Running in local development environment")
    
    # Check Python version
    import sys
    print(f"\nPython version: {sys.version}")
    
    # Check other environment variables
    print("\nOther environment variables:")
    port = os.environ.get('PORT')
    if port:
        print(f"✅ PORT is set to: {port}")
    else:
        print("ℹ️ PORT is not set (will default to 5000)")
        
    # Check for Flask environment variables
    flask_env = os.environ.get('FLASK_ENV')
    if flask_env:
        print(f"✅ FLASK_ENV is set to: {flask_env}")
    else:
        print("ℹ️ FLASK_ENV is not set (will default to production)")
        
    # Check for debug mode
    flask_debug = os.environ.get('FLASK_DEBUG')
    if flask_debug:
        print(f"✅ FLASK_DEBUG is set to: {flask_debug}")
    else:
        print("ℹ️ FLASK_DEBUG is not set (will default to 0)")
        
    print("\nEnvironment check complete.\n")
    return True

if __name__ == "__main__":
    check_environment()