#!/bin/bash

# Deploy script for kuberns.com

echo "🚀 Preparing Django app for kuberns.com deployment..."

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📁 Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit for kuberns deployment"
fi

echo "✅ Files ready for deployment!"
echo ""
echo "📋 Next steps:"
echo "1. Push your code to GitHub:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "2. Go to kuberns.com and:"
echo "   - Create new app"
echo "   - Connect your GitHub repository"
echo "   - Set environment variables:"
echo "     SECRET_KEY=your-secret-key-here"
echo "     DEBUG=False"
echo "     ALLOWED_HOSTS=.kuberns.app,localhost,127.0.0.1"
echo ""
echo "3. Deploy and wait for build to complete"
echo ""
echo "4. Run migrations in kuberns console:"
echo "   python manage.py migrate"
echo ""
echo "🎉 Your app will be live at: https://your-app-name.kuberns.app"
