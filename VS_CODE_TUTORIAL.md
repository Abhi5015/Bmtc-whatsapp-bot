# 📚 COMPLETE VS CODE TUTORIAL

## Step-by-Step Guide for Beginners

### ✅ Step 1: Verify You Have Python

Open PowerShell (or Terminal on Mac) and run:

```bash
python --version
```

Should show: `Python 3.9` or higher

**If not installed:**
- Windows: Download from https://python.org (✅ CHECK "Add to PATH")
- Mac: `brew install python3`

---

### ✅ Step 2: Navigate to Project Folder

In PowerShell:

```bash
cd Downloads\bmtc-whatsapp-bot
```

Verify you're in the right place:

```bash
ls
```

Should show: `main.py`, `config.py`, `requirements.txt`, etc.

---

### ✅ Step 3: Create Virtual Environment

```bash
python -m venv venv
```

**What this does:** Creates isolated Python environment in `venv` folder

---

### ✅ Step 4: Activate Virtual Environment

**Windows PowerShell:**
```bash
venv\Scripts\Activate.ps1
```

**If you get an error** about execution policy:
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try activating again.

**Alternative (Windows CMD):**
```bash
venv\Scripts\activate.bat
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

**Success indicator:**
You should see `(venv)` at the start of your prompt:
```
(venv) PS C:\Users\...\bmtc-whatsapp-bot>
```

---

### ✅ Step 5: Install Dependencies

**Make sure (venv) is showing!**

```bash
pip install -r requirements.txt
```

**This installs:**
- FastAPI (web framework)
- Twilio (WhatsApp)
- OpenAI (ChatGPT)
- And 6 other packages

**Wait 1-2 minutes...**

**Verify installation:**
```bash
pip list
```

Should show fastapi, twilio, openai, etc.

---

### ✅ Step 6: Create .env File

**Windows PowerShell:**
```bash
copy .env.example .env
```

**Mac/Linux:**
```bash
cp .env.example .env
```

---

### ✅ Step 7: Get API Keys

#### **7a. Get Twilio Credentials**

1. Go to https://console.twilio.com
2. Sign up (free trial available)
3. Dashboard → Account Info section:
   - Copy **Account SID** (starts with AC...)
   - Copy **Auth Token**
4. Go to: Messaging → Try it out → Send a WhatsApp message
5. Copy the **WhatsApp Sandbox Number** (like `whatsapp:+14155238886`)

#### **7b. Get OpenAI API Key**

1. Go to https://platform.openai.com
2. Sign up
3. Click your profile → View API Keys
4. Create new secret key
5. Copy the key (starts with `sk-`)
6. Add payment method (Billing section) - needs $5-10 for testing

---

### ✅ Step 8: Edit .env File

Open `.env` in VS Code (or any text editor):

```bash
code .env
```

Replace the placeholder values:

```env
TWILIO_ACCOUNT_SID=AC1234567890abcdef  # ← Paste your Twilio Account SID
TWILIO_AUTH_TOKEN=your_auth_token_here  # ← Paste your Twilio Auth Token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886  # ← Your sandbox number

OPENAI_API_KEY=sk-abc123xyz  # ← Paste your OpenAI API key
OPENAI_MODEL=gpt-4

HOST=0.0.0.0
PORT=8000
DEBUG=True
```

**Save the file!** (`Ctrl+S`)

---

### ✅ Step 9: Run the Server

```bash
python main.py
```

**Expected output:**
```
INFO:     Starting BMTC WhatsApp Bot...
INFO:     ✓ Configuration validated
INFO:     ✓ Twilio WhatsApp Number: whatsapp:+14155238886
INFO:     ✓ OpenAI Model: gpt-4
INFO:     ✓ Server ready to receive messages
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**✅ Success!** Your server is running!

---

### ✅ Step 10: Test Locally

Open browser: http://localhost:8000

Should see:
```json
{
  "status": "online",
  "service": "BMTC WhatsApp Bot",
  "version": "1.0.0"
}
```

**To stop server:** Press `Ctrl+C` in PowerShell

---

### ✅ Step 11: Expose to Internet (ngrok)

Twilio needs a public URL to send webhooks.

#### **Install ngrok:**

1. Download from https://ngrok.com/download
2. Extract the zip
3. Move `ngrok.exe` to your project folder (or add to PATH)
4. Sign up at ngrok.com
5. Copy your auth token from dashboard
6. Run:
```bash
ngrok config add-authtoken YOUR_AUTH_TOKEN
```

#### **Start ngrok tunnel:**

**Open a NEW PowerShell window** (keep server running in the first one!)

```bash
cd Downloads\bmtc-whatsapp-bot
ngrok http 8000
```

**Output:**
```
Forwarding  https://abc123.ngrok.io -> http://localhost:8000
```

**Copy the HTTPS URL:** `https://abc123.ngrok.io`

---

### ✅ Step 12: Configure Twilio Webhook

1. Go to: https://console.twilio.com
2. Navigate to: Messaging → Try it out → Send a WhatsApp message
3. Scroll to **Sandbox Configuration**
4. Under **"When a message comes in"**:
   - Paste: `https://abc123.ngrok.io/whatsapp`
   - Method: POST
5. Click **Save**

---

### ✅ Step 13: Join WhatsApp Sandbox

1. On the Twilio sandbox page, you'll see:
   ```
   join <random-code>
   ```
2. Open WhatsApp on your phone
3. Send message to the Twilio number: `join <random-code>`
4. You'll get a confirmation message

---

### ✅ Step 14: Test Your Bot!

Send these messages to the Twilio WhatsApp number:

**Test 1:**
```
help
```

**Expected response:**
```
👋 Welcome to BMTC Bot!

I can help you with:
🚌 Next Bus
🚍 Route Info
💰 Fare
...
```

**Test 2:**
```
Next bus at Majestic
```

**Expected response:**
```
🚌 Buses arriving at Majestic

• 335E to Kadugodi
  ⏱️ 4 min

• G-4 to Hebbal
  ⏱️ 9 min

ℹ️ Data from third-party transit sources...
```

**Test 3:**
```
Route 335E
```

**Test 4:**
```
Fare from Majestic to BTM
```

---

## 🐛 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'fastapi'"

**Problem:** Virtual environment not activated

**Fix:**
```bash
venv\Scripts\Activate.ps1
```

Look for `(venv)` prefix!

---

### Error: "Configuration error: Missing required configuration"

**Problem:** .env file not configured

**Fix:**
1. Make sure `.env` file exists (not `.env.example`)
2. Fill in all API keys
3. No extra spaces or quotes around values

---

### Error: "cannot be loaded because running scripts is disabled"

**Problem:** PowerShell execution policy

**Fix:**
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate venv again.

---

### Error: "Address already in use" or "Port 8000 is already in use"

**Problem:** Another app using port 8000

**Fix Option 1** - Use different port:
Edit `.env`:
```
PORT=8001
```

**Fix Option 2** - Kill existing process:
```bash
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F
```

---

### Twilio webhook not working

**Checklist:**
- ✅ Server is running (`python main.py`)
- ✅ ngrok is running (`ngrok http 8000`)
- ✅ Webhook URL in Twilio is: `https://YOUR-NGROK-URL/whatsapp`
- ✅ Webhook URL uses HTTPS (not HTTP)
- ✅ You joined the sandbox (`join <code>`)

---

### ChatGPT errors / OpenAI API errors

**Problem:** API key invalid or no credits

**Fix:**
1. Verify API key is correct in `.env`
2. Check OpenAI account has credits: https://platform.openai.com/account/billing
3. Try using `gpt-3.5-turbo` instead of `gpt-4` (cheaper):
   ```env
   OPENAI_MODEL=gpt-3.5-turbo
   ```

---

## 📊 Understanding the Code Flow

```
1. User sends WhatsApp message
   ↓
2. Twilio receives it
   ↓
3. Twilio POSTs to: https://your-ngrok-url/whatsapp
   ↓
4. main.py → whatsapp_webhook.py receives webhook
   ↓
5. message_processor.py processes message
   ↓
6. nlp.py sends to ChatGPT: "Extract intent from: Next bus at Majestic"
   ↓
7. ChatGPT returns: {"intent": "eta", "stop_name": "Majestic"}
   ↓
8. transit/demo_provider.py returns mock bus data
   ↓
9. responses.py formats the reply
   ↓
10. whatsapp_webhook.py sends TwiML response back to Twilio
    ↓
11. Twilio sends message to user's WhatsApp
```

---

## 📁 Project Files Explained

| File | What It Does |
|------|--------------|
| `main.py` | FastAPI server - entry point |
| `config.py` | Loads .env variables |
| `app/whatsapp_webhook.py` | Receives Twilio webhooks |
| `app/message_processor.py` | Main processing logic |
| `app/nlp.py` | ChatGPT integration (NLP ONLY) |
| `app/responses.py` | Formats WhatsApp messages |
| `app/transit/provider.py` | Transit provider interface |
| `app/transit/demo_provider.py` | Mock bus data (replace with real API) |

---

## 🚀 Next Steps

1. ✅ **Test with mock data** (done if you followed this guide!)
2. **Replace mock data** with real transit API:
   - Edit `app/transit/demo_provider.py`
   - Connect to Tummoc, Moovit, or BMTC APIs
3. **Deploy to production:**
   - Railway.app
   - Render.com
   - AWS/Google Cloud
4. **Switch to Meta Cloud API** (optional, for scale)

---

## 💡 Pro Tips

1. **Always activate venv** before running commands
2. **Keep ngrok running** while testing
3. **Check logs** when debugging:
   - Open `logs/app.log` in VS Code
   - Or run: `cat logs/app.log`
4. **Test locally first** before connecting WhatsApp
5. **Restart server** after changing code (Ctrl+C, then `python main.py`)

---

## 🎉 You Did It!

You now have a working WhatsApp bot that:

✅ Receives WhatsApp messages via Twilio
✅ Uses ChatGPT to understand user intent
✅ Fetches bus data from transit provider
✅ Sends formatted replies

**Celebrate! 🎊** This is production-grade code!

---

For more details, check:
- **README.md** - Full documentation
- **ARCHITECTURE.md** - System design
- **PROJECT_GUIDE.md** - File overview
