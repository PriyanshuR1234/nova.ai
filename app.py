from flask import Flask, render_template, jsonify, request
import subprocess
import threading
import os
import sys
import logging
import importlib.util
import traceback

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Run pre-start checks
try:
    # Check if pre_start module exists and run checks
    if importlib.util.find_spec("pre_start") is not None:
        import pre_start
        pre_start.run_checks()
    else:
        logger.warning("pre_start module not found, skipping pre-start checks")
        
    # Check for werkzeug.urls.url_quote (the specific import that fails in the error log)
    try:
        from werkzeug.urls import url_quote
        logger.info("Successfully imported url_quote from werkzeug.urls")
    except ImportError as e:
        logger.error(f"ImportError: {e}")
        logger.error("This is likely causing the deployment error on Render")
        logger.error("Please ensure werkzeug==2.0.3 is installed")
        
        # Try to fix the issue by installing the correct version
        if os.environ.get('RENDER'):
            logger.info("Attempting to fix werkzeug version...")
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", "werkzeug==2.0.3"], 
                              check=True, capture_output=True)
                logger.info("Successfully installed werkzeug==2.0.3")
                
                # Try importing again
                try:
                    from werkzeug.urls import url_quote
                    logger.info("Successfully imported url_quote after fixing werkzeug version")
                except ImportError as e:
                    logger.error(f"Still cannot import url_quote after fixing werkzeug version: {e}")
            except subprocess.CalledProcessError as e:
                logger.error(f"Failed to install werkzeug==2.0.3: {e.stderr}")
            except Exception as e:
                logger.error(f"Unexpected error while fixing werkzeug version: {e}")
                
except Exception as e:
    logger.error(f"Error during pre-start checks: {e}")
    logger.error(traceback.format_exc())

# Configure Flask app
app = Flask(__name__)

# Set environment configuration
app.config['PRODUCTION'] = os.environ.get('RENDER', False)

# Disable debug mode in production
app.config['DEBUG'] = not app.config['PRODUCTION']

def run_nova():
    try:
        logger.info("Starting Nova AI assistant...")
        # Use absolute path for better reliability in production
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "main.py")
        result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
        
        if result.returncode != 0:
            logger.error(f"Nova process failed with error: {result.stderr}")
            return False
        
        logger.info("Nova AI assistant started successfully")
        return True
    except Exception as e:
        logger.exception(f"Error running Nova: {e}")
        return False

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start():
    try:
        logger.info("Received request to start Nova")
        # Use a daemon thread to ensure it doesn't block app shutdown
        thread = threading.Thread(target=run_nova, daemon=True)
        thread.start()
        logger.info("Nova thread started")
        return jsonify({"message": "Nova started successfully!", "status": "success"})
    except Exception as e:
        logger.exception(f"Failed to start Nova: {e}")
        return jsonify({"message": f"Failed to start Nova: {str(e)}", "status": "error"}), 500

# Add a health check endpoint for monitoring
@app.route("/health")
def health_check():
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    # Use environment variables for host and port if available
    port = int(os.environ.get("PORT", 5000))
    
    # Log startup information
    logger.info(f"Starting Nova AI web server on port {port}")
    logger.info(f"Production mode: {app.config['PRODUCTION']}")
    
    # Run the Flask app
    app.run(host="0.0.0.0", port=port, debug=app.config['DEBUG'])
