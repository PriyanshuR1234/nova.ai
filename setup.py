#!/usr/bin/env python
"""
Setup script for Nova AI

This script helps set up the project locally by installing dependencies
and checking for common issues.
"""

import os
import sys
import subprocess
import platform

def check_python_version():
    """Check if Python version is compatible"""
    required_version = (3, 10)
    current_version = sys.version_info
    
    if current_version < required_version:
        print(f"❌ Python {required_version[0]}.{required_version[1]} or higher is required")
        print(f"   Current version: {current_version[0]}.{current_version[1]}")
        return False
    else:
        print(f"✅ Python version {current_version[0]}.{current_version[1]} is compatible")
        return True

def install_dependencies():
    """Install dependencies from requirements.txt"""
    try:
        print("\n📦 Installing dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def install_undetected_chromedriver_manually():
    """Install undetected-chromedriver manually"""
    try:
        print("\n🔄 Installing undetected-chromedriver manually...")
        subprocess.run([sys.executable, "-m", "pip", "install", "undetected-chromedriver==3.5.0", "--force-reinstall"], check=True)
        print("✅ undetected-chromedriver installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install undetected-chromedriver: {e}")
        return False

def check_chrome_installed():
    """Check if Chrome is installed"""
    system = platform.system()
    
    if system == "Windows":
        chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        chrome_path_x86 = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
        if os.path.exists(chrome_path) or os.path.exists(chrome_path_x86):
            print("✅ Google Chrome is installed")
            return True
    elif system == "Darwin":  # macOS
        chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        if os.path.exists(chrome_path):
            print("✅ Google Chrome is installed")
            return True
    elif system == "Linux":
        try:
            subprocess.run(["which", "google-chrome"], check=True, stdout=subprocess.PIPE)
            print("✅ Google Chrome is installed")
            return True
        except subprocess.CalledProcessError:
            pass
    
    print("❌ Google Chrome is not installed or not found in the default location")
    print("   Please install Chrome from https://www.google.com/chrome/")
    return False

def create_virtual_env():
    """Create a virtual environment if it doesn't exist"""
    if os.path.exists("venv"):
        print("✅ Virtual environment already exists")
        return True
    
    try:
        print("\n🔄 Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✅ Virtual environment created successfully")
        
        # Suggest activation command
        system = platform.system()
        if system == "Windows":
            print("\nTo activate the virtual environment, run:")
            print("   venv\\Scripts\\activate")
        else:
            print("\nTo activate the virtual environment, run:")
            print("   source venv/bin/activate")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create virtual environment: {e}")
        return False

def main():
    """Main function"""
    print("\n🚀 Nova AI Setup Helper\n")
    
    # Check Python version
    python_ok = check_python_version()
    if not python_ok:
        print("\n❌ Setup failed due to incompatible Python version")
        return
    
    # Create virtual environment
    venv_ok = create_virtual_env()
    
    # Check Chrome installation
    chrome_ok = check_chrome_installed()
    
    # Install dependencies
    deps_ok = install_dependencies()
    
    # If undetected-chromedriver installation failed, try manual installation
    if deps_ok:
        try:
            import undetected_chromedriver
            print("✅ undetected-chromedriver is installed correctly")
        except ImportError:
            print("❌ undetected-chromedriver not found, trying manual installation")
            undetected_ok = install_undetected_chromedriver_manually()
    
    # Summary
    print("\n📊 Setup Summary:")
    print(f"Python version: {'✅' if python_ok else '❌'}")
    print(f"Virtual environment: {'✅' if venv_ok else '❌'}")
    print(f"Chrome installation: {'✅' if chrome_ok else '❌'}")
    print(f"Dependencies: {'✅' if deps_ok else '❌'}")
    
    if python_ok and chrome_ok and deps_ok:
        print("\n✅ Setup completed successfully!")
        print("\nTo run the application:")
        print("1. Activate the virtual environment")
        print("2. Run 'python app.py'")
    else:
        print("\n❌ Setup completed with issues. Please fix the problems above.")

if __name__ == "__main__":
    main()