# Nova AI - Voice Assistant

Nova is a voice-controlled assistant that helps you book cabs and more. This project uses Flask for the web interface and integrates with various voice and browser automation technologies.

> **Note**: This project has been updated to fix deployment issues on Render.com by addressing dependency compatibility problems.

## Features

- Voice-controlled cab booking
- Web interface to start the assistant
- Automated browser interactions
- Speech recognition and text-to-speech capabilities

## Prerequisites

- Python 3.9.18 (recommended for deployment compatibility)
- Chrome browser
- Required Python packages (see requirements.txt)

## Local Development

### Option 1: Using the Setup Script (Recommended)

1. Clone the repository
2. Run the setup script:
   ```
   python setup.py
   ```
3. Activate the virtual environment:
   ```
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```
4. Run the application:
   ```
   python app.py
   ```
5. Open your browser and navigate to `http://localhost:5000`

### Option 2: Manual Setup

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. If you encounter issues with undetected-chromedriver, install it manually:
   ```
   pip install undetected-chromedriver==3.5.5 --force-reinstall
   ```
5. Run the application:
   ```
   python app.py
   ```
6. Open your browser and navigate to `http://localhost:5000`

## Deployment to Railway

### Important Note About Railway Free Tier

The Railway free tier has limitations. As shown in the screenshot, the free tier may only allow deploying databases, not web services. To deploy this application, you may need to:

1. Upgrade to a paid plan
2. Use the Railway Pro trial
3. Consider alternative deployment platforms like Heroku, Render, or PythonAnywhere

### Step 1: Prepare Your Project

Ensure your project has the following files:
- `requirements.txt` - Lists all Python dependencies
- `runtime.txt` - Specifies Python version (python-3.10.13)
- `Procfile` - Tells Railway how to run your app (web: gunicorn app:app)
- `railway.toml` - Configuration file for Railway (included in this repository)

### Step 2: Create a Railway Account

1. Go to [Railway.app](https://railway.app/) and sign up for an account
2. Verify your email address
3. Consider upgrading to a paid plan if you encounter the "Limited Access" error

### Step 3: Install Railway CLI (Optional)

```
npm i -g @railway/cli
railway login
```

### Step 4: Deploy Your Project

#### Option 1: Deploy via GitHub

1. Push your code to a GitHub repository
2. Log in to Railway dashboard
3. Click "New Project" > "Deploy from GitHub repo"
4. Select your repository
5. Railway will automatically detect your Python app and deploy it

#### Option 2: Deploy via Railway CLI

```
cd nova-agentic-ai
railway init
railway up
```

### Step 5: Configure Environment Variables

1. In the Railway dashboard, go to your project
2. Click on the "Variables" tab
3. Add the following environment variables:
   - `RAILWAY_ENVIRONMENT=production`
   - Any other necessary environment variables

### Step 6: Monitor Your Deployment

1. In the Railway dashboard, go to your project
2. Click on the "Deployments" tab to see deployment status
3. Once deployed, click on "Generate Domain" to get a public URL

## Notes for Railway Deployment

- Railway automatically installs dependencies from requirements.txt
- The free tier has usage limits and may not allow web service deployments
- For browser automation, you may need to configure additional buildpacks or use a headless browser service

## Troubleshooting

### Local Development Issues

- **undetected-chromedriver not found error**: Run `pip install undetected-chromedriver==3.5.5 --force-reinstall`
- **Chrome version mismatch**: If you see an error about Chrome version not being supported, update the `version_main` parameter in the code to match your Chrome version
- **Chrome not launching**: Ensure Chrome is installed and the path is correct in the code
- **Speech recognition not working**: Check your microphone settings and ensure you have an active internet connection
- **Test Chrome installation**: Run `python test_chrome.py` to verify that undetected-chromedriver is working correctly

### Railway Deployment Issues

- **Limited Access Error**: This indicates your Railway account is on the free tier which may only allow database deployments. Consider upgrading your plan.
- **Deployment fails**: Check the logs in the Railway dashboard
- **Chrome/Selenium issues**: The application is configured to run in headless mode on Railway, but you may need additional configuration for browser automation in a cloud environment

## Deployment to Render.com

### Step 1: Prepare Your Project

Ensure your project has the following files:
- `requirements.txt` - Lists all Python dependencies with specific versions
- `runtime.txt` - Specifies Python version (python-3.9.18)
- `Procfile` - Tells Render how to run your app (web: gunicorn app:app)
- `render.yaml` - Configuration file for Render (included in this repository)
- `startup.sh` - Custom startup script to ensure proper environment setup

### Step 2: Create a Render Account

1. Go to [Render.com](https://render.com/) and sign up for an account
2. Verify your email address

### Step 3: Deploy Your Project

#### Option 1: Deploy via GitHub

1. Push your code to a GitHub repository
2. Log in to Render dashboard
3. Click "New" > "Web Service"
4. Select your repository
5. Configure the service:
   - Name: nova-agentic-ai
   - Environment: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `bash startup.sh`
6. Add environment variables:
   - `RENDER=true`
   - `PYTHON_VERSION=3.9.18`
7. Click "Create Web Service"

### Step 4: Monitor Your Deployment

1. In the Render dashboard, go to your web service
2. Click on the "Logs" tab to see deployment status
3. Once deployed, Render will provide a public URL

## Troubleshooting Render Deployment

### Common Issues and Solutions

- **Werkzeug Import Error**: If you see an error like `ImportError: cannot import name 'url_quote' from 'werkzeug.urls'`, ensure you're using compatible versions of Flask and Werkzeug. The current configuration uses Flask 2.0.1 with Werkzeug 2.0.3.

- **pkg_resources Deprecation Warning**: If you see warnings about pkg_resources being deprecated, you can ignore these or pin setuptools to a version below 81.0.0 as done in the requirements.txt file.

- **Chrome/Selenium Issues**: For headless browser automation on Render, the application uses specific Chrome options. If you encounter issues, check the logs and consider modifying the Chrome options in the code.

- **Deployment Fails**: Run the included diagnostic scripts to check your environment:
  ```
  python check_env.py
  python compatibility.py
  python deployment_check.py
  ```

- **Python Version Compatibility**: This project is configured to use Python 3.9.18 for maximum compatibility with all dependencies. If you change the Python version, you may need to adjust dependency versions.

## Alternative Deployment Options

If Render deployment is not suitable for your needs, consider these alternatives:

1. **Railway**: Similar to Render but with different tier limitations
2. **Heroku**: Popular platform for Python web applications
3. **PythonAnywhere**: Good for Python web applications
4. **Google Cloud Run**: Serverless deployment option with free tier