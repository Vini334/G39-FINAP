# 🚀 Quick Setup Guide - FINAP

## 📋 Prerequisites

- **Node.js**: v18+ (LTS recommended)
- **Python**: 3.11+
- **Git**: Latest version
- **Firebase Account**: For Firestore and Auth
- **Google Cloud Account**: For deployment
- **Twilio Account**: For WhatsApp integration
- **Gemini API Key**: For AI assistant

## 🎯 Quick Start (< 30 minutes)

### Step 1: Clone and Setup Repository

```bash
# Clone the repository
git clone https://github.com/finap/finap-app.git
cd finap-app

# Create branch for development
git checkout -b develop
```

### Step 2: Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
```

#### Configure Backend Environment Variables

Edit `backend/.env`:

```env
# Application
APP_NAME=FINAP API
APP_VERSION=1.0.0
DEBUG=True
ENV=development

# API
API_V1_PREFIX=/api/v1
ALLOWED_ORIGINS=["http://localhost:19006","http://localhost:3000","exp://"]

# Security
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# Firebase (Get from Firebase Console)
FIREBASE_PROJECT_ID=finap-dev
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
FIREBASE_CLIENT_EMAIL=firebase-adminsdk@finap-dev.iam.gserviceaccount.com

# Gemini AI (Get from Google AI Studio)
GEMINI_API_KEY=your-gemini-api-key

# Twilio (Get from Twilio Console)
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_WHATSAPP_NUMBER=+14155238886

# Redis (Optional for development)
REDIS_URL=redis://localhost:6379

# Monitoring (Optional)
SENTRY_DSN=
```

#### Run Backend

```bash
# Run development server
uvicorn main:app --reload --port 8000

# Or with custom host
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend should be running at: `http://localhost:8000`
API Docs available at: `http://localhost:8000/docs`

### Step 3: Frontend Setup

Open new terminal:

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install
# or
yarn install

# Create .env file
cp .env.example .env
```

#### Configure Frontend Environment Variables

Edit `frontend/.env`:

```env
# API Configuration
EXPO_PUBLIC_API_URL=http://localhost:8000
EXPO_PUBLIC_API_VERSION=v1

# Firebase Web Config (Get from Firebase Console)
EXPO_PUBLIC_FIREBASE_API_KEY=your-firebase-api-key
EXPO_PUBLIC_FIREBASE_AUTH_DOMAIN=finap-dev.firebaseapp.com
EXPO_PUBLIC_FIREBASE_PROJECT_ID=finap-dev
EXPO_PUBLIC_FIREBASE_STORAGE_BUCKET=finap-dev.appspot.com
EXPO_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=123456789
EXPO_PUBLIC_FIREBASE_APP_ID=1:123456789:web:abcdef

# Features Flags
EXPO_PUBLIC_ENABLE_WHATSAPP=true
EXPO_PUBLIC_ENABLE_GAMIFICATION=true
EXPO_PUBLIC_ENABLE_SOCIAL=false

# Development
EXPO_PUBLIC_ENV=development
EXPO_PUBLIC_DEBUG=true
```

#### Run Frontend

```bash
# Start Expo development server
npx expo start

# Or with specific platform
npx expo start --ios
npx expo start --android
npx expo start --web
```

Metro Bundler will start at: `http://localhost:19000`

### Step 4: Firebase Setup

1. **Create Firebase Project**
   ```
   1. Go to https://console.firebase.google.com
   2. Click "Create Project"
   3. Name it "finap-dev"
   4. Disable Google Analytics (for now)
   ```

2. **Enable Firestore**
   ```
   1. Go to Firestore Database
   2. Click "Create Database"
   3. Choose "Start in test mode"
   4. Select location closest to you
   ```

3. **Enable Authentication**
   ```
   1. Go to Authentication
   2. Click "Get Started"
   3. Enable Email/Password provider
   4. Optional: Enable Google Sign-In
   ```

4. **Get Service Account Key**
   ```
   1. Go to Project Settings > Service Accounts
   2. Click "Generate New Private Key"
   3. Save the JSON file
   4. Copy contents to backend .env (FIREBASE_PRIVATE_KEY, etc)
   ```

5. **Get Web App Config**
   ```
   1. Go to Project Settings > General
   2. Add Web App
   3. Copy config to frontend .env
   ```

### Step 5: Initialize Database

```bash
# In backend directory
python scripts/init_db.py
```

This creates initial collections and sample data.

## 🧪 Testing the Setup

### 1. Test Backend Health

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

### 2. Test Registration

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test123!",
    "name": "Test User"
  }'
```

### 3. Test Frontend Connection

1. Open Expo app on your phone
2. Scan QR code from Metro Bundler
3. App should load without errors
4. Try registering a new account

## 🛠️ Development Workflow

### 1. Feature Development

```bash
# Create feature branch
git checkout -b feature/FINAP-123-transaction-crud

# Make changes
# Test locally
# Commit with conventional commits
git add .
git commit -m "feat: add transaction CRUD operations"

# Push to remote
git push origin feature/FINAP-123-transaction-crud

# Create Pull Request
```

### 2. Running Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

### 3. Code Quality

```bash
# Backend linting
cd backend
black .
ruff check .

# Frontend linting
cd frontend
npm run lint
npm run format
```

## 🐛 Common Issues & Solutions

### Issue 1: Firebase Connection Error

**Error**: `Firebase: No Firebase App '[DEFAULT]' has been created`

**Solution**:
```bash
# Verify Firebase credentials in .env
# Ensure service account JSON is properly formatted
# Check if Firebase project exists
```

### Issue 2: Expo Not Loading

**Error**: `Unable to resolve module`

**Solution**:
```bash
# Clear cache
npx expo start -c

# Reinstall dependencies
rm -rf node_modules
npm install
```

### Issue 3: Backend Import Errors

**Error**: `ModuleNotFoundError`

**Solution**:
```bash
# Ensure virtual environment is activated
# Reinstall requirements
pip install -r requirements.txt

# Add backend to PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd)
```

### Issue 4: CORS Errors

**Error**: `CORS policy: No 'Access-Control-Allow-Origin'`

**Solution**:
```python
# In backend/main.py, verify ALLOWED_ORIGINS includes your frontend URL
ALLOWED_ORIGINS = [
    "http://localhost:19006",
    "http://localhost:3000",
    "exp://192.168.x.x:19000"  # Your local IP
]
```

## 📱 Mobile Development Tips

### iOS Simulator
```bash
# Install Xcode from App Store
# Run iOS simulator
npx expo start --ios
```

### Android Emulator
```bash
# Install Android Studio
# Create AVD (Android Virtual Device)
# Run Android emulator
npx expo start --android
```

### Physical Device
```bash
# Install Expo Go app from App Store/Play Store
# Connect to same WiFi network
# Scan QR code from Metro Bundler
```

## 🚀 Deployment (Staging)

### Backend Deployment to Cloud Run

```bash
# Build Docker image
cd backend
docker build -t finap-api .

# Tag for Google Container Registry
docker tag finap-api gcr.io/finap-dev/finap-api

# Push to GCR
docker push gcr.io/finap-dev/finap-api

# Deploy to Cloud Run
gcloud run deploy finap-api \
  --image gcr.io/finap-dev/finap-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Frontend Build

```bash
# Build for production
cd frontend

# For Expo (EAS Build)
eas build --platform all

# For Web
npx expo export:web
```

## 📚 Essential Commands Cheat Sheet

```bash
# Backend
uvicorn main:app --reload          # Run backend
pytest                              # Run tests
black .                             # Format code
ruff check .                        # Lint code

# Frontend  
npx expo start                      # Start dev server
npm test                            # Run tests
npm run lint                        # Lint code
npx expo doctor                     # Check setup

# Git
git status                          # Check changes
git add .                           # Stage all changes
git commit -m "feat: message"       # Commit
git push origin branch-name         # Push to remote
git pull origin main                # Update from main

# Firebase
firebase init                       # Initialize Firebase
firebase deploy                     # Deploy to Firebase
firebase emulators:start            # Start local emulators

# Docker
docker-compose up                   # Start all services
docker-compose down                 # Stop all services
docker ps                           # List running containers
docker logs container-id            # View container logs
```

## 🔗 Important Links

- **Backend API Docs**: http://localhost:8000/docs
- **Frontend Dev Server**: http://localhost:19000
- **Firebase Console**: https://console.firebase.google.com
- **Google Cloud Console**: https://console.cloud.google.com
- **Twilio Console**: https://console.twilio.com
- **Gemini AI Studio**: https://makersuite.google.com

## 💡 Pro Tips

1. **Use Git Hooks**: Setup pre-commit hooks for automatic linting
2. **Environment Variables**: Never commit .env files
3. **Database Backups**: Regular Firestore exports
4. **API Testing**: Use Postman/Insomnia for API testing
5. **Mobile Testing**: Test on real devices regularly
6. **Performance**: Monitor bundle size and API response times
7. **Security**: Rotate API keys regularly
8. **Documentation**: Update docs as you code

## 🆘 Getting Help

- **Documentation**: Check `/docs` folder
- **Issues**: Create GitHub issue with details
- **Team Chat**: Slack channel #finap-dev
- **Email**: dev@finap.com.br

---

**Last Updated**: November 2024  
**Version**: 1.0.0  
**Maintainer**: FINAP Dev Team

## Next Steps

1. ✅ Complete setup
2. ⏳ Run tests to verify everything works
3. ⏳ Pick a task from the backlog
4. ⏳ Start coding!

Happy coding! 🚀
