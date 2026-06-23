# Mail.tm Dashboard - Deployment Guide

## Project Structure

```
d-gig/
├── email_generator.py     # Generates temporary email accounts
├── proxy_server.py        # CORS proxy for Mail.tm API
├── index.html            # Client webmail dashboard UI
├── created_emails.pdf    # Generated emails (create via email_generator.py)
├── requirements.txt      # Python dependencies
├── Procfile             # Render deployment config
├── render.yaml          # Render service config
└── README.md            # This file
```

## Quick Start (Local Development)

### 1. Generate Email Accounts

```bash
python email_generator.py
```

This creates `created_emails.pdf` with temporary email accounts.

### 2. Start Proxy Server (Terminal 1)

```bash
python proxy_server.py
```

Server runs on `http://127.0.0.1:5000`

### 3. Open Dashboard

Open `index.html` in your browser, or visit:
```
http://127.0.0.1:5000
```

### 4. Login

- Use any email from `created_emails.pdf`
- Password: `YourGlobalPassword123!`

---

## Deployment to Render

### Prerequisites

1. Create a free account at [render.com](https://render.com)
2. Connect your GitHub repository (or use Render's Git integration)

### Deployment Steps

#### Option A: Using render.yaml (Recommended)

1. Push all files to GitHub (or Render's Git)
2. Go to [render.com](https://render.com) → New → Web Service
3. Connect your repository
4. Select branch (main/master)
5. **Build Command:** `pip install -r requirements.txt`
6. **Start Command:** `gunicorn proxy_server:app`
7. Choose **Free Plan**
8. Click Deploy

Render will automatically read `render.yaml` for configuration.

#### Option B: Manual Setup

1. Create new Web Service on Render
2. Connect your repo
3. Configure:
   - **Name:** `mail-dashboard` (or your preference)
   - **Runtime:** Python
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn proxy_server:app`
   - **Free Plan**
4. Set environment variable:
   - **FLASK_ENV:** `production`
5. Deploy

### After Deployment

- Render provides a public URL like: `https://mail-dashboard-xxxxx.onrender.com`
- Share this URL with your client
- Client enters email from `created_emails.pdf` and password: `YourGlobalPassword123!`

---

## Configuration

### Changing Master Password

Edit `email_generator.py` and `index.html`:

```python
# email_generator.py
MASTER_PASSWORD = "YourNewPassword123!"
```

```javascript
// index.html
const MASTER_PASSWORD = "YourNewPassword123!";
```

### Changing Number of Emails Generated

Edit `email_generator.py`:

```python
TOTAL_ACCOUNTS_NEEDED = 100  # Change this number
```

---

## Troubleshooting

### "Cannot access inbox" Error
- Ensure proxy server is running
- Verify email address and password are correct
- Check browser console for CORS errors

### 404 Error on Render
- Verify all files are pushed to GitHub
- Check build logs on Render dashboard
- Ensure Procfile and requirements.txt exist

### Render keeps crashing
- Check Application logs on Render
- Verify `requirements.txt` has all dependencies
- Ensure `proxy_server.py` uses `os.environ.get('PORT')`

---

## Important Notes

- ⏰ Mail.tm temporary emails expire after 24-48 hours
- 🔐 All emails use the same password (shown in PDF)
- 📧 The UI auto-detects API URL based on deployment location
- 🌐 CORS proxy is required because browsers block cross-origin API calls

---

## Files Reference

| File | Purpose |
|------|---------|
| `email_generator.py` | Creates temporary email accounts via Mail.tm API |
| `proxy_server.py` | Flask server that proxies requests and serves UI |
| `index.html` | Client-side webmail dashboard |
| `requirements.txt` | Python dependencies for deployment |
| `Procfile` | Tells Render how to start the app |
| `render.yaml` | Render service configuration |
| `created_emails.pdf` | Generated temporary emails (created by script) |

---

## Support

For issues with:
- **Mail.tm API:** https://mail.tm
- **Render deployment:** https://render.com/docs
- **Flask:** https://flask.palletsprojects.com/
