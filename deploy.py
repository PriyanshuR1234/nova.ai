#!/usr/bin/env python
"""
Deployment helper script for Nova AI

This script helps prepare the project for deployment to Railway.
It checks for required files and dependencies.
"""

import os
import sys
import subprocess

def check_file_exists(filename):
    """Check if a file exists in the current directory"""
    if os.path.isfile(filename):
        print(f"✅ {filename} exists")
        return True
    else:
        print(f"❌ {filename} does not exist")
        return False

def check_required_files():
    """Check if all required files for deployment exist"""
    required_files = ['requirements.txt', 'runtime.txt', 'Procfile', 'app.py']
    all_exist = True
    
    for file in required_files:
        if not check_file_exists(file):
            all_exist = False
    
    return all_exist

def check_templates_folder():
    """Check if templates folder exists and contains index.html"""
    if os.path.isdir('templates'):
        print("✅ templates folder exists")
        if os.path.isfile(os.path.join('templates', 'index.html')):
            print("✅ templates/index.html exists")
            return True
        else:
            print("❌ templates/index.html does not exist")
            return False
    else:
        print("❌ templates folder does not exist")
        return False

def check_git_initialized():
    """Check if git is initialized"""
    if os.path.isdir('.git'):
        print("✅ Git repository is initialized")
        return True
    else:
        print("❌ Git repository is not initialized")
        return False

def initialize_git():
    """Initialize git repository"""
    try:
        subprocess.run(['git', 'init'], check=True)
        print("✅ Git repository initialized")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to initialize git repository")
        return False
    except FileNotFoundError:
        print("❌ Git is not installed or not in PATH")
        return False

def main():
    """Main function"""
    print("\n🚀 Nova AI Deployment Helper\n")
    
    # Check required files
    print("\n📋 Checking required files...")
    files_ok = check_required_files()
    
    # Check templates folder
    print("\n📁 Checking templates folder...")
    templates_ok = check_templates_folder()
    
    # Check git
    print("\n🔄 Checking git...")
    git_ok = check_git_initialized()
    
    if not git_ok:
        print("\nWould you like to initialize git? (y/n)")
        choice = input().lower()
        if choice == 'y':
            git_ok = initialize_git()
    
    # Summary
    print("\n📊 Deployment Readiness Summary:")
    print(f"Required files: {'✅' if files_ok else '❌'}")
    print(f"Templates folder: {'✅' if templates_ok else '❌'}")
    print(f"Git initialized: {'✅' if git_ok else '❌'}")
    
    if files_ok and templates_ok and git_ok:
        print("\n✅ Your project is ready for deployment to Railway!")
        print("\nNext steps:")
        print("1. Push your code to GitHub")
        print("2. Create a Railway account at https://railway.app/")
        print("3. Create a new project in Railway and connect it to your GitHub repository")
        print("4. Railway will automatically detect and deploy your app")
    else:
        print("\n❌ Your project is not ready for deployment yet. Please fix the issues above.")

if __name__ == "__main__":
    main()