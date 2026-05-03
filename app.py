from dotenv import load_dotenv
load_dotenv()
from flask import Flask, request, jsonify, render_template
import requests
import urllib.parse
import os
app = Flask(__name__)

# 🔑 ADD YOUR KEYS

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")

# ------------------ NEWS ------------------
def get_news(query):
    try:
        url = f"https://gnews.io/api/v4/search?q={query}&lang=en&max=5&token={GNEWS_API_KEY}"
        res = requests.get(url, timeout=10)
        data = res.json()

        articles = data.get("articles", [])
        if not articles:
            return "❌ No news found."

        return "\n\n".join([
            f"• {a.get('title','')}\n🔗 {a.get('url','')}"
            for a in articles
        ])

    except Exception as e:
        print("News Error:", e)
        return "⚠️ News error"


# ------------------ WIKIPEDIA ------------------
def get_info(topic):
    try:
        topic = urllib.parse.quote(topic.strip())

        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic}"

        headers = {"User-Agent": "Mozilla/5.0"}

        res = requests.get(url, headers=headers, timeout=10)

        if res.status_code != 200:
            return "❌ No info found."

        data = res.json()

        return (
            f"📘 {data.get('title','')}\n\n"
            f"{data.get('extract','')}\n\n"
            f"🔗 {data.get('content_urls',{}).get('desktop',{}).get('page','')}"
        )

    except Exception as e:
        print("Wiki Error:", e)
        return "⚠️ Wiki error"


# ------------------ GEMINI (FINAL WORKING) ------------------
def gemini_ai(msg):
    try:
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

        payload = {
            "contents": [
                {"parts": [{"text": msg}]}
            ]
        }

        headers = {"Content-Type": "application/json"}

        res = requests.post(url, headers=headers, json=payload, timeout=15)

        print("AI STATUS:", res.status_code)
        print("AI RAW:", res.text[:200])

        if res.status_code != 200:
            return None

        data = res.json()

        # ✅ SAFE PARSE
        candidates = data.get("candidates", [])
        if not candidates:
            return None

        parts = candidates[0].get("content", {}).get("parts", [])

        for p in parts:
            if "text" in p:
                return p["text"]

        return None

    except Exception as e:
        print("Gemini Error:", e)
        return None


# ------------------ FALLBACK ------------------
def fallback(msg):
    return f"""
🤖 AI temporarily unavailable

You asked: {msg}

Try:
👉 latest tech news
👉 about India
👉 who is Elon Musk
"""


# ------------------ INTENT ------------------
def detect_intent(msg):
    msg = msg.lower()

    if "news" in msg or "latest" in msg:
        return "news"

    elif any(msg.startswith(k) for k in ["who is", "what is", "about", "tell me about"]):
        return "info"

    return "ai"


# ------------------ TOPIC ------------------
def extract_topic(msg):
    msg = msg.lower()

    for k in ["who is", "what is", "about", "tell me about"]:
        if msg.startswith(k):
            return msg.replace(k, "").strip()

    return msg


# ------------------ ENGINE ------------------
def generate_reply(msg):
    intent = detect_intent(msg)

    if intent == "news":
        return f"📰 Latest News:\n\n{get_news(msg)}"

    elif intent == "info":
        topic = extract_topic(msg)
        return get_info(topic)

    else:
        ai = gemini_ai(msg)
        return ai if ai else fallback(msg)


# ------------------ ROUTES ------------------
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message", "")
    reply = generate_reply(user_msg)
    return jsonify({"reply": reply})


# ------------------ RUN ------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
chat_history = []

def generate_reply(msg):
    chat_history.append({"role": "user", "text": msg})

    # send last few messages to Gemini
