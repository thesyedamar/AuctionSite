# Deploying to kuberns.com

This guide will help you deploy your Django auction site to kuberns.com.

## Prerequisites

1. A GitHub account
2. Your code pushed to a GitHub repository
3. A kuberns.com account

## Files Created

- `Dockerfile` - Container configuration
- `.dockerignore` - Files to exclude from container
- `deploy.sh` - Deployment helper script
- Updated `settings.py` - Production-ready settings
- Updated `requirements.txt` - Added gunicorn and whitenoise

## Deployment Steps

### 1. Push to GitHub

```bash
# Initialize git if not already done
git init
git add .
git commit -m "Initial commit for kuberns deployment"

# Add remote and push
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

### 2. Deploy on kuberns.com

1. Go to [kuberns.com](https://kuberns.com)
2. Sign up/Login
3. Click "New App"
4. Connect your GitHub repository
5. Select the repository with your Django app
6. kuberns will automatically detect it's a Django app

### 3. Set Environment Variables

In the kuberns dashboard, add these environment variables:

```
SECRET_KEY=your-very-secure-secret-key-here
DEBUG=False
ALLOWED_HOSTS=.kuberns.app,localhost,127.0.0.1
```

### 4. Deploy

Click "Deploy" and wait for the build to complete.

### 5. Run Migrations

After deployment, go to the kuberns console and run:

```bash
python manage.py migrate
```

### 6. Access Your App

Your app will be available at: `https://your-app-name.kuberns.app`

## Environment Variables Explained

- `SECRET_KEY`: Django's secret key for security
- `DEBUG`: Set to False for production
- `ALLOWED_HOSTS`: Domains that can serve your app

## Troubleshooting

- If static files don't load, check that `STATIC_ROOT` is set correctly
- If you get database errors, run migrations in the console
- If the app doesn't start, check the logs in kuberns dashboard

## Security Notes

- Never commit your actual SECRET_KEY to git
- Always use environment variables for sensitive data
- Keep DEBUG=False in production
