AI Assistant (Flask + Gemini)

A modern AI-powered web assistant built using Flask that integrates Google Gemini AI, real-time news APIs, and Wikipedia knowledge, with a clean ChatGPT-style interface.

---

Features

- AI Chat (Gemini API)
  Ask anything and get intelligent responses powered by Google Gemini.

- Real-Time News
  Fetch latest news using GNews API.

- Wikipedia Knowledge
  Get instant summaries for topics like "Who is Elon Musk".

- ChatGPT-style UI
  Clean dark theme with chat bubbles and responsive layout.

- Fallback System
  If AI fails, app still responds using news/wiki.

- Mobile Friendly
  Works smoothly on phone browsers (Termux compatible).

---

Tech Stack

- Backend: Flask (Python)
- Frontend: HTML, CSS, JavaScript
- APIs:
  - Google Gemini API
  - GNews API
  - Wikipedia REST API

---

Project Structure

ai/
├── app.py
├── requirements.txt
├── templates/
│   └── index.html
├── static/
│   └── style.css
├── .env
└── README.md

---

Setup Instructions

Clone Repository

git clone https://github.com/<your-username>/ai.git
cd ai

---

Install Dependencies

pip install -r requirements.txt

---

Add Environment Variables

Create a ".env" file:

GEMINI_API_KEY=your_gemini_key
GNEWS_API_KEY=your_gnews_key

---

Run the App

python app.py

Open in browser:

http://localhost:5000

---

Security Note

API keys are stored using environment variables (".env") and are not pushed to GitHub.

---

Deployment

You can deploy this project on:

- Render
- Railway
- Vercel (with backend proxy)

---

Future Improvements

- Chat history (memory)
- User authentication
- Dashboard and analytics
- Convert to mobile app
- Streaming responses (typing effect)
