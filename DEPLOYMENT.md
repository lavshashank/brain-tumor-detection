# Deployment Guide

## Important: Model File Required
Before deploying, ensure `Final_Model.h5` is in the `Brain_Tumor_Detection` directory.

## Deployment Options

### Option 1: Render (Recommended)
1. Push your code to GitHub
2. Go to [render.com](https://render.com) and create a new Web Service
3. Connect your GitHub repository
4. Render will automatically detect `render.yaml` and deploy
5. Make sure to upload `Final_Model.h5` to the repository (or use a build script)

### Option 2: Railway
1. Push your code to GitHub
2. Go to [railway.app](https://railway.app) and create a new project
3. Connect your GitHub repository
4. Railway will automatically detect the `Procfile` and deploy
5. Upload `Final_Model.h5` to the repository

### Option 3: Heroku
1. Install Heroku CLI
2. Run: `heroku create your-app-name`
3. Run: `git push heroku main`
4. Upload `Final_Model.h5` to the repository

### Option 4: Docker
1. Build: `docker build -t brain-tumor-detection .`
2. Run: `docker run -p 5000:5000 brain-tumor-detection`
3. Make sure `Final_Model.h5` is in the directory when building

## Local Testing
```bash
cd Brain_Tumor_Detection
pip install -r requirements.txt
gunicorn app:app
```

