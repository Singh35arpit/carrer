# 🔧 Troubleshooting Guide - CareerPath AI

## ✅ System Status Check

### **Quick Diagnostic Test:**

Visit: **http://localhost:5000/test**

This will automatically test:
- ✅ Server connectivity
- ✅ API endpoints
- ✅ Database connection
- ✅ Authentication system

---

## 🚨 Common Issues & Solutions

### **Issue 1: Site Not Loading / CodeWindow Error**

**Error Message:**
```
failed to load (reason: <unknown>, code: -3)
```

**Solutions:**

#### Solution A: Clear Browser Cache
1. Press `Ctrl + Shift + Delete`
2. Select "Cached images and files"
3. Click "Clear data"
4. Refresh page (`Ctrl + R`)

#### Solution B: Hard Refresh
```
Press: Ctrl + Shift + R
```

#### Solution C: Try Different Browser
- Chrome/Edge (Recommended)
- Firefox
- Safari

#### Solution D: Check Server
```bash
# Server should be running on:
http://localhost:5000
```

If not running:
```bash
cd c:\Users\ASUS\carrer
python web_app.py
```

---

### **Issue 2: Authenticator Not Working**

**Symptoms:**
- Login/Register buttons don't respond
- Forms don't submit
- No error messages

**Solutions:**

#### Solution A: Check JavaScript Console
1. Press `F12` to open Developer Tools
2. Go to "Console" tab
3. Look for red errors
4. Share the error message

#### Solution B: Verify API is Running
```bash
# Test authentication endpoint
curl http://localhost:5000/api/auth/me
```

Expected response:
```json
{"error": "Not authenticated", "success": false}
```

If you get this → API is working ✅
If error → Server needs restart

#### Solution C: Check Session Storage
1. Open DevTools (`F12`)
2. Go to Application tab
3. Check Session Storage
4. Should have `user_token` if logged in

#### Solution D: Restart Server
```bash
# Stop current server (Ctrl + C)
# Then restart:
python web_app.py
```

---

### **Issue 3: Pages Not Loading Styles**

**Symptoms:**
- Page loads but looks broken
- No colors or animations
- Plain HTML only

**Solutions:**

#### Solution A: Check Static Files
Verify these files exist:
```
c:\Users\ASUS\carrer\static\landing.css
c:\Users\ASUS\carrer\static\dashboard-dark.css
c:\Users\ASUS\carrer\static\auth-glass.css
```

#### Solution B: Check Browser Console
Look for 404 errors like:
```
Failed to load resource: net::ERR_ABORTED
```

#### Solution C: Clear CDN Cache
If using CDN, clear cache or use direct paths

---

### **Issue 4: Database Errors**

**Symptoms:**
- Careers not loading
- Skills not showing
- Search not working

**Solutions:**

#### Solution A: Verify Large Dataset Loaded
Visit:
```
http://localhost:5000/api/careers
http://localhost:5000/api/skills
```

Should return JSON with 500+ careers and 1700+ skills

#### Solution B: Check Python Imports
In terminal:
```bash
python -c "from src.data.large_career_db import career_database_large; print('OK')"
```

Should print: `OK`

#### Solution C: Restart with Clean State
```bash
# Stop server
# Clear __pycache__ folders
# Restart server
python web_app.py
```

---

### **Issue 5: Resume Upload Failing**

**Symptoms:**
- File upload doesn't work
- Analysis fails
- Timeout errors

**Solutions:**

#### Solution A: Verify Dependencies Installed
```bash
pip install spacy PyPDF2 python-docx
python -m spacy download en_core_web_sm
```

#### Solution B: Check File Size
- Max size: 16MB
- Supported formats: PDF, DOCX, TXT

#### Solution C: Check Server Logs
Look for errors in terminal where server is running

---

## 🔍 Diagnostic Commands

### **Test All Endpoints:**

```bash
# 1. Test Server
curl http://localhost:5000/

# 2. Test Careers API
curl http://localhost:5000/api/careers

# 3. Test Skills API
curl http://localhost:5000/api/skills

# 4. Test Auth API
curl http://localhost:5000/api/auth/me

# 5. Test Job Search
curl "http://localhost:5000/api/jobs/search?query=python"
```

### **Check Server Process:**

Windows PowerShell:
```powershell
Get-Process python
```

### **Check Port Usage:**

```powershell
netstat -ano | findstr :5000
```

---

## 💡 Quick Fixes

### **Fix 1: Server Won't Start**

**Problem:** Port 5000 already in use

**Solution:**
```bash
# Find process using port 5000
netstat -ano | findstr :5000

# Kill process (replace PID with actual number)
taskkill /PID <PID> /F

# Restart server
python web_app.py
```

### **Fix 2: Module Not Found Errors**

**Problem:** Missing Python packages

**Solution:**
```bash
pip install flask flask-cors scikit-learn numpy pandas
pip install spacy PyPDF2 python-docx requests
python -m spacy download en_core_web_sm
```

### **Fix 3: Browser Shows Old Version**

**Problem:** Cached files

**Solution:**
1. Clear browser cache completely
2. Use Incognito/Private mode
3. Add version parameter to URLs:
   ```html
   <link rel="stylesheet" href="/static/style.css?v=2">
   ```

---

## 🎯 Step-by-Step Debugging

### **When Something Doesn't Work:**

1. **Check Server First**
   ```
   Is server running? → Yes → Continue
                     → No → Start it
   ```

2. **Check Browser Console**
   ```
   Press F12 → Console tab
   Look for red errors
   Note the error message
   ```

3. **Check Network Tab**
   ```
   F12 → Network tab
   Refresh page
   Look for failed requests (red)
   Check status codes
   ```

4. **Test Specific Feature**
   ```
   Visit /test page
   See which tests fail
   Focus on that component
   ```

5. **Check Logs**
   ```
   Look at terminal output
   Find error messages
   Search for stack traces
   ```

---

## 📞 Getting Help

### **Information to Provide:**

1. **Error Message** (exact text)
2. **Browser Console** errors (screenshot)
3. **Network Tab** failures (screenshot)
4. **Server Logs** (last 20 lines)
5. **What you were trying to do**
6. **What happened instead**

### **Collect Server Logs:**

In terminal where server is running:
1. Select all text
2. Copy
3. Paste into a file
4. Share the relevant error part

---

## 🎊 Verification Checklist

After fixing, verify:

- [ ] Server starts without errors
- [ ] Landing page loads at http://localhost:5000
- [ ] Can navigate to /auth
- [ ] Can register new account
- [ ] Can login successfully
- [ ] Dashboard loads after login
- [ ] Resume analyzer works
- [ ] Job search works
- [ ] Career roadmap works
- [ ] All styles and animations working

---

## 🚀 Performance Tips

### **If Site is Slow:**

1. **Disable Browser Extensions**
   - Some extensions interfere
   - Try Incognito mode

2. **Reduce Particle Count**
   Edit `landing.js`:
   ```javascript
   const particleCount = 30; // Instead of 50
   ```

3. **Enable Compression**
   Add to web_app.py:
   ```python
   from flask_compress import Compress
   Compress(app)
   ```

4. **Use Production Server**
   ```bash
   pip install gunicorn
   gunicorn web_app:app -w 4 -b 0.0.0.0:5000
   ```

---

## 🎉 Success Indicators

**Everything is Working When:**

✅ Server shows: "Running on http://127.0.0.1:5000"
✅ Test page shows all green checkmarks
✅ Can register and login
✅ Dashboard displays correctly
✅ All features accessible
✅ No console errors
✅ Fast response times

---

## 📚 Additional Resources

- **System Test Page:** http://localhost:5000/test
- **API Documentation:** See COMPLETE_FEATURES_GUIDE.md
- **Dataset Info:** See LARGE_DATASET_GUIDE.md
- **Resume Analyzer:** See RESUME_ANALYZER_GUIDE.md

---

**Last Updated:** March 16, 2026
**Version:** 2.0.0 (Large Dataset Edition)
