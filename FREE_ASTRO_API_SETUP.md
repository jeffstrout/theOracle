# 🆓 Free Astrology API Setup Guide

## Quick Setup: AstroAPI.com (Recommended)

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

### Step 4: Restart Backend
```bash
# Stop current backend (Ctrl+C in terminal)
cd backend
source venv/bin/activate
python main.py
```

## Alternative Free Options

### Option 2: RapidAPI Astrology
- **Free**: 100 requests/month
- **Setup**: https://rapidapi.com/astrology/api/astrology2
- **Good for**: Basic testing

### Option 3: Build Your Own
- **Use**: PyEphem or Swiss Ephemeris libraries
- **Pros**: Unlimited, offline
- **Cons**: More complex setup

## Current Status
- ✅ **Mock Data**: Working now (no API key needed)
- ⏳ **Real Data**: Ready when you add API key
- 🎯 **Recommendation**: Start with AstroAPI.com free tier

## Testing
1. Add real API key to `.env` file
2. Restart backend server
3. Generate personality assessment
4. Check console for "Making API call..." messages

Your Oracle app will automatically switch from mock data to real astrology data once you add the API key!