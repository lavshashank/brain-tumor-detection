# Deploy to Render - Quick Guide

## Steps to Deploy:

1. **Go to Render Dashboard**
   - Visit: https://dashboard.render.com
   - Sign in or create an account (free tier available)

2. **Create New Web Service**
   - Click "New +" button
   - Select "Web Service"
   - Connect your GitHub account if not already connected

3. **Connect Repository**
   - Select repository: `lavshashank/brain-tumor-detection`
   - Render will auto-detect the `render.yaml` file

4. **Configure Service** (if auto-detection doesn't work)
   - **Name:** brain-tumor-detection
   - **Environment:** Python 3
   - **Build Command:** `cd Brain_Tumor_Detection && pip install -r requirements.txt`
   - **Start Command:** `cd Brain_Tumor_Detection && gunicorn app:app`
   - **Plan:** Free (or Starter if you need more resources)

5. **Important: Add Model File**
   - You'll need to add `Final_Model.h5` to your repository
   - Or use Render's environment variables/secrets for file storage
   - The model file should be in the `Brain_Tumor_Detection` directory

6. **Deploy**
   - Click "Create Web Service"
   - Render will build and deploy your app
   - Wait for deployment to complete (usually 5-10 minutes)

7. **Your App URL**
   - Once deployed, you'll get a URL like: `https://brain-tumor-detection.onrender.com`

## Notes:
- Free tier has limitations (spins down after inactivity)
- First deployment may take longer due to TensorFlow installation
- Make sure `Final_Model.h5` is in the repository before deploying

