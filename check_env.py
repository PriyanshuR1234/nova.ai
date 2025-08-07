#!/usr/bin/env python
"""
Check environment variables

This script checks if the environment variables are set correctly.
"""

import os

def check_environment():
    """Check if environment variables are set correctly"""
    print("\n🔍 Checking environment variables\n")
    
    # Check if RAILWAY_ENVIRONMENT is set
    railway_env = os.environ.get('RAILWAY_ENVIRONMENT')
    if railway_env:
        print(f"✅ RAILWAY_ENVIRONMENT is set to: {railway_env}")
    else:
        print("❌ RAILWAY_ENVIRONMENT is not set")
        print("   For local development, this is fine.")
        print("   For Railway deployment, set RAILWAY_ENVIRONMENT=production")
    
    # Check other environment variables
    print("\nOther environment variables that might be useful:")
    port = os.environ.get('PORT')
    if port:
        print(f"✅ PORT is set to: {port}")
    else:
        print("ℹ️ PORT is not set (will default to 5000)")
    
    # Print Python version
    import sys
    print(f"\nPython version: {sys.version}")
    
    return True

if __name__ == "__main__":
    check_environment()