# SmartShop - Product Discovery Platform

A conversational AI-powered product discovery platform that helps users find the best products across multiple e-commerce platforms.

## 🚀 Quick Start (Hackathon Setup)

### 1. Setup Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Update `.env` file with your API keys:
- OpenAI API key for chatbot
- RapidAPI key for product searches
- MongoDB URI for data storage

### 3. Run the Application
```bash
source venv/bin/activate
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 🎯 Features

### Phase 1 (Current - Hackathon MVP)
- ✅ Conversational chatbot interface
- ✅ Smart requirement gathering
- ✅ Mock product data for demo
- ✅ Product comparison interface
- ✅ Multi-platform simulation

### Phase 2 (Post-Hackathon)
- 🔄 Real API integration (Amazon, Flipkart)
- 🔄 MongoDB integration for user sessions
- 🔄 Advanced filtering and sorting
- 🔄 Price history tracking
- 🔄 User preferences learning

## 🛠️ Tech Stack

- **Frontend:** Streamlit (Python web app framework)
- **Backend:** Python with Flask (for API layer)
- **Database:** MongoDB (user sessions, product cache)
- **AI:** OpenAI GPT-3.5 for conversational chatbot
- **APIs:** RapidAPI, Google Shopping API
- **Deployment:** Streamlit Cloud (for demo)

## 🏗️ Architecture

```
User Input → Streamlit UI → Chatbot Service → 
Requirement Clarification → Product Service → 
API Calls → MongoDB Cache → Product Matching → 
Comparison Results → Streamlit Display
```

## 📝 Usage Example

1. **User:** "I need a laptop"
2. **Bot:** "Great! What will you use it for - work, gaming, or studies?"
3. **User:** "Gaming and college work"
4. **Bot:** "What's your budget range?"
5. **User:** "Around 60k"
6. **Bot:** "Perfect! Let me find the best gaming laptops under ₹60,000..."
7. **App:** Shows comparison of 3-5 best matching products

## 🎯 Hackathon Strategy

### Demo Flow:
1. Show conversational requirement gathering
2. Demonstrate intelligent product matching
3. Display comprehensive comparison
4. Highlight multi-platform aggregation
5. Show potential for real API integration

### Key Differentiators:
- **Conversational Interface:** Not just keyword search
- **Requirement Clarification:** Handles vague/incomplete requests  
- **Multi-platform Aggregation:** One search, multiple sources
- **Intelligent Matching:** Based on actual needs, not just keywords

## 🚀 Deployment

For hackathon demo:
```bash
streamlit run app.py --server.port 8501
```

For production deployment, see deployment guide in `/docs/deployment.md`

## 🤝 Team

- **Product Discovery Platform** for Lords College Hackathon
- Built with ❤️ using Python & Streamlit

## 📈 Future Roadmap

1. **Real-time API Integration**
2. **Machine Learning for Better Matching**
3. **Price Alert System**
4. **Mobile App Development**
5. **Social Shopping Features**