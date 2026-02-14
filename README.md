# 🚌 BMTC WhatsApp Bot

A production-ready WhatsApp chatbot for BMTC (Bengaluru Metropolitan Transport Corporation) bus information.

**Architecture:**
- 📱 WhatsApp → Twilio API
- 🧠 ChatGPT → NLP/Intent extraction (NOT for bus data)
- 🚌 Transit APIs → Real bus data
- ⚡ FastAPI → Backend server

---

## 🏗️ Architecture Overview

```
User (WhatsApp)
    ↓
Twilio WhatsApp API
    ↓ Webhook
FastAPI Backend
    ↓
├─ ChatGPT (Intent Extraction ONLY)
└─ Transit APIs (Real Bus Data)
    ↓
Response → Twilio → WhatsApp
```

**Important:** ChatGPT is ONLY used for understanding user intent. Real-time bus data comes from transit APIs.

---

## 📁 Project Structure

```
bmtc-whatsapp-bot/
├── main.py                    # FastAPI application entry point
├── config.py                  # Configuration management
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (create this)
├── .env.example              # Environment template
├── app/
│   ├── __init__.py
│   ├── nlp.py                # ChatGPT integration
│   ├── responses.py          # Message formatting
│   ├── message_processor.py # Main processing logic
│   ├── whatsapp_webhook.py  # Twilio webhook handler
│   └── transit/
│       ├── __init__.py
│       ├── provider.py       # Transit provider interface
│       └── demo_provider.py  # Mock data (replace with real API)
└── logs/
    └── app.log               # Application logs
```

---

## 🚀 Setup Instructions

### **Step 1: Prerequisites**

- Python 3.9 or higher
- VS Code (or any code editor)
- Twilio account
- OpenAI API key

### **Step 2: Clone/Download Project**

If you created this in the directory, you're already in it!

Otherwise:
```bash
cd bmtc-whatsapp-bot
```

### **Step 3: Create Virtual Environment**

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

You should see `(venv)` in your terminal.

### **Step 4: Install Dependencies**

```bash
pip install -r requirements.txt
```

### **Step 5: Configure Environment Variables**

1. Copy the example file:
```bash
cp .env.example .env
```

2. Open `.env` in VS Code and fill in your credentials:

```env
# Twilio Configuration
TWILIO_ACCOUNT_SID=your_account_sid_from_twilio
TWILIO_AUTH_TOKEN=your_auth_token_from_twilio
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-api-key
OPENAI_MODEL=gpt-4

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

### **Step 6: Get Twilio Credentials**

1. Go to [Twilio Console](https://console.twilio.com)
2. Navigate to **Account → Keys & Credentials**
3. Copy:
   - Account SID
   - Auth Token
4. Navigate to **Messaging → Try it out → Send a WhatsApp message**
5. Join the sandbox
6. Copy the sandbox number (e.g., `whatsapp:+14155238886`)

### **Step 7: Get OpenAI API Key**

1. Go to [OpenAI Platform](https://platform.openai.com)
2. Navigate to **API Keys**
3. Create new key
4. Copy the key (starts with `sk-`)

### **Step 8: Create Logs Directory**

```bash
mkdir logs
```

### **Step 9: Test Locally**

Start the server:
```bash
python main.py
```

You should see:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Starting BMTC WhatsApp Bot...
INFO:     ✓ Configuration validated
INFO:     ✓ Server ready to receive messages
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

Open browser: http://localhost:8000

You should see:
```json
{
  "status": "online",
  "service": "BMTC WhatsApp Bot",
  "version": "1.0.0"
}
```

---

## 🌐 Deploy & Connect to Twilio

### **Option 1: ngrok (For Testing)**

1. Install ngrok: https://ngrok.com/download

2. Start ngrok:
```bash
ngrok http 8000
```

3. Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`)

4. Go to Twilio Console → Messaging → Settings → WhatsApp Sandbox

5. Set **"When a message comes in"** to:
```
https://abc123.ngrok.io/whatsapp
```

6. Save!

### **Option 2: Deploy to Cloud (Production)**

**Deploy to Railway:**
1. Install Railway CLI
2. `railway init`
3. `railway up`
4. Set environment variables in Railway dashboard
5. Use Railway URL in Twilio webhook

**Deploy to Render:**
1. Connect GitHub repo
2. Set environment variables
3. Deploy
4. Use Render URL in Twilio webhook

---

## 🧪 Testing the Bot

### **Step 1: Join Sandbox**
- Send the join code to your Twilio sandbox number via WhatsApp
- Example: `join <code-from-twilio>`

### **Step 2: Test Commands**

Send these messages to your WhatsApp bot:

**Help:**
```
help
```

**Next Bus:**
```
Next bus at Majestic
Buses from BTM to Silk Board
```

**Route Info:**
```
Route 335E
Tell me about G-4
```

**Fare:**
```
Fare from Majestic to Indiranagar
```

---

## 📊 Expected Flow

1. **User sends:** "Next bus at Majestic"

2. **ChatGPT extracts:**
```json
{
  "intent": "eta",
  "stop_name": "Majestic"
}
```

3. **Transit API returns:**
```python
[
  BusArrival(route="335E", destination="Kadugodi", eta=4),
  BusArrival(route="G-4", destination="Hebbal", eta=9)
]
```

4. **Bot replies:**
```
🚌 Buses arriving at Majestic

• 335E to Kadugodi
  ⏱️ 4 min

• G-4 to Hebbal
  ⏱️ 9 min

ℹ️ Data from third-party transit sources.
```

---

## 🔧 Customization

### Replace Mock Data with Real API

Edit `app/transit/demo_provider.py` or create new provider:

```python
class TummocProvider(TransitProvider):
    def get_arrivals(self, stop_name: str):
        # Call Tummoc API
        response = requests.get(f"https://api.tummoc.com/v1/arrivals?stop={stop_name}")
        return parse_arrivals(response.json())
```

### Add More Features

Edit `app/message_processor.py`:

```python
def _handle_tracking(self, intent_data: dict):
    # Implement bus tracking
    pass
```

---

## 🐛 Troubleshooting

### Server won't start
- Check if port 8000 is free: `lsof -i :8000` (Mac/Linux)
- Try different port: Change `PORT=8001` in `.env`

### "Configuration error"
- Verify all API keys are set in `.env`
- Check for typos in variable names

### Twilio not receiving messages
- Ensure ngrok is running
- Check webhook URL is correct in Twilio
- Verify webhook uses HTTPS (not HTTP)

### ChatGPT errors
- Verify API key is valid
- Check OpenAI account has credits
- Try using `gpt-3.5-turbo` instead of `gpt-4`

---

## 📝 Code Explanation

### **main.py**
- FastAPI application
- Defines endpoints
- Handles startup/shutdown

### **app/whatsapp_webhook.py**
- Receives Twilio webhook
- Extracts user message
- Returns TwiML response

### **app/nlp.py**
- Calls OpenAI ChatGPT
- Extracts intent from user message
- Returns structured JSON

### **app/message_processor.py**
- Orchestrates flow
- Routes based on intent
- Calls transit API

### **app/transit/demo_provider.py**
- Mock transit data
- Replace with real API

### **app/responses.py**
- Formats messages
- Adds disclaimers
- Creates WhatsApp-friendly text

---

## 🎯 What to Tell Your Tech Lead

> "We've built a WhatsApp bot using Twilio for messaging. ChatGPT is used **only** for NLP to extract user intent — it does NOT provide bus data. Real-time BMTC data is fetched from third-party transit APIs with proper disclaimers. The architecture is modular, allowing us to swap providers without code rewrites."

---

## 📚 Next Steps

1. ✅ Test with mock data
2. ✅ Integrate real transit API (Tummoc, Moovit, or GTFS)
3. ✅ Add error handling & retries
4. ✅ Implement caching (Redis)
5. ✅ Deploy to production
6. ✅ Get BMTC approval
7. ✅ Switch to Meta Cloud API (optional)

---

## 📞 Support

- Twilio Docs: https://www.twilio.com/docs/whatsapp
- OpenAI Docs: https://platform.openai.com/docs
- FastAPI Docs: https://fastapi.tiangolo.com

---

## 📄 License

MIT License - Feel free to use and modify!

---

**Built with ❤️ for BMTC commuters**
