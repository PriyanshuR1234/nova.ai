#!/usr/bin/env python
"""
Dependency Compatibility Checker

This script checks for compatibility issues between installed packages.
It's useful for diagnosing deployment problems related to package versions.
"""

import pkg_resources
import sys
import importlib
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_flask_werkzeug_compatibility():
    """Check if Flask and Werkzeug versions are compatible"""
    try:
        flask_version = pkg_resources.get_distribution("flask").version
        werkzeug_version = pkg_resources.get_distribution("werkzeug").version
        
        logger.info(f"Flask version: {flask_version}")
        logger.info(f"Werkzeug version: {werkzeug_version}")
        
        # Check for known compatibility issues
        if flask_version.startswith("2.0") and not werkzeug_version.startswith("2.0"):
            logger.warning(f"Potential compatibility issue: Flask {flask_version} works best with Werkzeug 2.0.x")
            logger.warning(f"Current Werkzeug version is {werkzeug_version}")
            return False
        
        # Test importing url_quote from werkzeug.urls
        try:
            from werkzeug.urls import url_quote
            logger.info("Successfully imported url_quote from werkzeug.urls")
            return True
        except ImportError as e:
            logger.error(f"ImportError: {e}")
            logger.error("This is likely causing the deployment error on Render")
            return False
            
    except pkg_resources.DistributionNotFound as e:
        logger.error(f"Package not found: {e}")
        return False

def check_all_dependencies():
    """Check all dependencies for compatibility issues"""
    logger.info("\n===== Checking dependency compatibility =====")
    
    # Check Python version
    logger.info(f"Python version: {sys.version}")
    
    # List all installed packages
    logger.info("\nInstalled packages:")
    for pkg in pkg_resources.working_set:
        logger.info(f"{pkg.key}=={pkg.version}")
    
    # Check Flask and Werkzeug compatibility
    logger.info("\nChecking Flask and Werkzeug compatibility:")
    flask_werkzeug_compatible = check_flask_werkzeug_compatibility()
    
    if flask_werkzeug_compatible:
        logger.info("✅ Flask and Werkzeug appear to be compatible")
    else:
        logger.warning("⚠️ Flask and Werkzeug may have compatibility issues")
        logger.warning("   Consider updating requirements.txt with compatible versions")
    
    logger.info("\n===== Dependency check complete =====")
    return flask_werkzeug_compatible

if __name__ == "__main__":
    check_all_dependencies()