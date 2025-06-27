# 🆓 Free Astrology API Setup Guide

The Oracle app now supports **multiple astrology API providers** with automatic fallback for maximum reliability!

## 🏆 Recommended Setup: Prokerala (New!)

### Why Prokerala?
- **5000 free requests/month** (5x more than AstroAPI.com)
- Professional Vedic & Western astrology
- Better free tier for development

### Step 1: Sign Up for Free
1. Go to https://api.prokerala.com
2. Click "Get Started" or "Sign Up"
3. Create a free account
4. Verify your email

### Step 2: Get Your API Credentials
1. Log into your Prokerala dashboard
2. Create an API application
3. Copy your **Client ID** and **Client Secret**
4. You get **5000 free requests per month**

### Step 3: Add Prokerala to Oracle
1. Open: `/Users/jeffstrout/Projects/theOracle/backend/.env`
2. Replace these lines:
   ```
   PROKERALA_CLIENT_ID=YOUR_PROKERALA_CLIENT_ID_HERE
   PROKERALA_CLIENT_SECRET=YOUR_PROKERALA_CLIENT_SECRET_HERE
   ```
3. With your actual credentials:
   ```
   PROKERALA_CLIENT_ID=your_actual_client_id
   PROKERALA_CLIENT_SECRET=your_actual_client_secret
   ```

## 🥈 Alternative: AstroAPI.com

### Step 1: Sign Up for Free
1. Go to https://astroapi.com
2. Click "Sign Up" or "Get API Key"
3. Create a free account
4. Verify your email

### Step 2: Get Your API Key
1. Log into your AstroAPI.com dashboard
2. Copy your API key from the dashboard
3. You get **1000 free requests per month**

### Step 3: Add API Key to Oracle
1. Open: `/Users/jeffstrout/Projects/theOracle/backend/.env`
2. Replace: `ASTRO_API_KEY=YOUR_ACTUAL_API_KEY_HERE`
3. With: `ASTRO_API_KEY=your_real_api_key_here`

## 🔧 Restart Backend
```bash
# Stop current backend (Ctrl+C in terminal)
cd backend
source venv/bin/activate
python main.py
```

## 🚀 Multi-Provider Fallback System

The Oracle app automatically tries providers in this order:
1. **Primary**: AstroAPI.com (if configured)
2. **Secondary**: Prokerala (if configured)
3. **Fallback**: Mock data (always works)

### Benefits:
- ✅ **Higher Reliability**: Multiple API sources
- ✅ **Better Free Tiers**: More monthly requests
- ✅ **Automatic Fallback**: Never fails completely
- ✅ **Development Friendly**: Mock data when APIs are down

## 📊 Provider Comparison

| Provider | Free Requests | Authentication | Data Quality |
|----------|--------------|----------------|--------------|
| **Prokerala** | 5,000/month | OAuth2 | Vedic + Western |
| **AstroAPI.com** | 1,000/month | API Key | Western focused |
| **Mock Data** | Unlimited | None | Development only |

## 🧪 Testing Your Setup

1. Add API credentials to `.env` file
2. Restart backend server
3. Generate personality assessment
4. Check console logs for:
   - "Starting multi-provider astrology data fetch..."
   - "Successfully retrieved data from [provider]"

## 💡 Pro Tips

- **Use both APIs**: Configure both for maximum requests
- **Monitor usage**: Check your API dashboards regularly
- **Development**: Mock data works perfectly for testing UI
- **Production**: Real APIs provide accurate personality assessments

Your Oracle app will automatically use the best available data source!