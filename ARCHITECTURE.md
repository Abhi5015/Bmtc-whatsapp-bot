# 📐 SYSTEM ARCHITECTURE

## High-Level Architecture

```
┌─────────────────┐
│     USER        │
│   (WhatsApp)    │
└────────┬────────┘
         │
         ↓
┌─────────────────────────────────────────┐
│        TWILIO WHATSAPP API              │
│  (Receives/Sends WhatsApp Messages)     │
└────────┬────────────────────────────────┘
         │
         ↓ POST /whatsapp
┌─────────────────────────────────────────┐
│      FASTAPI BACKEND SERVER             │
│         (main.py)                       │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │   WhatsApp Webhook Handler      │   │
│  │   (whatsapp_webhook.py)         │   │
│  └─────────────┬───────────────────┘   │
│                │                        │
│                ↓                        │
│  ┌─────────────────────────────────┐   │
│  │   Message Processor             │   │
│  │   (message_processor.py)        │   │
│  └─────┬───────────────┬───────────┘   │
│        │               │                │
│        ↓               ↓                │
│  ┌──────────┐   ┌──────────────┐      │
│  │   NLP    │   │   Transit    │      │
│  │ Service  │   │   Provider   │      │
│  └────┬─────┘   └──────┬───────┘      │
└───────┼────────────────┼───────────────┘
        │                │
        ↓                ↓
┌──────────────┐  ┌─────────────────┐
│   ChatGPT    │  │  Transit APIs   │
│ (Intent ONLY)│  │ (Real Bus Data) │
└──────────────┘  └─────────────────┘
```

## Data Flow

### Example: "Next bus at Majestic"

```
1. User sends WhatsApp message
   ↓
2. Twilio receives message
   ↓
3. Twilio POST to /whatsapp webhook
   ↓
4. whatsapp_webhook.py extracts message body
   ↓
5. message_processor.py receives "Next bus at Majestic"
   ↓
6. nlp.py sends to ChatGPT: "Extract intent from: Next bus at Majestic"
   ↓
7. ChatGPT returns: {"intent": "eta", "stop_name": "Majestic"}
   ↓
8. message_processor.py calls transit_provider.get_arrivals("Majestic")
   ↓
9. transit API returns: [Bus(335E, 4min), Bus(G-4, 9min)]
   ↓
10. responses.py formats: "🚌 Buses arriving at Majestic\n• 335E - 4 min..."
    ↓
11. whatsapp_webhook.py creates TwiML response
    ↓
12. Twilio sends formatted message to user
    ↓
13. User receives reply on WhatsApp
```

## Component Responsibilities

### 1. **main.py**
- Initialize FastAPI app
- Define endpoints
- Handle startup/shutdown
- Configure logging

### 2. **whatsapp_webhook.py**
- Receive Twilio webhooks
- Parse form data
- Create TwiML responses
- Handle delivery status

### 3. **message_processor.py**
- Orchestrate processing flow
- Route based on intent
- Call appropriate handlers
- Handle errors gracefully

### 4. **nlp.py**
- Interface with ChatGPT
- Build prompts
- Parse JSON responses
- Extract intent & entities

### 5. **transit/provider.py**
- Define transit interface
- Abstract data models
- Ensure swappable providers

### 6. **transit/demo_provider.py**
- Implement transit interface
- Provide mock data
- **Replace with real API**

### 7. **responses.py**
- Format messages
- Add disclaimers
- Create templates
- Handle errors

### 8. **config.py**
- Manage environment vars
- Validate configuration
- Centralize settings

## Why This Architecture?

### ✅ Separation of Concerns
- Each component has one job
- Easy to test and debug
- Clear responsibilities

### ✅ Modular Design
- Swap ChatGPT with other NLPs
- Change transit providers easily
- Replace Twilio with Meta API

### ✅ Production Ready
- Error handling at each layer
- Logging throughout
- Configuration validation
- Stateless design

### ✅ Scalable
- Can add caching (Redis)
- Can add message queues
- Can deploy multiple instances
- Can add rate limiting

## Key Design Decisions

### 1. **ChatGPT for NLP ONLY**
❌ Don't: Ask ChatGPT for bus schedules
✅ Do: Ask ChatGPT to extract intent

### 2. **Transit API for Data ONLY**
❌ Don't: Use transit API for NLP
✅ Do: Use transit API for real-time data

### 3. **Twilio as Gateway**
- Handles WhatsApp protocol
- Manages phone numbers
- Provides webhooks
- Easy to replace later

### 4. **FastAPI as Backend**
- Modern async Python
- Auto documentation
- Type validation
- High performance

## Security Considerations

1. **API Keys**
   - Stored in `.env`
   - Never committed to Git
   - Rotated regularly

2. **Webhook Validation**
   - Can add Twilio signature verification
   - Rate limiting recommended
   - Input sanitization

3. **Error Messages**
   - Don't expose internal details
   - Log errors server-side
   - User-friendly messages

## Performance Optimizations

### Current:
- Synchronous processing
- No caching
- Direct API calls

### Future Improvements:
1. **Add Redis Caching**
   - Cache frequent queries
   - Reduce API calls
   - Faster responses

2. **Async Processing**
   - Queue long-running tasks
   - Background jobs
   - Webhook acknowledgment

3. **Load Balancing**
   - Multiple instances
   - Horizontal scaling
   - Auto-scaling

## Deployment Architecture

```
┌────────────────┐
│   CloudFlare   │ (Optional CDN/Protection)
└───────┬────────┘
        │
        ↓
┌────────────────┐
│  Load Balancer │ (Nginx/Cloud LB)
└───────┬────────┘
        │
        ├──────────┬──────────┐
        ↓          ↓          ↓
    ┌──────┐  ┌──────┐  ┌──────┐
    │ App  │  │ App  │  │ App  │ (FastAPI Instances)
    │  #1  │  │  #2  │  │  #3  │
    └───┬──┘  └───┬──┘  └───┬──┘
        │         │         │
        └────────┬┴─────────┘
                 ↓
         ┌──────────────┐
         │    Redis     │ (Caching)
         └──────────────┘
```

## Testing Strategy

1. **Unit Tests**
   - Test each component separately
   - Mock external APIs
   - Validate logic

2. **Integration Tests**
   - Test component interaction
   - End-to-end flows
   - Webhook handling

3. **Manual Tests**
   - Real WhatsApp messages
   - Edge cases
   - User experience

---

This architecture ensures:
- ✅ Clean separation of NLP and data
- ✅ Easy to maintain and extend
- ✅ Production-grade reliability
- ✅ Scalable design
