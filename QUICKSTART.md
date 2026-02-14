# 🚀 QUICK START GUIDE - 5 MINUTES

Follow these exact steps in VS Code:

## ✅ Step 1: Open Terminal in VS Code

Press: **Ctrl + `** (or **Cmd + `** on Mac)

## ✅ Step 2: Navigate to Project

```bash
cd bmtc-whatsapp-bot
```

## ✅ Step 3: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see **(venv)** appear in your terminal.

## ✅ Step 4: Install Everything

```bash
pip install -r requirements.txt
```

Wait 1-2 minutes...

## ✅ Step 5: Create Environment File

**Windows:**
```bash
copy .env.example .env
```

**Mac/Linux:**
```bash
cp .env.example .env
```

## ✅ Step 6: Add Your API Keys

Open `.env` file in VS Code and replace:

1. **Twilio credentials** (get from https://console.twilio.com)
2. **OpenAI key** (get from https://platform.openai.com)

Save the file!

## ✅ Step 7: Create Logs Folder

```bash
mkdir logs
```

## ✅ Step 8: Run the Server

```bash
python main.py
```

You should see:
```
✓ Configuration validated
✓ Server ready to receive messages
Uvicorn running on http://0.0.0.0:8000
```

## ✅ Step 9: Test in Browser

Open: http://localhost:8000

Should show: `"status": "online"`

## ✅ Step 10: Connect to WhatsApp

### Option A: Quick Test (ngrok)

1. Download ngrok: https://ngrok.com/download
2. Open NEW terminal
3. Run:
```bash
ngrok http 8000
```
4. Copy the HTTPS URL (e.g., https://abc123.ngrok.io)
5. Go to Twilio Console → WhatsApp Sandbox Settings
6. Paste: `https://abc123.ngrok.io/whatsapp` in webhook URL
7. Save!

### Option B: Deploy (Production)

See README.md for deployment instructions.

## 🎉 Done! Test Your Bot

1. Join Twilio WhatsApp sandbox (send join code)
2. Send: "help"
3. Send: "Next bus at Majestic"

---

## 🆘 Common Errors

### "No module named 'fastapi'"
→ You forgot to activate venv. Run: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)

### "Configuration error"
→ Check `.env` file has correct API keys

### "Port already in use"
→ Change PORT in `.env` to 8001

---

**Need help?** Read the full README.md
