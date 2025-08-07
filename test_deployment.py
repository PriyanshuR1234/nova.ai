#!/usr/bin/env python
"""
Deployment Readiness Test

This script tests if the application is ready for deployment to Render.com
by checking for common issues and verifying dependencies.
"""

import os
import sys
import importlib
import platform
import subprocess
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_python_version():
    """Check if Python version is compatible with Render deployment"""
    recommended_version = (3, 9, 18)  # Recommended for Render deployment
    current_version = sys.version_info
    
    logger.info(f"Python version: {platform.python_version()}")
    
    if current_version.major == recommended_version[0] and current_version.minor == recommended_version[1]:
        logger.info("✅ Python version is ideal for Render deployment")
        return True
    else:
        logger.warning(f"⚠️ Python version {current_version.major}.{current_version.minor} is not ideal for Render deployment")
        logger.warning(f"   Recommended version: {recommended_version[0]}.{recommended_version[1]}.{recommended_version[2]}")
        return False

def check_dependencies():
    """Check if all required dependencies are installed and compatible"""
    required_packages = {
        'flask': '2.0.1',
        'werkzeug': '2.0.3',
        'gunicorn': '20.1.0',
        'gtts': '2.2.4',
        'SpeechRecognition': '3.8.1',
        'undetected-chromedriver': '3.5.5',
        'selenium': '4.10.0',
    }
    
    logger.info("Checking dependencies...")
    all_dependencies_ok = True
    
    try:
        import pkg_resources
        
        for package, recommended_version in required_packages.items():
            try:
                installed_version = pkg_resources.get_distribution(package).version
                if installed_version == recommended_version:
                    logger.info(f"✅ {package}=={installed_version} (recommended)")
                else:
                    logger.warning(f"⚠️ {package}=={installed_version} (recommended: {recommended_version})")
                    all_dependencies_ok = False
            except pkg_resources.DistributionNotFound:
                logger.error(f"❌ {package} not installed")
                all_dependencies_ok = False
        
        # Special check for werkzeug.urls.url_quote
        try:
            from werkzeug.urls import url_quote
            logger.info("✅ werkzeug.urls.url_quote is available")
        except ImportError as e:
            logger.error(f"❌ werkzeug.urls.url_quote is not available: {e}")
            logger.error("   This will cause deployment errors on Render")
            all_dependencies_ok = False
    
    except ImportError:
        logger.error("❌ pkg_resources not available, cannot check package versions")
        all_dependencies_ok = False
    
    return all_dependencies_ok

def check_required_files():
    """Check if all required files for deployment are present"""
    required_files = [
        'requirements.txt',
        'runtime.txt',
        'Procfile',
        'render.yaml',
        'startup.sh',
        'app.py',
        'templates/index.html',
    ]
    
    logger.info("Checking required files...")
    all_files_present = True
    
    for file_path in required_files:
        if os.path.exists(file_path):
            logger.info(f"✅ {file_path} exists")
        else:
            logger.error(f"❌ {file_path} not found")
            all_files_present = False
    
    return all_files_present

def check_runtime_txt():
    """Check if runtime.txt contains the correct Python version"""
    try:
        with open('runtime.txt', 'r') as f:
            content = f.read().strip()
        
        expected_content = 'python-3.9.18'
        if content == expected_content:
            logger.info(f"✅ runtime.txt contains correct Python version: {content}")
            return True
        else:
            logger.warning(f"⚠️ runtime.txt contains {content}, expected {expected_content}")
            return False
    except FileNotFoundError:
        logger.error("❌ runtime.txt not found")
        return False

def check_render_yaml():
    """Check if render.yaml is configured correctly"""
    try:
        with open('render.yaml', 'r') as f:
            content = f.read()
        
        # Check for key configurations
        checks = [
            ('startCommand: bash startup.sh', 'startup.sh script'),
            ('RENDER', 'RENDER environment variable'),
            ('PYTHON_VERSION', 'PYTHON_VERSION environment variable'),
        ]
        
        all_checks_passed = True
        for check_string, description in checks:
            if check_string in content:
                logger.info(f"✅ render.yaml includes {description}")
            else:
                logger.warning(f"⚠️ render.yaml missing {description}")
                all_checks_passed = False
        
        return all_checks_passed
    except FileNotFoundError:
        logger.error("❌ render.yaml not found")
        return False

def main():
    """Run all deployment readiness tests"""
    logger.info("===== Testing Deployment Readiness for Render.com =====")
    
    # Run all checks
    python_ok = check_python_version()
    dependencies_ok = check_dependencies()
    files_ok = check_required_files()
    runtime_ok = check_runtime_txt()
    render_yaml_ok = check_render_yaml()
    
    # Summary
    logger.info("\n===== Deployment Readiness Summary =====")
    logger.info(f"Python version: {'✅' if python_ok else '⚠️'}")
    logger.info(f"Dependencies: {'✅' if dependencies_ok else '❌'}")
    logger.info(f"Required files: {'✅' if files_ok else '❌'}")
    logger.info(f"runtime.txt: {'✅' if runtime_ok else '❌'}")
    logger.info(f"render.yaml: {'✅' if render_yaml_ok else '❌'}")
    
    # Overall readiness
    deployment_ready = dependencies_ok and files_ok and runtime_ok and render_yaml_ok
    
    if deployment_ready:
        logger.info("\n✅ Your application is READY for deployment to Render.com!")
        return True
    else:
        logger.warning("\n⚠️ Your application is NOT READY for deployment to Render.com")
        logger.warning("   Please fix the issues above before deploying")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)