#!/usr/bin/env python
"""
Deployment Environment Checker

This script performs checks specific to the deployment environment (Render.com)
and verifies that all necessary components are available.
"""

import os
import sys
import platform
import logging
import importlib.util

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_render_environment():
    """Check if running on Render.com and verify environment"""
    logger.info("\n===== Checking Render.com deployment environment =====")
    
    # Check if RENDER environment variable is set
    render_env = os.environ.get('RENDER')
    if render_env:
        logger.info(f"✅ RENDER environment variable is set to: {render_env}")
        logger.info("   Running on Render.com platform")
    else:
        logger.info("ℹ️ RENDER environment variable is not set")
        logger.info("   Not running on Render.com platform")
        return True  # Not on Render, so no specific checks needed
    
    # Check Python version
    python_version = platform.python_version()
    logger.info(f"Python version: {python_version}")
    
    # Check for critical imports
    critical_packages = [
        'flask', 'werkzeug', 'gunicorn', 'gtts', 'speech_recognition',
        'selenium', 'undetected_chromedriver'
    ]
    
    logger.info("\nChecking critical package imports:")
    all_imports_successful = True
    
    for package in critical_packages:
        try:
            # Try to import the package
            spec = importlib.util.find_spec(package)
            if spec is None:
                logger.error(f"❌ {package} - Not found")
                all_imports_successful = False
            else:
                # For werkzeug, check specific modules
                if package == 'werkzeug':
                    try:
                        # This is the specific import that fails in the error log
                        from werkzeug.urls import url_quote
                        logger.info(f"✅ {package} - Successfully imported (including url_quote)")
                    except ImportError as e:
                        logger.error(f"❌ {package} - Found but url_quote import failed: {e}")
                        all_imports_successful = False
                else:
                    logger.info(f"✅ {package} - Successfully found")
        except Exception as e:
            logger.error(f"❌ {package} - Error during import check: {e}")
            all_imports_successful = False
    
    # Check for Chrome/Chromium availability (needed for selenium/undetected_chromedriver)
    logger.info("\nChecking for Chrome/Chromium availability:")
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        logger.info("Attempting to create Chrome WebDriver instance...")
        # Just check if we can create a driver, don't actually use it
        try:
            driver = webdriver.Chrome(options=options)
            driver.quit()
            logger.info("✅ Chrome WebDriver successfully initialized")
        except Exception as e:
            logger.warning(f"⚠️ Chrome WebDriver initialization failed: {e}")
            logger.warning("   This may be expected in headless environments")
    except Exception as e:
        logger.error(f"❌ Error checking Chrome availability: {e}")
    
    logger.info("\n===== Deployment environment check complete =====")
    return all_imports_successful

if __name__ == "__main__":
    check_render_environment()