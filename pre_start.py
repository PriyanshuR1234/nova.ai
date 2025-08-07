#!/usr/bin/env python
"""
Pre-start Script

This script runs before the application starts to ensure all dependencies
are properly configured and the environment is ready for deployment.
"""

import os
import sys
import logging
import importlib.util

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_checks():
    """Run all pre-start checks"""
    logger.info("\n===== Running pre-start checks =====")
    
    # Check if running on Render.com
    render_env = os.environ.get('RENDER')
    if render_env:
        logger.info("Running on Render.com platform")
    else:
        logger.info("Running in local environment")
    
    # Check Python version
    logger.info(f"Python version: {sys.version}")
    
    # Check for critical modules
    critical_modules = [
        ('flask', 'Flask web framework'),
        ('werkzeug', 'WSGI utilities'),
        ('werkzeug.urls', 'URL utilities from Werkzeug'),
        ('gunicorn', 'WSGI HTTP Server'),
        ('gtts', 'Google Text-to-Speech'),
        ('speech_recognition', 'Speech recognition'),
        ('selenium', 'Browser automation'),
        ('undetected_chromedriver', 'Undetected ChromeDriver')
    ]
    
    all_modules_available = True
    logger.info("\nChecking critical modules:")
    
    for module_name, description in critical_modules:
        try:
            if '.' in module_name:
                # For submodules like werkzeug.urls
                parent_module, submodule = module_name.split('.', 1)
                parent = __import__(parent_module, fromlist=[submodule])
                getattr(parent, submodule)
                logger.info(f"✅ {module_name} - Available ({description})")
            else:
                # For top-level modules
                __import__(module_name)
                logger.info(f"✅ {module_name} - Available ({description})")
        except ImportError as e:
            logger.error(f"❌ {module_name} - Not available: {e}")
            all_modules_available = False
    
    # Special check for werkzeug.urls.url_quote
    try:
        from werkzeug.urls import url_quote
        logger.info("✅ werkzeug.urls.url_quote - Available")
    except ImportError as e:
        logger.error(f"❌ werkzeug.urls.url_quote - Not available: {e}")
        all_modules_available = False
    
    # Check environment variables
    logger.info("\nChecking environment variables:")
    env_vars = ['PORT', 'RENDER', 'FLASK_ENV', 'FLASK_DEBUG']
    for var in env_vars:
        value = os.environ.get(var)
        if value:
            logger.info(f"✅ {var}={value}")
        else:
            logger.info(f"ℹ️ {var} not set")
    
    # Check for templates directory
    templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    if os.path.isdir(templates_dir):
        logger.info(f"✅ Templates directory exists: {templates_dir}")
        # Check for index.html
        index_html = os.path.join(templates_dir, 'index.html')
        if os.path.isfile(index_html):
            logger.info(f"✅ index.html exists")
        else:
            logger.error(f"❌ index.html not found in templates directory")
            all_modules_available = False
    else:
        logger.error(f"❌ Templates directory not found: {templates_dir}")
        all_modules_available = False
    
    logger.info("\n===== Pre-start checks complete =====")
    
    if all_modules_available:
        logger.info("✅ All critical modules are available")
        return True
    else:
        logger.error("❌ Some critical modules are missing")
        return False

if __name__ == "__main__":
    success = run_checks()
    if not success:
        logger.error("Pre-start checks failed. Application may not function correctly.")
        # Don't exit with error code as this might prevent the app from starting
        # sys.exit(1)