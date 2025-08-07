# Nova AI - Voice Assistant

Nova is a voice-controlled assistant that helps you book cabs and more. This project uses Flask for the web interface and integrates with various voice and browser automation technologies.

## Features

- Voice-controlled cab booking
- Web interface to start the assistant
- Automated browser interactions
- Speech recognition and text-to-speech capabilities

## Prerequisites

- Python 3.10.13
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

## Alternative Deployment Options

If Railway deployment is not possible due to the free tier limitations, consider these alternatives:

1. **Heroku**: Similar to Railway but with different free tier limitations
2. **Render**: Offers free tier for web services
3. **PythonAnywhere**: Good for Python web applications
4. **Google Cloud Run**: Serverless deployment option with free tier