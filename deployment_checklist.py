#!/usr/bin/env python
"""
Deployment Checklist

This script checks if all the necessary files and configurations are in place for deployment.
"""

import os
import sys
import subprocess

def check_file_exists(file_path, required=True):
    """Check if a file exists"""
    exists = os.path.isfile(file_path)
    if exists:
        print(f"✅ {file_path} exists")
    else:
        if required:
            print(f"❌ {file_path} does not exist (required)")
        else:
            print(f"⚠️ {file_path} does not exist (optional)")
    return exists

def check_directory_exists(dir_path, required=True):
    """Check if a directory exists"""
    exists = os.path.isdir(dir_path)
    if exists:
        print(f"✅ {dir_path} exists")
    else:
        if required:
            print(f"❌ {dir_path} does not exist (required)")
        else:
            print(f"⚠️ {dir_path} does not exist (optional)")
    return exists

def check_dependencies():
    """Check if all dependencies are installed"""
    try:
        # Try importing key dependencies
        import flask
        import undetected_chromedriver
        import selenium
        import gtts
        import playsound
        import speech_recognition
        print("✅ All key dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False

def check_deployment_readiness():
    """Check if the project is ready for deployment"""
    print("\n🔍 Checking deployment readiness\n")
    
    # Check required files
    required_files = [
        "requirements.txt",
        "Procfile",
        "app.py",
        "main.py",
        "railway.toml"
    ]
    
    optional_files = [
        "runtime.txt",
        ".gitignore",
        "README.md"
    ]
    
    all_required_files_exist = True
    for file in required_files:
        if not check_file_exists(file):
            all_required_files_exist = False
    
    for file in optional_files:
        check_file_exists(file, required=False)
    
    # Check directories
    required_dirs = [
        "templates"
    ]
    
    all_required_dirs_exist = True
    for dir_path in required_dirs:
        if not check_directory_exists(dir_path):
            all_required_dirs_exist = False
    
    # Check if templates/index.html exists
    if os.path.isdir("templates"):
        check_file_exists(os.path.join("templates", "index.html"))
    
    # Check dependencies
    dependencies_ok = check_dependencies()
    
    # Check if git is initialized
    git_initialized = os.path.isdir(".git")
    if git_initialized:
        print("✅ Git repository is initialized")
    else:
        print("⚠️ Git repository is not initialized (required for Railway deployment)")
        init_git = input("Do you want to initialize Git? (y/n): ")
        if init_git.lower() == 'y':
            try:
                subprocess.run(["git", "init"], check=True)
                print("✅ Git repository initialized")
                git_initialized = True
            except Exception as e:
                print(f"❌ Failed to initialize Git: {e}")
    
    # Summary
    print("\n📋 Deployment Readiness Summary")
    if all_required_files_exist and all_required_dirs_exist and dependencies_ok and git_initialized:
        print("✅ Your project is ready for deployment!")
    else:
        print("❌ Your project is not ready for deployment. Please fix the issues above.")
    
    # Next steps
    print("\n📝 Next Steps for Railway Deployment:")
    print("1. Push your code to GitHub")
    print("2. Log in to Railway and create a new project from your GitHub repository")
    print("3. Set the RAILWAY_ENVIRONMENT=production environment variable")
    print("4. Monitor the deployment in the Railway dashboard")
    
    return all_required_files_exist and all_required_dirs_exist and dependencies_ok and git_initialized

if __name__ == "__main__":
    check_deployment_readiness()