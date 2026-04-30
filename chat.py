import streamlit as st
import time
import json
import re
import os
import hashlib
import requests
import math
import random
from datetime import datetime, timedelta
from collections import Counter
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import streamlit as st
import plotly.graph_objects as go


def hex_to_rgba(hex_color, alpha=0.2):
    try:
        if hex_color.startswith("#"):
            hex_color = hex_color.lstrip('#')
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            return f"rgba({r},{g},{b},{alpha})"
        else:
            return f"rgba(100,100,100,{alpha})"
    except:
        return f"rgba(100,100,100,{alpha})"



# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Phoenix · Multi-AI Studio v5",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── PHOENIX CSS v5 ───────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700;900&family=Crimson+Pro:ital,wght@0,300;0,400;0,600;1,400&family=JetBrains+Mono:wght@300;400;500;700&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; }

:root {
  --bg-base:     #060203;
  --bg-card:     #0d0406;
  --bg-input:    #140608;
  --bg-hover:    #1d0b0e;
  --border:      #2a1015;
  --border-glow: #ff6b3518;
  --accent:      #ff6b35;
  --accent2:     #f7c948;
  --accent3:     #e63946;
  --accent4:     #ff8c42;
  --ember:       #ff4500;
  --gold:        #f7c948;
  --text-pri:    #fdf0e8;
  --text-sec:    #c8917a;
  --text-muted:  #4a2a22;
  --success:     #52b788;
  --warning:     #f7c948;
  --danger:      #e63946;
  --purple:      #c084fc;
  --cyan:        #67e8f9;
  --font-head:   'Cinzel', serif;
  --font-body:   'Crimson Pro', serif;
  --font-code:   'JetBrains Mono', monospace;
}

@keyframes flicker    { 0%,100%{opacity:1;filter:brightness(1)}50%{opacity:.92;filter:brightness(1.08)}75%{opacity:.97} }
@keyframes emberGlow  { 0%,100%{box-shadow:0 0 8px #ff6b3540,0 0 20px #ff6b3520}50%{box-shadow:0 0 16px #ff6b3570,0 0 40px #ff6b3530,0 0 60px #f7c94810} }
@keyframes rise       { from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:translateY(0)} }
@keyframes pulse      { 0%,100%{opacity:1}50%{opacity:.35} }
@keyframes bounce     { 0%,80%,100%{transform:translateY(0);opacity:.3}40%{transform:translateY(-9px);opacity:1} }
@keyframes gridMove   { 0%{background-position:0 0}100%{background-position:44px 44px} }
@keyframes shimmer    { 0%{background-position:-200% 0}100%{background-position:200% 0} }
@keyframes float      { 0%,100%{transform:translateY(0)}50%{transform:translateY(-5px)} }
@keyframes burnIn     { 0%{opacity:0;filter:blur(4px) brightness(2)}100%{opacity:1;filter:blur(0) brightness(1)} }
@keyframes spin       { from{transform:rotate(0deg)}to{transform:rotate(360deg)} }
@keyframes gradShift  { 0%{background-position:0% 50%}50%{background-position:100% 50%}100%{background-position:0% 50%} }

.stApp {
  background: var(--bg-base) !important;
  font-family: var(--font-body) !important;
  color: var(--text-pri) !important;
}
.stApp::before {
  content: '';
  position: fixed; inset: 0;
  background-image:
    linear-gradient(rgba(255,107,53,0.025) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,107,53,0.025) 1px, transparent 1px);
  background-size: 44px 44px;
  animation: gridMove 12s linear infinite;
  pointer-events: none; z-index: 0;
}

[data-testid="stSidebar"] {
  background: var(--bg-card) !important;
  border-right: 1px solid var(--border) !important;
  box-shadow: 4px 0 40px rgba(255,107,53,0.06) !important;
}
[data-testid="stSidebar"] > div:first-child { padding-top: 0.5rem !important; }

h1,h2,h3 { font-family: var(--font-head) !important; letter-spacing: 1px; }

[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stChatInput"] textarea {
  background: var(--bg-input) !important;
  border: 1px solid var(--border) !important;
  border-radius: 8px !important;
  color: var(--text-pri) !important;
  font-family: var(--font-body) !important;
  font-size: 1rem !important;
  transition: all 0.3s ease !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
  border-color: var(--accent) !important;
  box-shadow: 0 0 0 2px rgba(255,107,53,0.12), 0 0 24px rgba(255,107,53,0.06) !important;
}
[data-testid="stChatInput"] {
  background: var(--bg-input) !important;
  border-top: 1px solid var(--border) !important;
}

.stButton > button {
  background: linear-gradient(135deg, #1d0b0e, #120608) !important;
  border: 1px solid #2a1015 !important;
  border-radius: 8px !important;
  color: var(--text-pri) !important;
  font-family: var(--font-body) !important;
  font-weight: 600 !important;
  transition: all 0.25s ease !important;
  position: relative !important;
  overflow: hidden !important;
}
.stButton > button:hover {
  border-color: var(--accent) !important;
  box-shadow: 0 0 20px rgba(255,107,53,0.2), inset 0 0 20px rgba(255,107,53,0.04) !important;
  transform: translateY(-1px) !important;
  color: var(--accent) !important;
}

[data-testid="stSelectbox"] > div > div {
  background: var(--bg-input) !important;
  border: 1px solid var(--border) !important;
  border-radius: 8px !important;
  color: var(--text-pri) !important;
}

[data-testid="stMetric"] {
  background: var(--bg-card) !important;
  border: 1px solid var(--border) !important;
  border-radius: 10px !important;
  padding: 1rem !important;
  transition: all 0.3s ease !important;
  animation: rise 0.4s ease !important;
}
[data-testid="stMetric"]:hover {
  border-color: var(--accent) !important;
  box-shadow: 0 0 20px rgba(255,107,53,0.1) !important;
}
[data-testid="stMetricLabel"] { color: var(--text-sec) !important; font-size: 0.72rem !important; letter-spacing: 1px; text-transform: uppercase; font-family: var(--font-code) !important; }
[data-testid="stMetricValue"] { color: var(--accent) !important; font-family: var(--font-head) !important; font-size: 1.4rem !important; }

[data-testid="stExpander"] {
  background: var(--bg-card) !important;
  border: 1px solid var(--border) !important;
  border-radius: 10px !important;
}
[data-testid="stExpander"]:hover { border-color: var(--accent) !important; }
[data-testid="stExpander"] summary { color: var(--text-sec) !important; font-family: var(--font-code) !important; font-size: 0.8rem !important; }

[data-testid="stTabs"] [data-baseweb="tab-list"] {
  background: var(--bg-card) !important;
  border-radius: 10px !important;
  padding: 4px !important;
  gap: 4px !important;
  border: 1px solid var(--border) !important;
  flex-wrap: wrap !important;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
  background: transparent !important;
  color: var(--text-sec) !important;
  border-radius: 7px !important;
  font-family: var(--font-body) !important;
  font-weight: 600 !important;
  font-size: 0.88rem !important;
  transition: all 0.2s ease !important;
  white-space: nowrap !important;
}
[data-testid="stTabs"] [aria-selected="true"] {
  background: linear-gradient(135deg, #2a1015, #1d0b0e) !important;
  color: var(--accent) !important;
  box-shadow: 0 0 15px rgba(255,107,53,0.15) !important;
}

[data-testid="stChatMessage"] { background: transparent !important; border: none !important; padding: 0 !important; }

::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent); box-shadow: 0 0 8px var(--accent); }

[data-testid="stProgressBar"] > div > div {
  background: linear-gradient(90deg, var(--ember), var(--accent2)) !important;
  box-shadow: 0 0 10px var(--ember) !important;
}

hr { border-color: var(--border) !important; }
[data-testid="stDataFrame"] { border-radius: 10px !important; overflow: hidden !important; }
[data-testid="stAlert"] { border-radius: 10px !important; border-left-width: 3px !important; }

.msg-animate { animation: rise 0.35s ease forwards; }
.burn-in     { animation: burnIn 0.5s ease forwards; }

.phoenix-card {
  background: linear-gradient(135deg, var(--bg-card), var(--bg-base));
  border: 1px solid var(--border);
  border-radius: 14px;
  position: relative;
  overflow: hidden;
}
.phoenix-card::after {
  content: '';
  position: absolute; top: 0; left: 0; right: 0; height: 1px;
  background: linear-gradient(90deg, transparent, var(--accent), var(--accent2), transparent);
}

.sb-label {
  font-size: 0.66rem;
  color: var(--text-muted);
  letter-spacing: 2.5px;
  text-transform: uppercase;
  margin-bottom: 6px;
  font-family: 'JetBrains Mono', monospace;
}

.stat-card {
  background: linear-gradient(135deg, #0d0406, #060203);
  border: 1px solid #2a1015;
  border-radius: 12px;
  padding: 16px;
  text-align: center;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}
.stat-card:hover { border-color: #ff6b35; box-shadow: 0 0 20px rgba(255,107,53,0.1); transform: translateY(-2px); }

.gradient-text {
  background: linear-gradient(135deg, #ff6b35, #f7c948, #ff8c42);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.glow-border {
  border: 1px solid #ff6b3540;
  box-shadow: 0 0 20px rgba(255,107,53,0.1), inset 0 0 20px rgba(255,107,53,0.02);
}
</style>
""", unsafe_allow_html=True)


# ─── Provider Registry ────────────────────────────────────────────────────────
PROVIDERS = {
    "🔥 Groq (Free · Ultra-Fast)": {
        "id": "groq",
        "models": [
            "llama-3.3-70b-versatile",
            "llama-3.1-70b-versatile",
            "llama-3.1-8b-instant",
            "mixtral-8x7b-32768",
            "gemma2-9b-it",
            "deepseek-r1-distill-llama-70b",
        ],
        "default": "llama-3.3-70b-versatile",
        "key_env": "GROQ_API_KEY",
        "url": "https://api.groq.com/openai/v1/chat/completions",
        "openai_compat": True,
        "color": "#52b788",
        "icon": "🔥",
        "desc": "Fastest inference · Free tier · Open models",
    },
    "🔵 OpenAI (GPT)": {
        "id": "openai",
        "models": ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"],
        "default": "gpt-4o-mini",
        "key_env": "OPENAI_API_KEY",
        "url": "https://api.openai.com/v1/chat/completions",
        "openai_compat": True,
        "color": "#74c0fc",
        "icon": "🔵",
        "desc": "OpenAI GPT-4o family",
    },
    "🌟 Google Gemini": {
        "id": "gemini",
        "models": ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.0-flash-exp"],
        "default": "gemini-1.5-flash",
        "key_env": "GEMINI_API_KEY",
        "url": "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
        "openai_compat": False,
        "color": "#f7c948",
        "icon": "🌟",
        "desc": "Gemini 1.5 Flash (free) · Pro · 2.0 Exp",
    },
    "🌊 Mistral AI": {
        "id": "mistral",
        "models": ["mistral-small-latest", "mistral-medium-latest", "open-mistral-7b", "open-mixtral-8x7b"],
        "default": "mistral-small-latest",
        "key_env": "MISTRAL_API_KEY",
        "url": "https://api.mistral.ai/v1/chat/completions",
        "openai_compat": True,
        "color": "#ff8c42",
        "icon": "🌊",
        "desc": "Mistral AI models",
    },
    "💠 Cohere": {
        "id": "cohere",
        "models": ["command-r-plus", "command-r", "command"],
        "default": "command-r-plus",
        "key_env": "COHERE_API_KEY",
        "url": "https://api.cohere.ai/v1/chat",
        "openai_compat": False,
        "color": "#e879f9",
        "icon": "💠",
        "desc": "Cohere Command-R+ models",
    },
    "🔮 Anthropic Claude": {
        "id": "anthropic",
        "models": [
            "claude-sonnet-4-20250514",
            "claude-3-5-haiku-20241022",
            "claude-opus-4-5",
        ],
        "default": "claude-sonnet-4-20250514",
        "key_env": "ANTHROPIC_API_KEY",
        "url": "https://api.anthropic.com/v1/messages",
        "openai_compat": False,
        "color": "#c084fc",
        "icon": "🔮",
        "desc": "Anthropic Claude Sonnet 4 · Haiku · Opus",
    },
}

PERSONAS = {
    "🔥 Phoenix":           "You are Phoenix, a wise and powerful AI born from fire and knowledge. Be insightful, vivid, and transformative in your answers.",
    "🧠 NeuralChat Pro":    "You are NeuralChat Pro, a cutting-edge AI assistant with expertise across all domains. Be insightful, structured, and technically precise.",
    "🔬 Research Scientist":"You are a rigorous research scientist. Provide evidence-based, methodological answers with citations when possible. Use precise scientific language.",
    "💻 Code Architect":    "You are an expert software architect and senior developer. Provide clean, efficient, well-commented code with best practices. Explain every architectural decision.",
    "✍️ Creative Writer":   "You are a talented creative writer with a rich vocabulary and narrative skill. Be expressive, vivid, and imaginative.",
    "📊 Data Analyst":      "You are a data analyst. Provide analytical, data-driven insights. Use structured breakdowns and quantitative reasoning.",
    "🎓 Socratic Tutor":    "You are a Socratic tutor. Guide learning through thoughtful questions and gentle explanations. Break complex topics into digestible steps.",
    "🔐 Security Expert":   "You are a cybersecurity expert. Identify vulnerabilities, recommend best practices, and be thorough about risks.",
    "🌍 Multilingual Guide": "You are a multilingual communication expert. Help with translations, cultural context, and language nuances across multiple languages.",
    "🧮 Math Wizard":       "You are a brilliant mathematician. Solve problems step by step, explain concepts clearly, and use precise mathematical notation.",
    "🏥 Health Advisor":    "You are a knowledgeable health and wellness advisor. Provide evidence-based health information clearly (always remind users to consult a doctor for medical advice).",
    "📈 Business Strategist": "You are a senior business strategist with MBA-level knowledge. Provide frameworks, strategic analysis, and actionable recommendations.",
}

PROMPT_LIBRARY = {
    "💻 Code": [
        "Write a Python async REST API with FastAPI and SQLite",
        "Explain the SOLID principles with Python examples",
        "Build a recursive binary search tree in Python",
        "Write a Rust CLI tool with clap argument parsing",
        "Create a React hook for debounced search",
        "Explain async/await and the event loop in JavaScript",
        "Build a Python websocket server with asyncio",
        "Write a Docker Compose setup for a full-stack app",
    ],
    "🧠 AI/ML": [
        "Explain how transformer attention mechanisms work",
        "What's the difference between RAG and fine-tuning?",
        "Explain backpropagation step by step with math",
        "How does RLHF train language models?",
        "Compare LLaMA, Mistral and GPT architectures",
        "Explain vector embeddings and cosine similarity",
        "What is mixture of experts (MoE) architecture?",
    ],
    "🔐 Security": [
        "Explain SQL injection and how to prevent it",
        "How does OAuth 2.0 + PKCE work?",
        "What is a buffer overflow attack?",
        "Explain OWASP Top 10 vulnerabilities",
        "How does certificate pinning work?",
        "Explain zero-trust security architecture",
    ],
    "✍️ Creative": [
        "Write a cyberpunk short story set in 2087",
        "Create a fantasy world with unique magic system",
        "Write a noir detective scene with rich atmosphere",
        "Compose a haiku sequence about artificial minds",
        "Write a dystopian opening chapter",
        "Create a mythological origin story for fire",
    ],
    "📊 Data": [
        "Explain the CAP theorem with real examples",
        "What are the best data structures for LRU cache?",
        "Compare SQL vs NoSQL for different use cases",
        "How does consistent hashing work in distributed systems?",
        "Explain Apache Kafka architecture and use cases",
        "What is data lakehouse vs data warehouse?",
    ],
    "🌍 General Knowledge": [
        "Explain quantum entanglement in simple terms",
        "What caused the 2008 financial crisis?",
        "Explain how black holes form and evaporate",
        "What is the Fermi paradox?",
        "How does CRISPR gene editing work?",
        "Explain the history and impact of the internet",
    ],
    "📈 Business": [
        "Explain the Blue Ocean Strategy framework",
        "How to build a go-to-market strategy for a SaaS?",
        "What is the difference between B2B and B2C sales?",
        "Explain OKRs with practical examples",
        "How to conduct a SWOT analysis properly?",
    ],
    "🧮 Math": [
        "Explain Euler's identity and its significance",
        "What is the Monty Hall problem and why?",
        "Explain Bayesian probability with examples",
        "What is P vs NP and why does it matter?",
        "Explain Fourier transforms intuitively",
    ],
}

# ─── Flashcard Templates ──────────────────────────────────────────────────────
FLASHCARD_TOPICS = {
    "Python": ["List comprehensions", "Decorators", "Generators", "Context managers", "Async/Await", "Metaclasses"],
    "JavaScript": ["Closures", "Promises", "Event Loop", "Prototypes", "Module System", "WeakMap/WeakSet"],
    "ML Concepts": ["Gradient Descent", "Overfitting", "Cross-validation", "Embeddings", "Attention", "Backprop"],
    "System Design": ["Load balancing", "Caching strategies", "Database sharding", "Message queues", "CAP theorem", "Microservices"],
    "Security": ["XSS attacks", "CSRF tokens", "SQL injection", "JWT tokens", "Hash functions", "TLS handshake"],
}

# ─── AI API Caller ────────────────────────────────────────────────────────────
def call_ai(provider_name, model, messages, system_prompt, temperature, max_tokens, api_key):
    p = PROVIDERS[provider_name]
    pid = p["id"]
    headers = {"Content-Type": "application/json"}

    if p["openai_compat"]:
        headers["Authorization"] = f"Bearer {api_key}"
        payload = {
            "model": model,
            "messages": [{"role": "system", "content": system_prompt}] + messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        resp = requests.post(p["url"], headers=headers, json=payload, timeout=60)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]

    elif pid == "gemini":
        url = p["url"].replace("{model}", model) + f"?key={api_key}"
        contents = []
        for m in messages:
            role = "user" if m["role"] == "user" else "model"
            contents.append({"role": role, "parts": [{"text": m["content"]}]})
        payload = {
            "contents": contents,
            "generationConfig": {"temperature": temperature, "maxOutputTokens": max_tokens},
        }
        if system_prompt and system_prompt.strip():
            payload["systemInstruction"] = {"parts": [{"text": system_prompt}]}
        resp = requests.post(url, headers=headers, json=payload, timeout=60)
        if not resp.ok:
            err_msg = resp.json().get("error", {}).get("message", resp.text)
            raise ValueError(f"Gemini API error {resp.status_code}: {err_msg}")
        data = resp.json()
        candidates = data.get("candidates", [])
        if not candidates:
            raise ValueError(f"Gemini returned no candidates. Response: {data}")
        return candidates[0]["content"]["parts"][0]["text"]

    elif pid == "cohere":
        headers["Authorization"] = f"Bearer {api_key}"
        chat_history = []
        for m in messages[:-1]:
            chat_history.append({"role": "USER" if m["role"] == "user" else "CHATBOT", "message": m["content"]})
        last_user = messages[-1]["content"] if messages else ""
        payload = {
            "model": model, "message": last_user,
            "chat_history": chat_history,
            "preamble": system_prompt,
            "temperature": temperature, "max_tokens": max_tokens,
        }
        resp = requests.post(p["url"], headers=headers, json=payload, timeout=60)
        resp.raise_for_status()
        return resp.json()["text"]

    elif pid == "anthropic":
        headers["x-api-key"] = api_key
        headers["anthropic-version"] = "2023-06-01"
        payload = {
            "model": model, "max_tokens": max_tokens,
            "system": system_prompt, "messages": messages,
        }
        resp = requests.post(p["url"], headers=headers, json=payload, timeout=60)
        resp.raise_for_status()
        return resp.json()["content"][0]["text"]

    raise ValueError(f"Unknown provider: {pid}")


# ─── NLP Helpers ─────────────────────────────────────────────────────────────
def sentiment_score(text):
    pos = {'good','great','love','excellent','amazing','wonderful','fantastic','helpful','perfect',
           'awesome','brilliant','happy','thanks','thank','incredible','superb','beautiful','clear',
           'nice','interesting','useful','smart','fast','easy','works','insightful','detailed','correct',
           'right','true','valid','solid','elegant','clean','efficient','brilliant','creative'}
    neg = {'bad','hate','terrible','awful','horrible','worst','stupid','useless','wrong','error',
           'fail','poor','not','never','no','broken','ugly','slow','crash','confused','confusing',
           'unclear','impossible','cannot','dont','doesnt','incorrect','misleading','vague','missing'}
    words = set(text.lower().split())
    p = len(words & pos); n = len(words & neg)
    if p > n:   return "positive", min(1.0, 0.5 + p * 0.1)
    if n > p:   return "negative", min(1.0, 0.5 + n * 0.1)
    return "neutral", 0.5

def detect_intent(text):
    t = text.lower()
    intents = {
        "Question":     ["what","who","when","where","why","how","which","?"],
        "Code Request": ["code","write","implement","function","class","debug","fix","python","javascript","script","program","build","api"],
        "Creative":     ["story","poem","write","create","imagine","generate","design","compose","fiction","narrative"],
        "Analysis":     ["analyze","compare","explain","summarize","review","evaluate","assess","difference","vs","contrast"],
        "Greeting":     ["hi","hello","hey","good morning","good evening","howdy"],
        "Math":         ["calculate","solve","equation","math","number","compute","integral","derivative","proof"],
        "Security":     ["hack","vulnerability","exploit","secure","attack","injection","xss","csrf","pentest"],
        "Translation":  ["translate","in french","in spanish","in hindi","language","multilingual"],
        "Summary":      ["summarize","tldr","brief","overview","summary","recap","short"],
    }
    scores = {k: sum(1 for kw in v if kw in t) for k, v in intents.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "General"

def extract_keywords(text, top_n=8):
    stop = {'the','a','an','is','are','was','were','be','been','have','has','had','do','does','did',
            'will','would','could','should','may','might','to','of','in','on','at','by','for','with',
            'about','as','it','its','this','that','and','or','but','if','so','i','you','he','she','we',
            'they','my','your','his','her','our','their','what','how','when','where','why','who','which','not','can','just','like','use'}
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    return Counter(w for w in words if w not in stop).most_common(top_n)

def count_tokens_approx(text):
    return max(1, len(text) // 4)

def readability_score(text):
    words = text.split()
    sentences = len(re.split(r'[.!?]+', text)) or 1
    avg_wl = sum(len(w) for w in words) / max(1, len(words))
    words_per_sent = len(words) / sentences
    if avg_wl < 4 and words_per_sent < 12: return "Very Easy"
    if avg_wl < 5 and words_per_sent < 18: return "Easy"
    if avg_wl < 5.5 and words_per_sent < 22: return "Medium"
    if avg_wl < 6.5: return "Complex"
    return "Very Complex"

def format_content(content):
    html = re.sub(
        r'```(\w+)?\n?([\s\S]*?)```',
        lambda m: (
            f'<pre style="background:#0d0406;border:1px solid #2a1015;border-left:3px solid #ff6b35;'
            f'border-radius:8px;padding:14px;overflow-x:auto;font-family:\'JetBrains Mono\',monospace;'
            f'font-size:0.78rem;color:#ffd6b3;margin:10px 0;line-height:1.6;">'
            f'<span style="font-size:0.64rem;color:#4a2a22;display:block;margin-bottom:6px;font-family:\'JetBrains Mono\',monospace;">'
            f'{(m.group(1) or "code").upper()}</span>{m.group(2)}</pre>'
        ),
        content
    )
    html = re.sub(r'`([^`]+)`',
        r'<code style="background:#1d0b0e;padding:2px 7px;border-radius:4px;'
        r'font-family:\'JetBrains Mono\',monospace;font-size:0.82em;color:#ff8c42;">\1</code>', html)
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong style="color:#fdf0e8;font-weight:700;">\1</strong>', html)
    html = re.sub(r'\*(.*?)\*', r'<em style="color:#c8917a;">\1</em>', html)
    html = re.sub(r'^### (.+)$', r'<div style="font-family:\'Cinzel\',serif;font-size:1rem;color:#f7c948;font-weight:600;margin:10px 0 4px;">\1</div>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<div style="font-family:\'Cinzel\',serif;font-size:1.1rem;color:#ff8c42;font-weight:700;margin:12px 0 5px;">\1</div>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.+)$', r'<div style="font-family:\'Cinzel\',serif;font-size:1.2rem;color:#ff6b35;font-weight:900;margin:14px 0 6px;">\1</div>', html, flags=re.MULTILINE)
    html = re.sub(r'^[-•] (.+)$', r'<div style="display:flex;gap:8px;margin:3px 0;"><span style="color:#ff6b35;min-width:12px;">▸</span><span>\1</span></div>', html, flags=re.MULTILINE)
    html = re.sub(r'^\d+\. (.+)$', r'<div style="display:flex;gap:8px;margin:3px 0;"><span style="color:#f7c948;min-width:12px;">◆</span><span>\1</span></div>', html, flags=re.MULTILINE)
    html = html.replace('\n', '<br>')
    return html

def render_header(active_provider, active_model):
    p = PROVIDERS.get(active_provider, {})
    color = p.get("color", "#ff6b35")
    msg_count = len(st.session_state.get("messages", []))
    session_id = st.session_state.get("session_id", "UNKNOWN")

    st.markdown(f"""
<div style="padding:18px 24px;margin-bottom:18px;border-radius:16px;
background:linear-gradient(135deg,#0d0406,#060203);border:1px solid #2a1015;
display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;">
  <div>
    <div style="font-family:'Cinzel',serif;font-size:28px;font-weight:900;letter-spacing:3px;color:#ff6b35;
      animation:flicker 4s ease-in-out infinite;">🔥 PHOENIX AI STUDIO v5</div>
    <div style="color:#c8917a;font-size:12px;font-family:'JetBrains Mono',monospace;margin-top:2px;">
      Multi-Provider · Real-Time Analytics · NLP Engine · Session #{session_id}
    </div>
  </div>
  <div style="display:flex;gap:10px;align-items:center;flex-wrap:wrap;">
    <div style="padding:6px 14px;border-radius:8px;border:1px solid {color}44;color:{color};
      font-size:0.72rem;font-family:'JetBrains Mono',monospace;background:{color}0a;">{active_model}</div>
    <div style="padding:6px 14px;border-radius:8px;border:1px solid #2a1015;color:#c8917a;
      font-size:0.72rem;font-family:'JetBrains Mono',monospace;background:#0d0406;">
      💬 {msg_count} msgs
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


def render_message_bubble(role, content, timestamp, analysis=None, msg_idx=None, starred=False):
    is_user = role == "user"
    icon = "👤" if is_user else "🔥"
    label = "You" if is_user else "Phoenix AI"
    border = "#ff8c42" if is_user else "#ff6b35"
    bg = ("linear-gradient(135deg,#1d0b0e 0%,#120608 100%)" if is_user else "linear-gradient(135deg,#0d0406 0%,#060203 100%)")
    align = "flex-end" if is_user else "flex-start"
    radius = "16px 4px 16px 16px" if is_user else "4px 16px 16px 16px"
    border_color = "#ff8c4222" if is_user else "#ff6b351a"
    html = format_content(content)

    sent_badge = ""
    if analysis and not is_user:
        s = analysis.get("sentiment", "neutral")
        sc = {"positive": "#52b788", "negative": "#e63946", "neutral": "#c8917a"}.get(s, "#c8917a")
        sent_badge = f'<span style="font-size:0.62rem;padding:2px 8px;border-radius:8px;background:{sc}18;color:{sc};border:1px solid {sc}33;">{s}</span>'

    st.markdown(f"""
<div style="display:flex;flex-direction:column;align-items:{align};margin:10px 0;width:100%;">
  <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;">
    <div style="width:30px;height:30px;border-radius:8px;background:linear-gradient(135deg,{border}22,{border}08);
      border:1px solid {border}44;display:flex;align-items:center;justify-content:center;">{icon}</div>
    <span style="color:#c8917a;font-family:'JetBrains Mono',monospace;font-size:0.75rem;">{label}</span>
    <span style="font-size:.7rem;color:#555;">{timestamp}</span>
    {sent_badge}
  </div>
  <div style="max-width:82%;padding:14px 18px;background:{bg};border:1px solid {border_color};
    border-radius:{radius};line-height:1.7;color:#e8d5c8;font-family:'Crimson Pro',serif;">
    {html}
  </div>
</div>
""", unsafe_allow_html=True)


# ─── Session Init ─────────────────────────────────────────────────────────────
for key, val in {
    "messages":       [],
    "analytics":      [],
    "total_tokens":   0,
    "starred_msgs":   set(),
    "session_title":  None,
    "compare_mode":   False,
    "session_id":     hashlib.md5(str(time.time()).encode()).hexdigest()[:8].upper(),
    "notes":          [],
    "benchmarks":     [],
    "favorites":      [],
    "flashcard_idx":  0,
    "quiz_score":     {"correct": 0, "total": 0},
    "daily_usage":    {},
    "word_freq_all":  {},
    "provider_usage": {},
    "session_start":  datetime.now().isoformat(),
    "mood_log":       [],
    "research_reports": [],
    "prompt_tab_result": None,
    "prompt_tab_query":  "",
    "_run_prompt_tab":   False,
    "flashcard_history": [],
    "flashcard_log":     [],
    "last_report":       None,
    "model_stats":       {},
}.items():
    if key not in st.session_state:
        st.session_state[key] = val


# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:1rem 0 1.2rem;">
        <div style="font-family:'Cinzel',serif;font-size:0.85rem;font-weight:900;
            background:linear-gradient(135deg,#ff6b35,#f7c948);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;
            background-clip:text;letter-spacing:3px;">⚙ CONTROL PANEL</div>
        <div style="width:60px;height:1px;background:linear-gradient(90deg,transparent,#ff6b35,transparent);
            margin:8px auto 0;"></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sb-label">🌐 AI PROVIDER</div>', unsafe_allow_html=True)
    provider = st.selectbox("", list(PROVIDERS.keys()), label_visibility="collapsed", key="provider_sel")
    pdata  = PROVIDERS[provider]
    pcolor = pdata["color"]
    st.markdown(f'<div style="font-size:0.68rem;color:{pcolor};margin:-2px 0 8px;padding:4px 10px;background:{pcolor}0d;border-radius:6px;border:1px solid {pcolor}22;font-family:\'JetBrains Mono\',monospace;">{pdata["desc"]}</div>', unsafe_allow_html=True)

    stored_key = st.session_state.get(f"api_key_{pdata['id']}", os.environ.get(pdata["key_env"], ""))
    api_key_input = st.text_input(
        f"🔑 {pdata['id'].upper()} API Key",
        value=stored_key, type="password",
        placeholder="Paste your API key…",
        key=f"key_input_{pdata['id']}"
    )
    if api_key_input:
        st.session_state[f"api_key_{pdata['id']}"] = api_key_input
        os.environ[pdata["key_env"]] = api_key_input

    active_api_key = st.session_state.get(f"api_key_{pdata['id']}", "")
    if active_api_key:
        st.markdown('<div style="font-size:0.68rem;color:#52b788;margin-bottom:4px;font-family:\'JetBrains Mono\',monospace;">✅ Key configured</div>', unsafe_allow_html=True)
    else:
        tip = "⚡ Free key: console.groq.com" if pdata["id"] == "groq" else "⚠ API key required"
        tip_color = "#f7c948" if pdata["id"] == "groq" else "#e63946"
        st.markdown(f'<div style="font-size:0.68rem;color:{tip_color};font-family:\'JetBrains Mono\',monospace;">{tip}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sb-label">🤖 MODEL</div>', unsafe_allow_html=True)
    model_sel = st.selectbox("", pdata["models"], index=0, label_visibility="collapsed", key="model_sel")

    st.markdown("<br>", unsafe_allow_html=True)
    compare_mode = st.toggle("⚡ Model Comparison Mode", value=st.session_state.compare_mode)
    st.session_state.compare_mode = compare_mode
    if compare_mode:
        st.markdown('<div class="sb-label" style="margin-top:6px;">🔀 COMPARE PROVIDER</div>', unsafe_allow_html=True)
        other_providers = [p for p in PROVIDERS if p != provider]
        provider_b = st.selectbox("", other_providers, label_visibility="collapsed", key="provider_b_sel")
        pdata_b = PROVIDERS[provider_b]
        model_sel_b = st.selectbox("", pdata_b["models"], index=0, label_visibility="collapsed", key="model_sel_b")
        api_key_b = st.session_state.get(f"api_key_{pdata_b['id']}", os.environ.get(pdata_b["key_env"], ""))
        st.markdown(f'<div style="font-size:0.68rem;color:{"#52b788" if api_key_b else "#e63946"};font-family:\'JetBrains Mono\',monospace;">{"✅ Key ok" if api_key_b else "⚠ Key needed"}</div>', unsafe_allow_html=True)

    st.divider()
    st.markdown('<div class="sb-label">🎭 PERSONA</div>', unsafe_allow_html=True)
    persona = st.selectbox("", list(PERSONAS.keys()), label_visibility="collapsed", key="persona_sel")
    use_custom_sys = st.toggle("✏️ Custom System Prompt", value=False, key="use_custom_sys")
    if use_custom_sys:
        custom_sys = st.text_area("", placeholder="Enter custom system prompt…", height=80,
                                   label_visibility="collapsed", key="custom_sys_input")
    else:
        custom_sys = ""

    st.divider()
    st.markdown('<div class="sb-label">🎛 GENERATION</div>', unsafe_allow_html=True)
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.05)
    max_tokens  = st.slider("Max Tokens", 256, 4096, 1500, 64)

    st.divider()
    st.markdown('<div class="sb-label">🧪 NLP FEATURES</div>', unsafe_allow_html=True)
    show_sentiment = st.toggle("Sentiment Analysis", value=True)
    show_intent    = st.toggle("Intent Detection",   value=True)
    show_tokens    = st.toggle("Token Counter",      value=True)
    show_timing    = st.toggle("Response Timing",    value=True)

    st.divider()
    st.markdown('<div class="sb-label">🔍 SEARCH HISTORY</div>', unsafe_allow_html=True)
    search_query = st.text_input("", placeholder="Search messages…", label_visibility="collapsed", key="search_hist")

    st.divider()
    st.markdown('<div class="sb-label">📁 HISTORY</div>', unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🗑 Clear", use_container_width=True):
            st.session_state.messages = []
            st.session_state.analytics = []
            st.session_state.total_tokens = 0
            st.session_state.starred_msgs = set()
            st.session_state.session_title = None
            st.rerun()
    with col_b:
        if st.button("📤 Export", use_container_width=True):
            if st.session_state.messages:
                export = json.dumps({
                    "session_id": st.session_state.session_id,
                    "title": st.session_state.session_title or "Phoenix Chat",
                    "provider": provider, "model": model_sel,
                    "persona": persona,
                    "exported_at": datetime.now().isoformat(),
                    "messages": st.session_state.messages,
                    "analytics": st.session_state.analytics,
                }, indent=2, default=str)
                st.download_button("💾 Download JSON", export,
                    file_name=f"phoenix_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                    mime="application/json", use_container_width=True)

    # Session stats
    st.divider()
    msg_count  = len(st.session_state.messages)
    user_count = sum(1 for m in st.session_state.messages if m["role"] == "user")
    total_char = sum(len(m["content"]) for m in st.session_state.messages)
    valid_a    = [a for a in st.session_state.analytics if a]
    avg_rt     = sum(a.get("response_time", 0) for a in valid_a) / max(1, len(valid_a))

    session_dur = (datetime.now() - datetime.fromisoformat(st.session_state.session_start)).seconds
    dur_str = f"{session_dur//60}m {session_dur%60}s"

    st.markdown(f"""
    <div style="background:#0d0406;border:1px solid #2a1015;border-radius:10px;
        padding:12px;font-size:0.74rem;color:#c8917a;font-family:'JetBrains Mono',monospace;">
        <div style="display:flex;justify-content:space-between;margin-bottom:5px;">
            <span style="color:#4a2a22;">SESSION</span>
            <span style="color:#ff6b35;font-weight:700;">{st.session_state.session_id}</span>
        </div>
        <div style="display:flex;justify-content:space-between;margin-bottom:5px;">
            <span>Exchanges</span><span style="color:#ff6b35;">{user_count}</span>
        </div>
        <div style="display:flex;justify-content:space-between;margin-bottom:5px;">
            <span>Est. Tokens</span><span style="color:#f7c948;">~{total_char//4:,}</span>
        </div>
        <div style="display:flex;justify-content:space-between;margin-bottom:5px;">
            <span>Avg RT</span><span style="color:#ff8c42;">{avg_rt:.1f}s</span>
        </div>
        <div style="display:flex;justify-content:space-between;margin-bottom:5px;">
            <span>Duration</span><span style="color:#c084fc;">{dur_str}</span>
        </div>
        <div style="display:flex;justify-content:space-between;">
            <span>Notes</span><span style="color:#67e8f9;">{len(st.session_state.notes)}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─── Main Layout ──────────────────────────────────────────────────────────────
render_header(provider, model_sel)

tabs = st.tabs([
    "🔥 Chat",
    "💡 Prompts",
    "📊 Analytics",
    "🔬 NLP Lab",
    "📈 Deep Stats",
    "🗒️ Notes",
    "⚡ Benchmark",
    "🎯 Flashcards",
    "🌡️ Session Health",
    "🆚 Model Comparisons",
    "🛠 Settings",
])
tab_chat, tab_prompts, tab_analytics, tab_nlp, tab_deepstats, tab_notes, tab_bench, tab_flash, tab_health, tab_modelcomp, tab_settings = tabs


# ══════════════════════════════════════════════════════════════════
# TAB 1: CHAT
# ══════════════════════════════════════════════════════════════════
with tab_chat:
    if not st.session_state.messages:
        st.markdown(f"""
        <div class="msg-animate" style="text-align:center;padding:2rem 0 1.2rem;">
            <div style="font-family:'Cinzel',serif;font-size:2.4rem;font-weight:900;
                background:linear-gradient(135deg,#ff6b35,#f7c948,#ff8c42);
                -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                background-clip:text;margin-bottom:10px;letter-spacing:3px;
                animation:flicker 4s ease-in-out infinite;">
                RISE & ASK
            </div>
            <div style="color:#4a2a22;font-size:0.75rem;font-family:'JetBrains Mono',monospace;
                letter-spacing:3px;">POWERED BY {model_sel.upper()} · PHOENIX AI v5 · NLP ENGINE</div>
        </div>
        """, unsafe_allow_html=True)

    ALL_SUGGESTIONS = [
        ("🐍", "Python",      "Write a Python async REST API with FastAPI and SQLite"),
        ("🔥", "Transformers","Explain how transformer attention mechanisms work"),
        ("⚡", "Compare AI",  "Compare LLaMA 3, GPT-4o and Claude 3.5 architectures"),
        ("💻", "React",       "Create a React custom hook for debounced search input"),
        ("🐳", "Docker",      "Write a Docker Compose setup for a full-stack web app"),
        ("🦀", "Rust",        "Write a Rust CLI tool with clap argument parsing"),
        ("🧠", "RAG vs FT",   "What's the difference between RAG and fine-tuning?"),
        ("📉", "Backprop",    "Explain backpropagation step by step with math"),
        ("🤖", "RLHF",        "How does RLHF train language models?"),
        ("🌀", "MoE",         "What is mixture of experts (MoE) architecture?"),
        ("📐", "Embeddings",  "Explain vector embeddings and cosine similarity"),
        ("🔮", "Diffusion",   "How do diffusion models generate images?"),
        ("🔐", "SQL Inject",  "Explain SQL injection and how to prevent it"),
        ("🔑", "OAuth",       "How does OAuth 2.0 + PKCE work step by step?"),
        ("🛡️", "OWASP",       "Explain OWASP Top 10 vulnerabilities with examples"),
        ("🔒", "Zero Trust",  "Explain zero-trust security architecture"),
        ("💀", "Buffer Overflow","What is a buffer overflow attack and how to exploit it?"),
        ("🧩", "JWT",         "How do JWT tokens work and what are their risks?"),
        ("🌑", "Cyberpunk",   "Write a cyberpunk noir short story set in 2087"),
        ("🧙", "Fantasy",     "Create a fantasy world with a unique magic system"),
        ("🕵️", "Detective",   "Write a gripping noir detective scene"),
        ("🌌", "Sci-Fi",      "Write a hard sci-fi story about first contact"),
        ("🔥", "Fire Origin",  "Create a mythological origin story for fire"),
        ("🤖", "AI Poem",     "Compose a haiku sequence about artificial minds"),
        ("📦", "CAP Theorem", "Explain the CAP theorem with real-world examples"),
        ("🗃️", "LRU Cache",   "Best data structures for an LRU cache?"),
        ("🔀", "Hashing",     "How does consistent hashing work in distributed systems?"),
        ("📨", "Kafka",       "Explain Apache Kafka architecture and use cases"),
        ("🌊", "SQL vs NoSQL","Compare SQL vs NoSQL for different use cases"),
        ("🏗️", "Microservices","Microservices vs monolith — when to use each?"),
        ("⚛️", "Quantum",     "Explain quantum entanglement in simple terms"),
        ("🕳️", "Black Holes", "How do black holes form and evaporate?"),
        ("🧬", "CRISPR",      "How does CRISPR gene editing work?"),
        ("🌍", "Climate",     "What are the main drivers of climate change?"),
        ("💰", "2008 Crisis", "What caused the 2008 global financial crisis?"),
        ("🧮", "Euler",       "Explain Euler's identity and its deep significance"),
    ]

    SUGG_CATEGORIES = {
        "💻 Code":    ALL_SUGGESTIONS[0:6],
        "🧠 AI/ML":   ALL_SUGGESTIONS[6:12],
        "🔐 Security":ALL_SUGGESTIONS[12:18],
        "✍️ Creative":ALL_SUGGESTIONS[18:24],
        "📊 Data":    ALL_SUGGESTIONS[24:30],
        "🌍 Science": ALL_SUGGESTIONS[30:36],
    }

    st.markdown('<div style="font-size:0.62rem;color:#4a2a22;font-family:\'JetBrains Mono\',monospace;letter-spacing:2px;margin-bottom:6px;">⚡ QUICK QUESTIONS — click any to ask instantly</div>', unsafe_allow_html=True)

    sugg_cat = st.radio("", list(SUGG_CATEGORIES.keys()), horizontal=True,
                        key="sugg_cat_radio", label_visibility="collapsed")

    active_suggestions = SUGG_CATEGORIES[sugg_cat]

    for row_start in range(0, 6, 3):
        row_cols = st.columns(3)
        for col_idx, (icon, label, prompt) in enumerate(active_suggestions[row_start:row_start+3]):
            with row_cols[col_idx]:
                if st.button(prompt[:55] + ("…" if len(prompt)>55 else ""),
                             use_container_width=True,
                             key=f"qs_{sugg_cat}_{row_start}_{col_idx}",
                             help=prompt):
                    st.session_state._pending_prompt = prompt
                    st.rerun()

    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
    st.divider()

    search_active = search_query and search_query.strip()
    if search_active:
        sq = search_query.lower()
        filtered_msgs = [(i, m) for i, m in enumerate(st.session_state.messages) if sq in m["content"].lower()]
        if filtered_msgs:
            st.markdown(f'<div style="font-size:0.72rem;color:#ff6b35;font-family:\'JetBrains Mono\',monospace;margin-bottom:8px;">🔍 {len(filtered_msgs)} results for &quot;{search_query}&quot;</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="font-size:0.72rem;color:#e63946;font-family:\'JetBrains Mono\',monospace;margin-bottom:8px;">No results for &quot;{search_query}&quot;</div>', unsafe_allow_html=True)
        for i, msg in filtered_msgs:
            analysis = st.session_state.analytics[i] if i < len(st.session_state.analytics) else None
            render_message_bubble(msg["role"], msg["content"], msg.get("timestamp",""), analysis, i)
    else:
        for i, msg in enumerate(st.session_state.messages):
            analysis = st.session_state.analytics[i] if i < len(st.session_state.analytics) else None
            render_message_bubble(msg["role"], msg["content"], msg.get("timestamp",""), analysis, i)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    if show_tokens and st.session_state.messages:
        ctx = sum(len(m["content"]) // 4 for m in st.session_state.messages[-16:])
        max_ctx = 8192
        pct = min(1.0, ctx / max_ctx)
        bc = "#52b788" if pct < 0.6 else "#f7c948" if pct < 0.85 else "#e63946"
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:10px;margin:4px 0 10px;">
            <span style="font-size:0.62rem;color:#4a2a22;font-family:'JetBrains Mono',monospace;white-space:nowrap;">CTX WINDOW</span>
            <div style="flex:1;height:3px;background:#1d0b0e;border-radius:2px;overflow:hidden;">
                <div style="width:{pct*100:.1f}%;height:100%;background:{bc};border-radius:2px;box-shadow:0 0 8px {bc};transition:width 0.5s ease;"></div>
            </div>
            <span style="font-size:0.62rem;color:{bc};font-family:'JetBrains Mono',monospace;white-space:nowrap;">{ctx:,}/{max_ctx:,}</span>
        </div>
        """, unsafe_allow_html=True)

    if compare_mode:
        st.markdown(f"""
        <div style="background:#ff6b3508;border:1px solid #ff6b3522;border-radius:8px;padding:8px 14px;
            font-size:0.72rem;color:#ff8c42;font-family:'JetBrains Mono',monospace;margin-bottom:8px;">
            ⚡ COMPARISON MODE: {model_sel} vs {model_sel_b}
        </div>
        """, unsafe_allow_html=True)

    pending    = st.session_state.pop("_pending_prompt", None)
    user_input = st.chat_input("Message Phoenix AI…", key="chat_input")
    if pending and not user_input:
        user_input = pending

    if user_input and user_input.strip():
        if not active_api_key:
            st.error("⚠ No API key configured. Please add your key in the sidebar.")
            st.stop()

        user_text = user_input.strip()
        timestamp = datetime.now().strftime("%H:%M")

        if not st.session_state.session_title and len(user_text) > 3:
            st.session_state.session_title = user_text[:50] + ("…" if len(user_text) > 50 else "")

        pid = pdata["id"]
        st.session_state.provider_usage[pid] = st.session_state.provider_usage.get(pid, 0) + 1

        today = datetime.now().strftime("%Y-%m-%d")
        st.session_state.daily_usage[today] = st.session_state.daily_usage.get(today, 0) + 1

        st.session_state.messages.append({"role": "user", "content": user_text, "timestamp": timestamp})
        st.session_state.analytics.append(None)
        render_message_bubble("user", user_text, timestamp)

        api_messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-20:]]
        system_prompt = custom_sys if use_custom_sys and custom_sys.strip() else PERSONAS.get(persona, PERSONAS["🔥 Phoenix"])
        system_prompt += "\n\nRespond in a clear, well-structured way. Use markdown formatting when helpful."

        def typing_indicator(label=""):
            return f"""
            <div class="msg-animate" style="display:flex;align-items:center;gap:10px;padding:10px 0;margin-left:4px;">
                <div style="width:30px;height:30px;border-radius:8px;
                    background:linear-gradient(135deg,#ff6b3522,#ff6b3508);
                    border:1px solid #ff6b3540;
                    display:flex;align-items:center;justify-content:center;font-size:14px;
                    animation:emberGlow 1.5s ease-in-out infinite;">🔥</div>
                <div style="display:flex;gap:5px;align-items:center;">
                    <div style="width:7px;height:7px;border-radius:50%;background:#ff6b35;animation:bounce 1.2s infinite 0s;"></div>
                    <div style="width:7px;height:7px;border-radius:50%;background:#f7c948;animation:bounce 1.2s infinite 0.2s;"></div>
                    <div style="width:7px;height:7px;border-radius:50%;background:#ff8c42;animation:bounce 1.2s infinite 0.4s;"></div>
                </div>
                <span style="font-size:0.7rem;color:#4a2a22;font-family:'JetBrains Mono',monospace;">
                    {label or model_sel} igniting…
                </span>
            </div>
            """

        if compare_mode:
            col_left, col_right = st.columns(2)
            with col_left:
                ph_a = st.empty()
                ph_a.markdown(typing_indicator(model_sel), unsafe_allow_html=True)
            with col_right:
                ph_b = st.empty()
                ph_b.markdown(typing_indicator(model_sel_b), unsafe_allow_html=True)

            try:
                t0 = time.time()
                resp_a = call_ai(provider, model_sel, api_messages, system_prompt, temperature, max_tokens, active_api_key)
                rt_a = round(time.time() - t0, 2)
                ph_a.empty()
            except Exception as e:
                ph_a.empty()
                resp_a = f"⚠ Error: {e}"
                rt_a = 0

            try:
                t0 = time.time()
                resp_b = call_ai(provider_b, model_sel_b, api_messages, system_prompt, temperature, max_tokens, api_key_b)
                rt_b = round(time.time() - t0, 2)
                ph_b.empty()
            except Exception as e:
                ph_b.empty()
                resp_b = f"⚠ Error: {e}"
                rt_b = 0

            with col_left:
                st.markdown(f'<div style="font-size:0.68rem;color:{pcolor};font-family:\'JetBrains Mono\',monospace;margin-bottom:4px;">{model_sel} · {rt_a:.1f}s · {len(resp_a)} chars</div>', unsafe_allow_html=True)
                st.markdown(f'<div style="background:#0d0406;border:1px solid #2a1015;border-left:3px solid {pcolor};border-radius:10px;padding:14px;font-size:0.95rem;color:#e8d5c8;line-height:1.75;font-family:\'Crimson Pro\',serif;">{format_content(resp_a)}</div>', unsafe_allow_html=True)
            with col_right:
                color_b = PROVIDERS[provider_b]["color"]
                st.markdown(f'<div style="font-size:0.68rem;color:{color_b};font-family:\'JetBrains Mono\',monospace;margin-bottom:4px;">{model_sel_b} · {rt_b:.1f}s · {len(resp_b)} chars</div>', unsafe_allow_html=True)
                st.markdown(f'<div style="background:#0d0406;border:1px solid #2a1015;border-left:3px solid {color_b};border-radius:10px;padding:14px;font-size:0.95rem;color:#e8d5c8;line-height:1.75;font-family:\'Crimson Pro\',serif;">{format_content(resp_b)}</div>', unsafe_allow_html=True)

            ai_ts = datetime.now().strftime("%H:%M")
            tokens = count_tokens_approx(resp_a)
            sent, sent_score = sentiment_score(resp_a)
            analysis = {"sentiment": sent, "sentiment_score": sent_score, "intent": detect_intent(user_text),
                        "keywords": extract_keywords(user_text + " " + resp_a), "tokens": tokens,
                        "response_time": rt_a, "chars_per_sec": round(len(resp_a) / max(0.01, rt_a), 1), "thinking": ""}
            st.session_state.messages.append({"role": "assistant", "content": f"**{model_sel}:** {resp_a}", "timestamp": ai_ts})
            st.session_state.analytics.append(analysis)
            st.session_state.total_tokens += tokens

            # Track both models in compare mode
            for (prov_name, mod_name, resp_text, rt_val) in [
                (provider, model_sel, resp_a, rt_a),
                (provider_b, model_sel_b, resp_b, rt_b),
            ]:
                pd_tmp = PROVIDERS[prov_name]
                mkey = f"{pd_tmp['id']}::{mod_name}"
                if mkey not in st.session_state.model_stats:
                    st.session_state.model_stats[mkey] = {
                        "provider": pd_tmp["id"], "model": mod_name,
                        "provider_label": prov_name.split("(")[0].strip(),
                        "color": pd_tmp["color"],
                        "calls": 0, "total_tokens": 0, "total_rt": 0.0,
                        "total_chars": 0, "sentiments": [],
                        "response_times": [], "token_list": [],
                    }
                ms = st.session_state.model_stats[mkey]
                toks_tmp = count_tokens_approx(resp_text)
                ms["calls"]        += 1
                ms["total_tokens"] += toks_tmp
                ms["total_rt"]     += rt_val
                ms["total_chars"]  += len(resp_text)
                ms["sentiments"].append(sentiment_score(resp_text)[0])
                ms["response_times"].append(rt_val)
                ms["token_list"].append(toks_tmp)

        else:
            typing_ph = st.empty()
            typing_ph.markdown(typing_indicator(), unsafe_allow_html=True)
            try:
                t_start = time.time()
                full_response = call_ai(provider_name=provider, model=model_sel,
                    messages=api_messages, system_prompt=system_prompt,
                    temperature=temperature, max_tokens=max_tokens, api_key=active_api_key)
                rt = round(time.time() - t_start, 2)
                typing_ph.empty()

                sent, sent_score = sentiment_score(full_response)
                intent   = detect_intent(user_text)
                keywords = extract_keywords(user_text + " " + full_response)
                tokens   = count_tokens_approx(full_response)
                cps      = round(len(full_response) / max(0.01, rt), 1)
                read     = readability_score(full_response)

                analysis = {"sentiment": sent, "sentiment_score": sent_score, "intent": intent,
                            "keywords": keywords, "tokens": tokens, "response_time": rt,
                            "chars_per_sec": cps, "thinking": "", "readability": read,
                            "response_length": len(full_response)}

                for word, freq in keywords:
                    st.session_state.word_freq_all[word] = st.session_state.word_freq_all.get(word, 0) + freq

                st.session_state.mood_log.append({"time": datetime.now().strftime("%H:%M"), "sentiment": sent, "score": sent_score})

                mkey = f"{pdata['id']}::{model_sel}"
                if mkey not in st.session_state.model_stats:
                    st.session_state.model_stats[mkey] = {
                        "provider": pdata["id"], "model": model_sel,
                        "provider_label": provider.split("(")[0].strip(),
                        "color": pdata["color"],
                        "calls": 0, "total_tokens": 0, "total_rt": 0.0,
                        "total_chars": 0, "sentiments": [],
                        "response_times": [], "token_list": [],
                    }
                ms = st.session_state.model_stats[mkey]
                ms["calls"]        += 1
                ms["total_tokens"] += tokens
                ms["total_rt"]     += rt
                ms["total_chars"]  += len(full_response)
                ms["sentiments"].append(sent)
                ms["response_times"].append(rt)
                ms["token_list"].append(tokens)

                ai_ts = datetime.now().strftime("%H:%M")
                st.session_state.messages.append({"role": "assistant", "content": full_response, "timestamp": ai_ts})
                st.session_state.analytics.append(analysis)
                st.session_state.total_tokens += tokens

                render_message_bubble("assistant", full_response, ai_ts, analysis, len(st.session_state.messages) - 1)

                if any([show_sentiment, show_intent, show_tokens]):
                    sc = {"positive":"#52b788","negative":"#e63946","neutral":"#c8917a"}.get(sent,"#c8917a")
                    bdg = ""
                    if show_sentiment: bdg += f'<span style="font-size:0.66rem;padding:3px 10px;border-radius:8px;background:{sc}18;color:{sc};border:1px solid {sc}33;margin-right:6px;font-family:\'JetBrains Mono\',monospace;">❤ {sent} ({sent_score:.0%})</span>'
                    if show_intent:    bdg += f'<span style="font-size:0.66rem;padding:3px 10px;border-radius:8px;background:#ff8c4218;color:#ff8c42;border:1px solid #ff8c4233;margin-right:6px;font-family:\'JetBrains Mono\',monospace;">🎯 {intent}</span>'
                    if show_tokens:    bdg += f'<span style="font-size:0.66rem;padding:3px 10px;border-radius:8px;background:#f7c94818;color:#f7c948;border:1px solid #f7c94833;margin-right:6px;font-family:\'JetBrains Mono\',monospace;">⚡ ~{tokens} tok</span>'
                    if show_timing:    bdg += f'<span style="font-size:0.66rem;padding:3px 10px;border-radius:8px;background:#ff6b3510;color:#ff6b35;border:1px solid #ff6b3522;margin-right:6px;font-family:\'JetBrains Mono\',monospace;">⏱ {rt:.1f}s · {cps:.0f} c/s</span>'
                    bdg += f'<span style="font-size:0.66rem;padding:3px 10px;border-radius:8px;background:#c084fc18;color:#c084fc;border:1px solid #c084fc33;font-family:\'JetBrains Mono\',monospace;">📖 {read}</span>'
                    st.markdown(f'<div style="margin:4px 0 8px 42px;">{bdg}</div>', unsafe_allow_html=True)

            except requests.exceptions.HTTPError as e:
                typing_ph.empty()
                code = e.response.status_code if e.response else "?"
                try: msg = e.response.json().get("error", {}).get("message", str(e))
                except: msg = str(e)
                st.markdown(f'<div style="background:#120407;border:1px solid #7f1d1d;border-left:3px solid #e63946;border-radius:10px;padding:14px 18px;color:#e63946;font-size:0.88rem;margin:8px 0;font-family:\'JetBrains Mono\',monospace;">⚠ HTTP {code} · {msg}</div>', unsafe_allow_html=True)
                if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
                    st.session_state.messages.pop(); st.session_state.analytics.pop()
            except Exception as e:
                typing_ph.empty()
                st.markdown(f'<div style="background:#120407;border:1px solid #7f1d1d;border-left:3px solid #e63946;border-radius:10px;padding:14px 18px;color:#e63946;font-size:0.88rem;margin:8px 0;font-family:\'JetBrains Mono\',monospace;">⚠ Error · {str(e)}</div>', unsafe_allow_html=True)
                if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
                    st.session_state.messages.pop(); st.session_state.analytics.pop()


# ══════════════════════════════════════════════════════════════════
# TAB 2: PROMPT LIBRARY
# ══════════════════════════════════════════════════════════════════
with tab_prompts:
    st.markdown('<div style="font-family:\'Cinzel\',serif;font-size:1rem;font-weight:700;background:linear-gradient(135deg,#ff6b35,#f7c948);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;letter-spacing:2px;margin-bottom:0.5rem;">💡 PROMPT LIBRARY</div>', unsafe_allow_html=True)

    if "prompt_tab_result" not in st.session_state:
        st.session_state.prompt_tab_result = None
    if "prompt_tab_query" not in st.session_state:
        st.session_state.prompt_tab_query = ""

    prompt_mode = st.radio(
        "Where to send response:",
        ["💬 Chat Only", "📄 Show Here (Prompts Tab)", "📄+💬 Both"],
        horizontal=True, key="prompt_mode_radio",
        label_visibility="visible",
    )

    st.markdown("<br>", unsafe_allow_html=True)

    col_lib, col_resp = st.columns([1, 1])

    with col_lib:
        prompt_search = st.text_input("🔍 Search prompts", placeholder="Search library…", key="prompt_search")

        all_prompts_flat = [(cat, p) for cat, prompts in PROMPT_LIBRARY.items() for p in prompts]
        if prompt_search:
            filtered = [(cat, p) for cat, p in all_prompts_flat if prompt_search.lower() in p.lower()]
            st.markdown(f'<div style="font-size:0.72rem;color:#ff6b35;font-family:\'JetBrains Mono\',monospace;margin-bottom:8px;">{len(filtered)} prompts found</div>', unsafe_allow_html=True)
            for cat, prompt in filtered:
                col_p, col_b = st.columns([4, 1])
                with col_p:
                    st.markdown(f'<div style="padding:5px 0;color:#e8d5c8;font-family:\'Crimson Pro\',serif;font-size:0.9rem;"><span style="font-size:0.65rem;color:#4a2a22;">{cat}</span><br>{prompt}</div>', unsafe_allow_html=True)
                with col_b:
                    if st.button("▶", key=f"search_lib_{hash(prompt)}", use_container_width=True, help="Run this prompt"):
                        if prompt_mode == "💬 Chat Only":
                            st.session_state._pending_prompt = prompt
                            st.rerun()
                        else:
                            st.session_state.prompt_tab_query = prompt
                            st.session_state.prompt_tab_result = None
                            st.session_state._run_prompt_tab = True
                            if prompt_mode == "📄+💬 Both":
                                st.session_state._pending_prompt = prompt
        else:
            for category, prompts in PROMPT_LIBRARY.items():
                with st.expander(category, expanded=False):
                    for prompt in prompts:
                        col_p, col_b = st.columns([4, 1])
                        with col_p:
                            st.markdown(f'<div style="padding:5px 0;color:#e8d5c8;font-family:\'Crimson Pro\',serif;font-size:0.9rem;">{prompt}</div>', unsafe_allow_html=True)
                        with col_b:
                            if st.button("▶", key=f"lib_{hash(prompt)}", use_container_width=True):
                                if prompt_mode == "💬 Chat Only":
                                    st.session_state._pending_prompt = prompt
                                    st.rerun()
                                else:
                                    st.session_state.prompt_tab_query = prompt
                                    st.session_state.prompt_tab_result = None
                                    st.session_state._run_prompt_tab = True
                                    if prompt_mode == "📄+💬 Both":
                                        st.session_state._pending_prompt = prompt

        st.divider()

        st.markdown('<div style="font-size:0.76rem;color:#f7c948;margin-bottom:8px;font-family:\'JetBrains Mono\',monospace;">⭐ FAVORITES</div>', unsafe_allow_html=True)
        if st.session_state.favorites:
            for i, fav in enumerate(st.session_state.favorites):
                col_f, col_fb, col_fd = st.columns([3, 1, 1])
                with col_f:
                    st.markdown(f'<div style="padding:5px 0;color:#e8d5c8;font-size:0.85rem;font-family:\'Crimson Pro\',serif;">{fav[:60]}{"…" if len(fav)>60 else ""}</div>', unsafe_allow_html=True)
                with col_fb:
                    if st.button("▶", key=f"fav_use_{i}", use_container_width=True):
                        if prompt_mode == "💬 Chat Only":
                            st.session_state._pending_prompt = fav
                            st.rerun()
                        else:
                            st.session_state.prompt_tab_query = fav
                            st.session_state.prompt_tab_result = None
                            st.session_state._run_prompt_tab = True
                            if prompt_mode == "📄+💬 Both":
                                st.session_state._pending_prompt = fav
                with col_fd:
                    if st.button("🗑", key=f"fav_del_{i}", use_container_width=True):
                        st.session_state.favorites.pop(i)
                        st.rerun()
        else:
            st.markdown('<div style="color:#4a2a22;font-size:0.8rem;font-family:\'JetBrains Mono\',monospace;">No favorites yet</div>', unsafe_allow_html=True)

        st.divider()
        st.markdown('<div style="font-size:0.8rem;color:#4a2a22;font-family:\'JetBrains Mono\',monospace;margin-bottom:8px;">✏️ CUSTOM PROMPT</div>', unsafe_allow_html=True)
        custom_prompt = st.text_area("", placeholder="Type your own prompt…", height=80, label_visibility="collapsed", key="custom_prompt_input")
        col_cp1, col_cp2 = st.columns(2)
        with col_cp1:
            if st.button("🔥 Run Prompt", use_container_width=True):
                if custom_prompt.strip():
                    if prompt_mode == "💬 Chat Only":
                        st.session_state._pending_prompt = custom_prompt.strip()
                        st.rerun()
                    else:
                        st.session_state.prompt_tab_query = custom_prompt.strip()
                        st.session_state.prompt_tab_result = None
                        st.session_state._run_prompt_tab = True
                        if prompt_mode == "📄+💬 Both":
                            st.session_state._pending_prompt = custom_prompt.strip()
        with col_cp2:
            if st.button("⭐ Save to Favorites", use_container_width=True):
                if custom_prompt.strip() and custom_prompt.strip() not in st.session_state.favorites:
                    st.session_state.favorites.append(custom_prompt.strip())
                    st.success("Added to favorites!")
                    st.rerun()

    with col_resp:
        st.markdown('<div style="font-size:0.76rem;color:#c8917a;margin-bottom:8px;font-family:\'JetBrains Mono\',monospace;">📄 INLINE RESPONSE</div>', unsafe_allow_html=True)

        if st.session_state.get("_run_prompt_tab") and st.session_state.prompt_tab_query:
            st.session_state._run_prompt_tab = False
            if not active_api_key:
                st.error("⚠ No API key configured.")
            else:
                run_query = st.session_state.prompt_tab_query
                system_prompt_pt = PERSONAS.get(persona, PERSONAS["🔥 Phoenix"])
                system_prompt_pt += "\n\nRespond in a clear, well-structured way. Use markdown formatting when helpful."
                with st.spinner(f"🔥 Generating response…"):
                    try:
                        t0 = time.time()
                        pt_response = call_ai(
                            provider, model_sel,
                            [{"role":"user","content":run_query}],
                            system_prompt_pt,
                            temperature, max_tokens, active_api_key
                        )
                        pt_rt = round(time.time() - t0, 2)
                        pt_tokens = count_tokens_approx(pt_response)
                        st.session_state.prompt_tab_result = {
                            "query": run_query, "response": pt_response,
                            "rt": pt_rt, "tokens": pt_tokens,
                            "model": model_sel,
                        }
                    except Exception as e:
                        st.session_state.prompt_tab_result = {"error": str(e)}

        if st.session_state.prompt_tab_result:
            res = st.session_state.prompt_tab_result
            if "error" in res:
                st.markdown(f'<div style="background:#120407;border:1px solid #7f1d1d;border-left:3px solid #e63946;border-radius:10px;padding:14px;color:#e63946;font-size:0.82rem;font-family:\'JetBrains Mono\',monospace;">⚠ Error: {res["error"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background:#1d0b0e;border:1px solid #ff8c4222;border-radius:8px;padding:10px 14px;margin-bottom:10px;">
                    <div style="font-size:0.62rem;color:#ff8c42;font-family:'JetBrains Mono',monospace;margin-bottom:4px;">YOUR PROMPT</div>
                    <div style="color:#fdf0e8;font-size:0.9rem;font-family:'Crimson Pro',serif;">{res['query']}</div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:10px;">
                    <span style="font-size:0.66rem;padding:3px 10px;border-radius:8px;background:#ff6b3510;color:#ff6b35;border:1px solid #ff6b3522;font-family:'JetBrains Mono',monospace;">⏱ {res['rt']:.1f}s</span>
                    <span style="font-size:0.66rem;padding:3px 10px;border-radius:8px;background:#f7c94810;color:#f7c948;border:1px solid #f7c94822;font-family:'JetBrains Mono',monospace;">⚡ ~{res['tokens']} tokens</span>
                    <span style="font-size:0.66rem;padding:3px 10px;border-radius:8px;background:#c084fc10;color:#c084fc;border:1px solid #c084fc22;font-family:'JetBrains Mono',monospace;">🤖 {res['model']}</span>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div style="background:#0d0406;border:1px solid #2a1015;border-left:3px solid #ff6b35;border-radius:10px;
                    padding:18px;color:#e8d5c8;font-family:'Crimson Pro',serif;font-size:0.97rem;
                    line-height:1.8;max-height:60vh;overflow-y:auto;">
                    {format_content(res['response'])}
                </div>
                """, unsafe_allow_html=True)

                st.download_button("📥 Download Response", data=f"Prompt: {res['query']}\n\nResponse:\n{res['response']}",
                    file_name="phoenix_prompt_response.txt", mime="text/plain",
                    key="pt_download", use_container_width=True)
        else:
            st.markdown("""
            <div style="background:#0d0406;border:1px solid #2a1015;border-radius:12px;padding:40px 20px;
                text-align:center;color:#4a2a22;font-family:'JetBrains Mono',monospace;font-size:0.8rem;min-height:300px;
                display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;">
                <div style="font-size:2.5rem;animation:float 3s ease-in-out infinite;">📄</div>
                <div>Select "Show Here" or "Both" mode,<br>then click ▶ next to any prompt<br>to see the AI response here</div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
# TAB 3: ANALYTICS
# ══════════════════════════════════════════════════════════════════
with tab_analytics:
    st.markdown('<div style="font-family:\'Cinzel\',serif;font-size:1rem;font-weight:700;background:linear-gradient(135deg,#ff6b35,#f7c948);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;letter-spacing:2px;margin-bottom:1rem;">📊 CONVERSATION ANALYTICS</div>', unsafe_allow_html=True)

    valid_a = [a for a in st.session_state.analytics if a]

    if not st.session_state.messages:
        st.markdown("""
        <div style="text-align:center;padding:3rem;color:#4a2a22;font-family:'JetBrains Mono',monospace;">
            <div style="font-size:3rem;margin-bottom:1rem;animation:float 3s ease-in-out infinite;display:inline-block;">📊</div>
            <div>Start chatting to see real-time analytics</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        ai_msgs   = [m for m in st.session_state.messages if m["role"] == "assistant"]
        user_msgs = [m for m in st.session_state.messages if m["role"] == "user"]
        avg_len   = sum(len(m["content"]) for m in ai_msgs) // max(1, len(ai_msgs))
        sentiments = [a["sentiment"] for a in valid_a]
        intents    = [a["intent"] for a in valid_a]
        avg_rt     = sum(a.get("response_time",0) for a in valid_a) / max(1, len(valid_a))
        avg_cps    = sum(a.get("chars_per_sec",0) for a in valid_a) / max(1, len(valid_a))
        pos        = sentiments.count("positive")
        total_resp_chars = sum(a.get("response_length", len(ai_msgs[i]["content"])) for i, a in enumerate(valid_a) if i < len(ai_msgs))

        m1, m2, m3, m4, m5, m6 = st.columns(6)
        m1.metric("Exchanges", len(ai_msgs))
        m2.metric("Avg Length", f"{avg_len} ch")
        m3.metric("Total Tokens", f"~{st.session_state.total_tokens:,}")
        m4.metric("Positive Rate", f"{pos/max(1,len(sentiments)):.0%}")
        m5.metric("Avg Speed", f"{avg_cps:.0f} c/s")
        m6.metric("Avg RT", f"{avg_rt:.1f}s")

        st.markdown("<br>", unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            if sentiments:
                sc = Counter(sentiments)
                colors_map = {"positive": "#52b788", "negative": "#e63946", "neutral": "#c8917a"}
                fig = go.Figure(data=[go.Pie(
                    labels=list(sc.keys()), values=list(sc.values()), hole=0.6,
                    marker=dict(colors=[colors_map.get(k, "#aaa") for k in sc.keys()], line=dict(color='#060203', width=2)),
                    textfont=dict(color='#fdf0e8', size=11),
                )])
                fig.update_layout(
                    title=dict(text="Sentiment Distribution", font=dict(color="#ff6b35", size=13, family="Cinzel")),
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#c8917a"), legend=dict(font=dict(color="#c8917a"), bgcolor="rgba(0,0,0,0)"),
                    margin=dict(t=40, b=20, l=20, r=20),
                    annotations=[dict(text=f"{pos/max(1,len(sentiments)):.0%}<br>positive", x=0.5, y=0.5,
                        font_size=13, showarrow=False, font=dict(color="#52b788", family="Cinzel"))]
                )
                st.plotly_chart(fig, use_container_width=True)

        with c2:
            if intents:
                ic = Counter(intents)
                fig2 = go.Figure(go.Bar(
                    x=list(ic.values()), y=list(ic.keys()), orientation='h',
                    marker=dict(color=list(ic.values()),
                        colorscale=[[0,"#e63946"],[0.33,"#ff6b35"],[0.66,"#f7c948"],[1,"#52b788"]],
                        line=dict(color='rgba(0,0,0,0)', width=0)),
                    text=list(ic.values()), textposition='auto',
                    textfont=dict(color='#fdf0e8', size=11),
                ))
                fig2.update_layout(
                    title=dict(text="Intent Distribution", font=dict(color="#ff6b35", size=13, family="Cinzel")),
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#c8917a"),
                    xaxis=dict(gridcolor="#2a1015", color="#c8917a"),
                    yaxis=dict(gridcolor="rgba(0,0,0,0)", color="#c8917a"),
                    margin=dict(t=40, b=20, l=20, r=20),
                )
                st.plotly_chart(fig2, use_container_width=True)

        if len(ai_msgs) > 1:
            lengths  = [len(m["content"]) for m in ai_msgs]
            rt_times = [a.get("response_time", 0) for a in valid_a]
            cps_list = [a.get("chars_per_sec", 0) for a in valid_a]
            x_axis   = list(range(1, len(lengths)+1))

            fig3 = make_subplots(rows=1, cols=2,
                subplot_titles=("Response Length Over Time", "Response Time & Speed"))
            fig3.add_trace(go.Scatter(
                x=x_axis, y=lengths, mode='lines+markers', name="Length (chars)",
                line=dict(color="#ff6b35", width=2.5),
                marker=dict(color="#ff6b35", size=7, line=dict(color="#060203", width=1)),
                fill='tozeroy', fillcolor="rgba(255,107,53,0.07)",
            ), row=1, col=1)
            if rt_times:
                fig3.add_trace(go.Scatter(
                    x=x_axis[:len(rt_times)], y=rt_times, mode='lines+markers', name="RT (s)",
                    line=dict(color="#f7c948", width=2),
                    marker=dict(color="#f7c948", size=7),
                ), row=1, col=2)
                fig3.add_trace(go.Scatter(
                    x=x_axis[:len(cps_list)], y=cps_list, mode='lines+markers', name="Speed (c/s)",
                    line=dict(color="#52b788", width=2, dash="dot"),
                    marker=dict(color="#52b788", size=6),
                ), row=1, col=2)
            fig3.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#c8917a"),
                xaxis=dict(gridcolor="#2a1015", color="#c8917a"),
                yaxis=dict(gridcolor="#2a1015", color="#c8917a"),
                xaxis2=dict(gridcolor="#2a1015", color="#c8917a"),
                yaxis2=dict(gridcolor="#2a1015", color="#c8917a"),
                showlegend=True,
                legend=dict(font=dict(color="#c8917a"), bgcolor="rgba(0,0,0,0)"),
                margin=dict(t=50, b=20, l=20, r=20),
            )
            st.plotly_chart(fig3, use_container_width=True)

        c3, c4 = st.columns(2)
        with c3:
            if valid_a:
                categories = ['Speed', 'Length', 'Positivity', 'Tokens', 'Consistency']
                max_rt = max((a.get("response_time",1) for a in valid_a), default=1)
                max_len = max((a.get("response_length", 500) for a in valid_a), default=500)
                max_tok = max((a.get("tokens",1) for a in valid_a), default=1)
                last_a = valid_a[-1] if valid_a else {}
                values = [
                    100 - min(100, (last_a.get("response_time", avg_rt) / max(max_rt, 0.001)) * 100),
                    min(100, (last_a.get("response_length", avg_len) / max(max_len, 1)) * 100),
                    (last_a.get("sentiment_score", 0.5)) * 100,
                    min(100, (last_a.get("tokens", 100) / max(max_tok, 1)) * 100),
                    50 + (pos / max(1, len(sentiments)) - 0.5) * 100,
                ]
                fig_r = go.Figure(data=go.Scatterpolar(
                    r=values + [values[0]],
                    theta=categories + [categories[0]],
                    fill='toself', fillcolor='rgba(255,107,53,0.1)',
                    line=dict(color='#ff6b35', width=2),
                    marker=dict(color='#f7c948', size=7),
                ))
                fig_r.update_layout(
                    title=dict(text="Last Response Radar", font=dict(color="#ff6b35", size=13, family="Cinzel")),
                    polar=dict(
                        bgcolor='rgba(0,0,0,0)',
                        radialaxis=dict(visible=True, range=[0, 100], gridcolor='#2a1015', color='#4a2a22', tickfont=dict(size=9)),
                        angularaxis=dict(gridcolor='#2a1015', color='#c8917a'),
                    ),
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#c8917a'),
                    margin=dict(t=50, b=20, l=40, r=40),
                )
                st.plotly_chart(fig_r, use_container_width=True)

        with c4:
            if valid_a:
                token_vals = [a.get("tokens", 0) for a in valid_a]
                x_tok = list(range(1, len(token_vals)+1))
                cumulative = [sum(token_vals[:i+1]) for i in range(len(token_vals))]
                fig_t = go.Figure()
                fig_t.add_trace(go.Bar(
                    x=x_tok, y=token_vals, name="Tokens per Response",
                    marker=dict(color=token_vals,
                        colorscale=[[0,"#2a1015"],[0.5,"#ff6b35"],[1,"#f7c948"]],
                        line=dict(color='rgba(0,0,0,0)'),
                    ),
                ))
                fig_t.add_trace(go.Scatter(
                    x=x_tok, y=cumulative, name="Cumulative", yaxis="y2",
                    line=dict(color="#c084fc", width=2, dash="dot"),
                    marker=dict(color="#c084fc", size=5),
                ))
                fig_t.update_layout(
                    title=dict(text="Token Usage Per Response", font=dict(color="#ff6b35", size=13, family="Cinzel")),
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#c8917a"),
                    xaxis=dict(gridcolor="#2a1015", color="#c8917a", title="Response #"),
                    yaxis=dict(gridcolor="#2a1015", color="#c8917a", title="Tokens"),
                    yaxis2=dict(overlaying='y', side='right', color="#c084fc", title="Cumulative"),
                    showlegend=True, legend=dict(font=dict(color="#c8917a"), bgcolor="rgba(0,0,0,0)"),
                    margin=dict(t=40, b=20, l=20, r=40),
                )
                st.plotly_chart(fig_t, use_container_width=True)

        st.markdown('<div style="font-size:0.76rem;color:#c8917a;margin-bottom:8px;font-family:\'JetBrains Mono\',monospace;">RECENT EXCHANGES</div>', unsafe_allow_html=True)
        rows = []
        for i, a in enumerate(reversed(valid_a[-10:])):
            rows.append({
                "#": len(valid_a) - i,
                "Intent": a.get("intent","—"),
                "Sentiment": a.get("sentiment","—").title(),
                "Readability": a.get("readability","—"),
                "Tokens": f"~{a.get('tokens',0)}",
                "RT (s)": f"{a.get('response_time',0):.1f}",
                "Speed": f"{a.get('chars_per_sec',0):.0f} c/s",
            })
        if rows:
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════════
# TAB 4: NLP LAB
# ══════════════════════════════════════════════════════════════════
with tab_nlp:
    st.markdown('<div style="font-family:\'Cinzel\',serif;font-size:1rem;font-weight:700;background:linear-gradient(135deg,#ff6b35,#f7c948);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;letter-spacing:2px;margin-bottom:1rem;">🔬 NLP ANALYSIS LAB</div>', unsafe_allow_html=True)

    nlp_subtab_local, nlp_subtab_ai = st.tabs(["📊 Local Text Analysis", "🧠 AI Deep Research Report"])

    with nlp_subtab_local:
        nlp_text = st.text_area("Enter text to analyze",
            placeholder="Paste any text here for real-time NLP analysis…",
            height=130, key="nlp_input")

        if nlp_text.strip():
            sent, score = sentiment_score(nlp_text)
            intent      = detect_intent(nlp_text)
            keywords    = extract_keywords(nlp_text)
            token_est   = count_tokens_approx(nlp_text)
            words       = len(nlp_text.split())
            sents       = len(re.split(r'[.!?]+', nlp_text))
            avg_wl      = sum(len(w) for w in nlp_text.split()) / max(1, words)
            read        = readability_score(nlp_text)

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Sentiment", sent.title())
            c2.metric("Confidence", f"{score:.0%}")
            c3.metric("Intent", intent)
            c4.metric("Tokens", f"~{token_est}")

            st.markdown("<br>", unsafe_allow_html=True)
            ca, cb, cc = st.columns(3)

            with ca:
                st.markdown('<div style="font-size:0.76rem;color:#c8917a;margin-bottom:8px;font-family:\'JetBrains Mono\',monospace;">📊 TEXT STATISTICS</div>', unsafe_allow_html=True)
                complexity = 'High' if avg_wl > 5.5 else 'Medium' if avg_wl > 4 else 'Low'
                st.markdown(f"""
                <div style="background:#0d0406;border:1px solid #2a1015;border-radius:10px;padding:16px;font-family:'JetBrains Mono',monospace;">
                    <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;font-size:0.76rem;">
                        <div style="color:#4a2a22;">Characters</div><div style="color:#ff6b35;font-weight:700;">{len(nlp_text):,}</div>
                        <div style="color:#4a2a22;">Words</div><div style="color:#ff6b35;font-weight:700;">{words:,}</div>
                        <div style="color:#4a2a22;">Sentences</div><div style="color:#ff6b35;font-weight:700;">{sents}</div>
                        <div style="color:#4a2a22;">Avg Word Len</div><div style="color:#ff6b35;font-weight:700;">{avg_wl:.1f} chars</div>
                        <div style="color:#4a2a22;">Reading Time</div><div style="color:#f7c948;font-weight:700;">~{max(1,words//200)} min</div>
                        <div style="color:#4a2a22;">Complexity</div><div style="color:#ff8c42;font-weight:700;">{complexity}</div>
                        <div style="color:#4a2a22;">Readability</div><div style="color:#52b788;font-weight:700;">{read}</div>
                        <div style="color:#4a2a22;">Token/Word</div><div style="color:#c8917a;font-weight:700;">{token_est/max(1,words):.1f}x</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with cb:
                st.markdown('<div style="font-size:0.76rem;color:#c8917a;margin-bottom:8px;font-family:\'JetBrains Mono\',monospace;">🔑 TOP KEYWORDS</div>', unsafe_allow_html=True)
                if keywords:
                    mf = keywords[0][1]
                    colors_kw = ["#ff6b35","#f7c948","#ff8c42","#e63946","#52b788","#c084fc","#74c0fc","#fb923c"]
                    kw_html = ""
                    for i, (word, freq) in enumerate(keywords[:8]):
                        w = int(freq / mf * 100)
                        c = colors_kw[i % len(colors_kw)]
                        kw_html += f"""<div style="display:flex;align-items:center;gap:8px;margin-bottom:7px;">
                            <span style="font-size:0.72rem;color:{c};min-width:80px;font-weight:700;font-family:'JetBrains Mono',monospace;">{word}</span>
                            <div style="flex:1;height:5px;background:#1d0b0e;border-radius:3px;overflow:hidden;">
                                <div style="width:{w}%;height:100%;background:{c};border-radius:3px;box-shadow:0 0 6px {c};"></div>
                            </div>
                            <span style="font-size:0.64rem;color:#4a2a22;min-width:16px;text-align:right;">{freq}</span>
                        </div>"""
                    st.markdown(f'<div style="background:#0d0406;border:1px solid #2a1015;border-radius:10px;padding:16px;">{kw_html}</div>', unsafe_allow_html=True)

            with cc:
                sc_color = {"positive":"#52b788","negative":"#e63946","neutral":"#c8917a"}.get(sent,"#c8917a")
                gauge = go.Figure(go.Indicator(
                    mode="gauge+number", value=score * 100,
                    domain={'x':[0,1],'y':[0,1]},
                    title={'text':f"Sentiment: {sent.title()}", 'font':{'color':'#fdf0e8','size':12,'family':'Cinzel'}},
                    number={'font':{'color':sc_color,'size':26,'family':'Cinzel'},'suffix':'%'},
                    gauge={
                        'axis':{'range':[0,100],'tickcolor':'#4a2a22','tickfont':{'color':'#4a2a22'}},
                        'bar':{'color':sc_color,'thickness':0.25},
                        'bgcolor':'#2a1015','bordercolor':'#3a1a20',
                        'steps':[{'range':[0,40],'color':'#0d0406'},{'range':[40,70],'color':'#120508'},{'range':[70,100],'color':'#170608'}],
                        'threshold':{'line':{'color':sc_color,'width':2},'thickness':0.75,'value':score*100}
                    }
                ))
                gauge.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#c8917a"),
                    height=220, margin=dict(t=40,b=10,l=30,r=30))
                st.plotly_chart(gauge, use_container_width=True)

            if keywords:
                st.markdown('<div style="font-size:0.76rem;color:#c8917a;margin:10px 0 8px;font-family:\'JetBrains Mono\',monospace;">📈 KEYWORD FREQUENCY CHART</div>', unsafe_allow_html=True)
                kw_words = [k[0] for k in keywords]
                kw_freqs = [k[1] for k in keywords]
                fig_kw = go.Figure(go.Bar(
                    x=kw_words, y=kw_freqs,
                    marker=dict(color=kw_freqs,
                        colorscale=[[0,"#2a1015"],[0.3,"#ff6b35"],[0.7,"#f7c948"],[1,"#52b788"]],
                        line=dict(color='rgba(0,0,0,0)'),
                    ),
                    text=kw_freqs, textposition='auto',
                    textfont=dict(color='#fdf0e8', size=11),
                ))
                fig_kw.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#c8917a"),
                    xaxis=dict(gridcolor="#2a1015", color="#c8917a"),
                    yaxis=dict(gridcolor="#2a1015", color="#c8917a", title="Count"),
                    margin=dict(t=20, b=30, l=40, r=20), height=250,
                )
                st.plotly_chart(fig_kw, use_container_width=True)

        else:
            st.markdown("""
            <div style="text-align:center;padding:3rem;color:#4a2a22;font-family:'JetBrains Mono',monospace;">
                <div style="font-size:3rem;margin-bottom:1rem;animation:float 3s ease-in-out infinite;display:inline-block;">🔬</div>
                <div>Enter any text above to run local NLP analysis</div>
            </div>
            """, unsafe_allow_html=True)

    # ── SUB-TAB B: AI Deep Research Report ─────────────────────────
    with nlp_subtab_ai:
        st.markdown("""
        <div style="background:#0d0406;border:1px solid #ff6b3522;border-radius:10px;padding:14px 18px;margin-bottom:16px;font-size:0.82rem;color:#c8917a;font-family:'Crimson Pro',serif;line-height:1.7;">
            🧠 <strong style="color:#ff6b35;">AI Deep Research Report</strong> — Enter any topic, question, or scenario and the AI will generate a comprehensive, structured research report displayed right here in this tab.
        </div>
        """, unsafe_allow_html=True)

        research_query = st.text_area(
            "Research Topic / Question / Situation",
            placeholder="e.g. 'Explain transformer attention mechanisms in LLMs'\nor 'Analyze the pros and cons of microservices vs monolith'\nor 'Research report on climate change impact on agriculture'",
            height=110,
            key="research_query_input"
        )

        col_rd1, col_rd2 = st.columns(2)
        with col_rd1:
            report_depth = st.selectbox("Report Depth", [
                "Quick Summary (300 words)",
                "Standard Report (600 words)",
                "Detailed Analysis (1000 words)",
                "Comprehensive Deep-Dive (1500+ words)",
            ], index=1, key="report_depth")
        with col_rd2:
            report_style = st.selectbox("Report Style", [
                "🔬 Academic / Scientific",
                "💼 Business / Executive",
                "🎓 Educational / Beginner-friendly",
                "💻 Technical / Developer-focused",
                "📰 Journalistic / Narrative",
            ], index=0, key="report_style")

        if st.button("🔥 Generate Deep Research Report", use_container_width=True, key="gen_research_btn"):
            if not research_query.strip():
                st.warning("Please enter a research topic or question.")
            elif not active_api_key:
                st.error("⚠ No API key configured in the sidebar.")
            else:
                depth_tokens = {"Quick Summary (300 words)": 500, "Standard Report (600 words)": 900,
                                "Detailed Analysis (1000 words)": 1500, "Comprehensive Deep-Dive (1500+ words)": 2500}
                max_report_tokens = depth_tokens.get(report_depth, 900)
                style_desc = report_style.split(" ", 1)[1]

                research_prompt = f"""You are an expert research analyst. Write a {report_depth} in a {style_desc} style on the following topic:

TOPIC: {research_query}

Structure your report with ALL of the following sections using clear markdown headers:

# Research Report: {research_query[:80]}

## 📋 Executive Summary
[2-3 sentence overview of the topic and key findings]

## 🔍 Background & Context
[Historical context, why this topic matters, current state]

## 🧩 Key Concepts & Components
[Break down the main ideas, terms, mechanisms involved]

## 📊 Detailed Analysis
[Deep dive into the topic — mechanisms, causes, effects, how it works]

## ✅ Advantages / Strengths
[What works well, benefits, positive aspects]

## ⚠️ Challenges / Limitations
[Problems, risks, drawbacks, open questions]

## 💡 Real-World Applications / Use Cases
[Concrete examples of where/how this is applied]

## 🔮 Future Outlook & Trends
[Where is this heading? Emerging developments]

## 📌 Key Takeaways & Recommendations
[Bullet points of the most important things to remember + actionable recommendations]

## 📚 Further Reading Suggestions
[3-5 suggested topics or resources the reader should explore next]

Be thorough, accurate, well-structured, and use specific examples. Do NOT be vague or generic."""

                with st.spinner(f"🔥 Generating {report_depth} on: {research_query[:60]}…"):
                    try:
                        t0 = time.time()
                        report_response = call_ai(
                            provider, model_sel,
                            [{"role": "user", "content": research_prompt}],
                            "You are an expert research analyst and writer. Always produce structured, detailed, accurate reports with concrete examples and specific insights. Never give vague or generic answers.",
                            0.4, max_report_tokens, active_api_key
                        )
                        # Remove comments
                        report_response = re.sub(r'<!--.*?-->', '', report_response, flags=re.DOTALL)


                        report_response = re.sub(r'<[^>]+>', '', report_response)

                        report_response = re.sub(r'\n\s*\n+', '\n\n', report_response).strip()
                        rt_report = round(time.time() - t0, 2)

                        rpt_obj = {
                            "query":     research_query,
                            "report":    report_response,
                            "depth":     report_depth,
                            "style":     report_style,
                            "model":     model_sel,
                            "rt":        rt_report,
                            "timestamp": datetime.now().strftime("%H:%M %d/%m"),
                            "tokens":    count_tokens_approx(report_response),
                            "words":     len(report_response.split()),
                        }
                        st.session_state.research_reports.append(rpt_obj)
                        st.session_state.last_report = rpt_obj

                        # ── INLINE REPORT SUMMARY (replaces broken button) ──
                        rpt_words = report_response.split()
                        rpt_sentences = re.split(r'[.!?]+', report_response)
                        rpt_sent_score, rpt_s_val = sentiment_score(report_response)
                        rpt_keywords = extract_keywords(report_response, top_n=6)
                        rpt_read = readability_score(report_response)

                        # Extract executive summary (text after "Executive Summary" header)
                        exec_match = re.search(r'##\s*.*Executive Summary.*\n+([\s\S]*?)(?=\n##|\Z)', report_response, re.IGNORECASE)
                        exec_summary = call_ai(provider, model_sel, [{"role": "user", "content": f"Summarize the following report in 2-3 concise lines:\n\n{report_response}"}], "You are a summarization assistant.", 0.2, 150, active_api_key).strip()[:500] if report_response else "No summary available."

                        # Extract key takeaways
                        key_match = re.search(r'Key Takeaways[^\n]*\n+([\s\S]*?)(?=##|$)', report_response, re.IGNORECASE)
                        key_takeaways_raw = key_match.group(1).strip() if key_match else ""

                        # ── SUMMARY CARD ──
                        st.markdown(f"""
                        <div style="background:linear-gradient(135deg,#0d0406,#060203);border:1px solid #ff6b3540;
                            border-radius:16px;padding:0;margin:14px 0;position:relative;overflow:hidden;">
                            <div style="height:3px;background:linear-gradient(90deg,#e63946,#ff6b35,#f7c948,#52b788,#74c0fc,#c084fc);"></div>
                            <div style="padding:18px 22px 14px;">
                                <div style="font-family:'Cinzel',serif;font-size:1rem;color:#ff6b35;font-weight:700;margin-bottom:4px;">
                                    📋 Report Summary
                                </div>
                                <div style="font-size:0.68rem;color:#4a2a22;font-family:'JetBrains Mono',monospace;margin-bottom:12px;">
                                    {research_query[:80]}{"…" if len(research_query)>80 else ""}
                                </div>

                                <!-- Stat pills -->
                                <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px;">
                                    <span style="font-size:0.65rem;padding:3px 10px;border-radius:20px;background:#ff6b3510;color:#ff6b35;border:1px solid #ff6b3522;font-family:'JetBrains Mono',monospace;">⏱ {rt_report:.1f}s</span>
                                    <span style="font-size:0.65rem;padding:3px 10px;border-radius:20px;background:#f7c94810;color:#f7c948;border:1px solid #f7c94822;font-family:'JetBrains Mono',monospace;">⚡ ~{count_tokens_approx(report_response):,} tokens</span>
                                    <span style="font-size:0.65rem;padding:3px 10px;border-radius:20px;background:#52b78810;color:#52b788;border:1px solid #52b78822;font-family:'JetBrains Mono',monospace;">📖 {len(rpt_words)} words</span>
                                    <span style="font-size:0.65rem;padding:3px 10px;border-radius:20px;background:#c084fc10;color:#c084fc;border:1px solid #c084fc22;font-family:'JetBrains Mono',monospace;">🤖 {model_sel}</span>
                                    <span style="font-size:0.65rem;padding:3px 10px;border-radius:20px;background:#74c0fc10;color:#74c0fc;border:1px solid #74c0fc22;font-family:'JetBrains Mono',monospace;">📝 {rpt_read}</span>
                                    <span style="font-size:0.65rem;padding:3px 10px;border-radius:20px;background:#ff8c4210;color:#ff8c42;border:1px solid #ff8c4222;font-family:'JetBrains Mono',monospace;">💡 {report_depth.split("(")[0].strip()}</span>
                                </div>

                                <!-- Executive Summary -->
                                <div style="background:#1d0b0e;border:1px solid #ff6b3520;border-left:3px solid #ff6b35;border-radius:10px;padding:14px;margin-bottom:12px;">
                                    <div style="font-size:0.62rem;color:#ff6b35;font-family:'JetBrains Mono',monospace;letter-spacing:2px;margin-bottom:6px;">📋 EXECUTIVE SUMMARY</div>
                                    <div style="color:#e8d5c8;font-family:'Crimson Pro',serif;font-size:0.95rem;line-height:1.75;">{exec_summary}</div>
                                </div>

                                <!-- Keywords -->
                                <div style="margin-bottom:12px;">
                                    <div style="font-size:0.62rem;color:#f7c948;font-family:'JetBrains Mono',monospace;letter-spacing:2px;margin-bottom:6px;">🔑 KEY CONCEPTS</div>
                                    <div style="display:flex;gap:6px;flex-wrap:wrap;">
                                        {"".join(f'<span style="font-size:0.72rem;padding:3px 10px;border-radius:20px;background:#f7c94810;color:#f7c948;border:1px solid #f7c94822;font-family:JetBrains Mono,monospace;">{kw}</span>' for kw, _ in rpt_keywords)}
                                    </div>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                        # ── NLP Analysis of the report ──
                        col_nlp1, col_nlp2, col_nlp3 = st.columns(3)
                        with col_nlp1:
                            sc_rpt = {"positive":"#52b788","negative":"#e63946","neutral":"#c8917a"}.get(rpt_sent_score,"#c8917a")
                            st.markdown(f"""
                            <div style="background:#0d0406;border:1px solid #2a1015;border-radius:10px;padding:14px;text-align:center;">
                                <div style="font-size:0.62rem;color:#4a2a22;font-family:'JetBrains Mono',monospace;letter-spacing:2px;margin-bottom:6px;">REPORT TONE</div>
                                <div style="font-family:'Cinzel',serif;font-size:1.4rem;color:{sc_rpt};font-weight:700;">{rpt_sent_score.title()}</div>
                                <div style="font-size:0.72rem;color:#4a2a22;font-family:'JetBrains Mono',monospace;">{rpt_s_val:.0%} confidence</div>
                            </div>
                            """, unsafe_allow_html=True)
                        with col_nlp2:
                            st.markdown(f"""
                            <div style="background:#0d0406;border:1px solid #2a1015;border-radius:10px;padding:14px;text-align:center;">
                                <div style="font-size:0.62rem;color:#4a2a22;font-family:'JetBrains Mono',monospace;letter-spacing:2px;margin-bottom:6px;">READABILITY</div>
                                <div style="font-family:'Cinzel',serif;font-size:1.4rem;color:#74c0fc;font-weight:700;">{rpt_read}</div>
                                <div style="font-size:0.72rem;color:#4a2a22;font-family:'JetBrains Mono',monospace;">{len(rpt_sentences)} sentences</div>
                            </div>
                            """, unsafe_allow_html=True)
                        with col_nlp3:
                            avg_wl_rpt = sum(len(w) for w in rpt_words) / max(1, len(rpt_words))
                            st.markdown(f"""
                            <div style="background:#0d0406;border:1px solid #2a1015;border-radius:10px;padding:14px;text-align:center;">
                                <div style="font-size:0.62rem;color:#4a2a22;font-family:'JetBrains Mono',monospace;letter-spacing:2px;margin-bottom:6px;">DEPTH SCORE</div>
                                <div style="font-family:'Cinzel',serif;font-size:1.4rem;color:#ff8c42;font-weight:700;">{min(100,int(len(rpt_words)/15))}%</div>
                                <div style="font-size:0.72rem;color:#4a2a22;font-family:'JetBrains Mono',monospace;">avg {avg_wl_rpt:.1f} chars/word</div>
                            </div>
                            """, unsafe_allow_html=True)

                        # ── Full report ──
                        st.markdown('<div style="font-size:0.76rem;color:#c8917a;margin:14px 0 6px;font-family:\'JetBrains Mono\',monospace;">📄 FULL REPORT</div>', unsafe_allow_html=True)
                        st.markdown(f"""
                        <div style="background:#0d0406;border:1px solid #2a1015;border-radius:0 0 14px 14px;
                            padding:24px;font-family:'Crimson Pro',serif;font-size:1rem;color:#e8d5c8;line-height:1.85;
                            max-height:70vh;overflow-y:auto;">
                            {format_content(report_response)}
                        </div>
                        """, unsafe_allow_html=True)

                        st.download_button(
                            "📥 Download Report as .txt",
                            data=f"PHOENIX AI RESEARCH REPORT\n{'='*50}\nTopic: {research_query}\nModel: {model_sel}\nDepth: {report_depth}\nStyle: {report_style}\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\nTime: {rt_report}s\n{'='*50}\n\n{report_response}",
                            file_name=f"phoenix_report_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                            mime="text/plain",
                            use_container_width=True,
                        )

                    except Exception as e:
                        st.error(f"⚠ Report generation failed: {str(e)}")
                        st.markdown(f'<div style="background:#120407;border:1px solid #7f1d1d;border-left:3px solid #e63946;border-radius:10px;padding:14px;color:#e63946;font-size:0.82rem;font-family:\'JetBrains Mono\',monospace;">Error: {str(e)}<br><br>Tips: Check your API key and provider selection.</div>', unsafe_allow_html=True)

        # Previous reports
        if "research_reports" in st.session_state and st.session_state.research_reports:
            st.divider()
            st.markdown(f'<div style="font-size:0.76rem;color:#c8917a;margin-bottom:8px;font-family:\'JetBrains Mono\',monospace;">📁 SAVED REPORTS ({len(st.session_state.research_reports)})</div>', unsafe_allow_html=True)
            for i, rpt in enumerate(reversed(st.session_state.research_reports[-5:])):
                with st.expander(f"📄 {rpt['query'][:60]}… · {rpt['timestamp']} · {rpt['model']}", expanded=False):
                    st.markdown(f'<div style="background:#0d0406;border:1px solid #2a1015;border-radius:10px;padding:16px;font-family:\'Crimson Pro\',serif;font-size:0.95rem;color:#e8d5c8;line-height:1.8;max-height:400px;overflow-y:auto;">{format_content(rpt["report"])}</div>', unsafe_allow_html=True)
                    st.download_button(
                        "📥 Download", data=rpt["report"],
                        file_name=f"report_{i}.txt", mime="text/plain",
                        key=f"dl_report_{i}", use_container_width=True
                    )
        else:
            st.markdown("""
            <div style="text-align:center;padding:3rem;color:#4a2a22;font-family:'JetBrains Mono',monospace;">
                <div style="font-size:3rem;margin-bottom:1rem;animation:float 3s ease-in-out infinite;display:inline-block;">🧠</div>
                <div>Enter a topic above to generate your first AI research report</div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
# TAB 5: DEEP STATS
# ══════════════════════════════════════════════════════════════════
with tab_deepstats:
    st.markdown('<div style="font-family:\'Cinzel\',serif;font-size:1rem;font-weight:700;background:linear-gradient(135deg,#ff6b35,#f7c948);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;letter-spacing:2px;margin-bottom:1rem;">📈 DEEP STATISTICS</div>', unsafe_allow_html=True)

    valid_a = [a for a in st.session_state.analytics if a]

    if not valid_a:
        st.markdown('<div style="text-align:center;padding:3rem;color:#4a2a22;font-family:\'JetBrains Mono\',monospace;"><div style="font-size:3rem;margin-bottom:1rem;display:inline-block;">📈</div><div>Chat to generate deep statistics</div></div>', unsafe_allow_html=True)
    else:
        c1, c2 = st.columns(2)
        with c1:
            if st.session_state.provider_usage:
                pu = st.session_state.provider_usage
                fig_pu = go.Figure(data=[go.Pie(
                    labels=list(pu.keys()), values=list(pu.values()), hole=0.55,
                    marker=dict(colors=["#ff6b35","#74c0fc","#f7c948","#ff8c42","#e879f9","#c084fc"],
                                line=dict(color='#060203', width=2)),
                    textfont=dict(color='#fdf0e8', size=11),
                )])
                fig_pu.update_layout(
                    title=dict(text="Provider Usage", font=dict(color="#ff6b35", size=13, family="Cinzel")),
                    paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#c8917a"),
                    legend=dict(font=dict(color="#c8917a"), bgcolor="rgba(0,0,0,0)"),
                    margin=dict(t=40, b=20, l=20, r=20),
                )
                st.plotly_chart(fig_pu, use_container_width=True)
            else:
                st.info("No provider usage data yet.")

        with c2:
            if st.session_state.mood_log:
                ml = st.session_state.mood_log
                sent_map = {"positive": 1, "neutral": 0, "negative": -1}
                y_vals = [sent_map.get(m["sentiment"], 0) for m in ml]
                x_vals = [m["time"] for m in ml]
                colors_ml = ["#52b788" if v > 0 else "#e63946" if v < 0 else "#c8917a" for v in y_vals]
                fig_ml = go.Figure()
                fig_ml.add_trace(go.Scatter(
                    x=x_vals, y=y_vals, mode='lines+markers',
                    line=dict(color='#ff6b35', width=2),
                    marker=dict(color=colors_ml, size=10, line=dict(color='#060203', width=1)),
                    fill='tozeroy', fillcolor='rgba(255,107,53,0.07)',
                    name="Sentiment"
                ))
                fig_ml.update_layout(
                    title=dict(text="Sentiment Timeline", font=dict(color="#ff6b35", size=13, family="Cinzel")),
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#c8917a"),
                    xaxis=dict(gridcolor="#2a1015", color="#c8917a"),
                    yaxis=dict(gridcolor="#2a1015", color="#c8917a",
                        tickvals=[-1,0,1], ticktext=["Negative","Neutral","Positive"]),
                    margin=dict(t=40, b=20, l=20, r=20),
                )
                st.plotly_chart(fig_ml, use_container_width=True)

        if st.session_state.word_freq_all:
            st.markdown('<div style="font-size:0.76rem;color:#c8917a;margin:10px 0 8px;font-family:\'JetBrains Mono\',monospace;">🌐 GLOBAL WORD FREQUENCY (ALL CONVERSATIONS)</div>', unsafe_allow_html=True)
            top_words = sorted(st.session_state.word_freq_all.items(), key=lambda x: x[1], reverse=True)[:20]
            wf_words  = [w[0] for w in top_words]
            wf_freqs  = [w[1] for w in top_words]
            fig_wf = go.Figure(go.Bar(
                x=wf_words, y=wf_freqs,
                marker=dict(color=wf_freqs,
                    colorscale=[[0,"#1d0b0e"],[0.2,"#e63946"],[0.5,"#ff6b35"],[0.8,"#f7c948"],[1,"#52b788"]],
                    line=dict(color='rgba(0,0,0,0)'),
                ),
                text=wf_freqs, textposition='outside', textfont=dict(color='#c8917a', size=10),
            ))
            fig_wf.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#c8917a"),
                xaxis=dict(gridcolor="rgba(0,0,0,0)", color="#c8917a", tickangle=-35),
                yaxis=dict(gridcolor="#2a1015", color="#c8917a"),
                margin=dict(t=20, b=60, l=40, r=20), height=300,
            )
            st.plotly_chart(fig_wf, use_container_width=True)

        c3, c4 = st.columns(2)
        with c3:
            rt_all = [a.get("response_time", 0) for a in valid_a if a.get("response_time", 0) > 0]
            if rt_all:
                fig_hist = go.Figure(go.Histogram(
                    x=rt_all, nbinsx=min(10, len(rt_all)),
                    marker=dict(color='#ff6b35', line=dict(color='#060203', width=1)),
                    opacity=0.85,
                ))
                fig_hist.update_layout(
                    title=dict(text="Response Time Distribution", font=dict(color="#ff6b35", size=13, family="Cinzel")),
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#c8917a"),
                    xaxis=dict(gridcolor="#2a1015", color="#c8917a", title="RT (seconds)"),
                    yaxis=dict(gridcolor="#2a1015", color="#c8917a", title="Count"),
                    bargap=0.1, margin=dict(t=40, b=40, l=40, r=20),
                )
                st.plotly_chart(fig_hist, use_container_width=True)

        with c4:
            if len(valid_a) > 1:
                lens = [a.get("response_length", 500) for a in valid_a]
                rts2 = [a.get("response_time", 1) for a in valid_a]
                sents2 = [a.get("sentiment", "neutral") for a in valid_a]
                sent_color_map = {"positive":"#52b788","negative":"#e63946","neutral":"#c8917a"}
                marker_colors = [sent_color_map.get(s,"#c8917a") for s in sents2]
                fig_sc = go.Figure(go.Scatter(
                    x=rts2, y=lens, mode='markers',
                    marker=dict(color=marker_colors, size=12, line=dict(color='#060203', width=1),
                                opacity=0.85),
                    text=[f"RT: {r:.1f}s | {l} chars" for r, l in zip(rts2, lens)],
                    hovertemplate="%{text}<extra></extra>",
                ))
                fig_sc.update_layout(
                    title=dict(text="Speed vs Length (colored by sentiment)", font=dict(color="#ff6b35", size=13, family="Cinzel")),
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#c8917a"),
                    xaxis=dict(gridcolor="#2a1015", color="#c8917a", title="Response Time (s)"),
                    yaxis=dict(gridcolor="#2a1015", color="#c8917a", title="Length (chars)"),
                    margin=dict(t=40, b=40, l=40, r=20),
                )
                st.plotly_chart(fig_sc, use_container_width=True)

        readabilities = [a.get("readability","Medium") for a in valid_a if a.get("readability")]
        if readabilities:
            rc = Counter(readabilities)
            order = ["Very Easy","Easy","Medium","Complex","Very Complex"]
            vals  = [rc.get(k, 0) for k in order]
            fig_rd = go.Figure(go.Bar(
                x=order, y=vals,
                marker=dict(color=["#52b788","#74c0fc","#f7c948","#ff8c42","#e63946"],
                            line=dict(color='rgba(0,0,0,0)')),
                text=vals, textposition='auto', textfont=dict(color='#fdf0e8', size=11),
            ))
            fig_rd.update_layout(
                title=dict(text="Response Readability Distribution", font=dict(color="#ff6b35", size=13, family="Cinzel")),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#c8917a"),
                xaxis=dict(gridcolor="rgba(0,0,0,0)", color="#c8917a"),
                yaxis=dict(gridcolor="#2a1015", color="#c8917a"),
                margin=dict(t=40, b=30, l=40, r=20), height=280,
            )
            st.plotly_chart(fig_rd, use_container_width=True)


# ══════════════════════════════════════════════════════════════════
# TAB 6: NOTES
# ══════════════════════════════════════════════════════════════════
with tab_notes:
    st.markdown('<div style="font-family:\'Cinzel\',serif;font-size:1rem;font-weight:700;background:linear-gradient(135deg,#ff6b35,#f7c948);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;letter-spacing:2px;margin-bottom:1rem;">🗒️ SESSION NOTES</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.78rem;color:#4a2a22;font-family:\'JetBrains Mono\',monospace;margin-bottom:10px;">Save important snippets, ideas, or responses from your chat session</div>', unsafe_allow_html=True)

    with st.expander("➕ Add New Note", expanded=not st.session_state.notes):
        note_title = st.text_input("Title", placeholder="Note title…", key="note_title")
        note_content = st.text_area("Content", placeholder="Write your note…", height=100, key="note_content")
        note_tag = st.selectbox("Tag", ["💡 Idea","📌 Important","💻 Code","🔬 Research","✅ Todo","📊 Data","🎨 Creative"], key="note_tag")
        if st.button("💾 Save Note", use_container_width=True):
            if note_content.strip():
                st.session_state.notes.append({
                    "title": note_title or "Untitled",
                    "content": note_content.strip(),
                    "tag": note_tag,
                    "created": datetime.now().strftime("%H:%M %d/%m"),
                })
                st.success("Note saved!")
                st.rerun()

    if st.session_state.notes:
        all_tags = list(set(n["tag"] for n in st.session_state.notes))
        tag_filter = st.selectbox("Filter by tag", ["All"] + all_tags, key="notes_tag_filter")
        filtered_notes = st.session_state.notes if tag_filter == "All" else [n for n in st.session_state.notes if n["tag"] == tag_filter]

        st.markdown(f'<div style="font-size:0.72rem;color:#ff6b35;font-family:\'JetBrains Mono\',monospace;margin:8px 0;">{len(filtered_notes)} notes</div>', unsafe_allow_html=True)

        for i, note in enumerate(reversed(filtered_notes)):
            real_idx = len(st.session_state.notes) - 1 - i
            tag_color = {"💡 Idea":"#f7c948","📌 Important":"#e63946","💻 Code":"#74c0fc","🔬 Research":"#52b788","✅ Todo":"#ff8c42","📊 Data":"#c084fc","🎨 Creative":"#ff6b35"}.get(note["tag"], "#c8917a")
            with st.expander(f"{note['tag']} · {note['title']} · {note['created']}", expanded=False):
                st.markdown(f'<div style="color:#e8d5c8;line-height:1.8;font-family:\'Crimson Pro\',serif;white-space:pre-wrap;">{note["content"]}</div>', unsafe_allow_html=True)
                col_del, col_copy = st.columns(2)
                with col_del:
                    if st.button(f"🗑 Delete", key=f"del_note_{real_idx}", use_container_width=True):
                        st.session_state.notes.pop(real_idx)
                        st.rerun()

        st.divider()
        if st.button("📤 Export All Notes as JSON", use_container_width=True):
            export_notes = json.dumps({"notes": st.session_state.notes, "exported_at": datetime.now().isoformat()}, indent=2)
            st.download_button("💾 Download Notes", export_notes,
                file_name=f"phoenix_notes_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                mime="application/json", use_container_width=True)
    else:
        st.markdown("""
        <div style="text-align:center;padding:3rem;color:#4a2a22;font-family:'JetBrains Mono',monospace;">
            <div style="font-size:3rem;margin-bottom:1rem;animation:float 3s ease-in-out infinite;display:inline-block;">🗒️</div>
            <div>No notes yet — save snippets from your chat above!</div>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
# TAB 7: BENCHMARK
# ══════════════════════════════════════════════════════════════════
with tab_bench:
    st.markdown('<div style="font-family:\'Cinzel\',serif;font-size:1rem;font-weight:700;background:linear-gradient(135deg,#ff6b35,#f7c948);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;letter-spacing:2px;margin-bottom:1rem;">⚡ MODEL BENCHMARKING</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.78rem;color:#4a2a22;font-family:\'JetBrains Mono\',monospace;margin-bottom:12px;">Run timed benchmarks to compare model performance on standard tasks</div>', unsafe_allow_html=True)

    BENCH_PROMPTS = {
        "🧮 Math": "What is 15 * 17 + sqrt(144)? Show your work step by step.",
        "💻 Code":  "Write a Python function that checks if a number is prime. Include docstring.",
        "✍️ Creative": "Write a 3-sentence description of a futuristic city in 2200.",
        "🧠 Reasoning": "If all Bloops are Razzies and all Razzies are Lazzies, are all Bloops definitely Lazzies? Explain.",
        "📊 Summary": "In one paragraph, explain what machine learning is to a 10-year-old.",
    }

    col_b1, col_b2 = st.columns(2)
    with col_b1:
        bench_task = st.selectbox("Select benchmark task", list(BENCH_PROMPTS.keys()), key="bench_task")
    with col_b2:
        bench_prompt_preview = st.text_area("Prompt", value=BENCH_PROMPTS[bench_task], height=80, key="bench_prompt_preview")

    if st.button("🔥 Run Benchmark", use_container_width=True, type="primary"):
        if not active_api_key:
            st.error("⚠ No API key configured.")
        else:
            with st.spinner("Running benchmark…"):
                t0 = time.time()
                try:
                    result = call_ai(provider, model_sel,
                        [{"role":"user","content":bench_prompt_preview}],
                        "You are a helpful assistant. Be concise.",
                        0.3, 512, active_api_key)
                    rt_bench = round(time.time() - t0, 2)
                    toks = count_tokens_approx(result)
                    cps_bench = round(len(result) / max(0.01, rt_bench), 1)
                    bench_entry = {
                        "task": bench_task, "model": model_sel, "provider": provider,
                        "rt": rt_bench, "tokens": toks, "length": len(result),
                        "cps": cps_bench, "timestamp": datetime.now().strftime("%H:%M"),
                        "result_preview": result[:300] + ("…" if len(result) > 300 else ""),
                    }
                    st.session_state.benchmarks.append(bench_entry)

                    st.markdown(f"""
                    <div style="background:#0d0406;border:1px solid #52b78840;border-left:3px solid #52b788;border-radius:10px;padding:16px;margin:10px 0;">
                        <div style="display:flex;gap:20px;margin-bottom:10px;flex-wrap:wrap;">
                            <span style="color:#52b788;font-family:'JetBrains Mono',monospace;font-size:0.8rem;">✅ Completed</span>
                            <span style="color:#ff6b35;font-family:'JetBrains Mono',monospace;font-size:0.8rem;">⏱ {rt_bench}s</span>
                            <span style="color:#f7c948;font-family:'JetBrains Mono',monospace;font-size:0.8rem;">⚡ ~{toks} tokens</span>
                            <span style="color:#c084fc;font-family:'JetBrains Mono',monospace;font-size:0.8rem;">🚀 {cps_bench} c/s</span>
                        </div>
                        <div style="color:#e8d5c8;font-family:'Crimson Pro',serif;font-size:0.95rem;line-height:1.7;">{format_content(result)}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.success("Benchmark saved to history!")
                except Exception as e:
                    st.error(f"Benchmark failed: {e}")

    if st.session_state.benchmarks:
        st.markdown('<div style="font-size:0.76rem;color:#c8917a;margin:14px 0 8px;font-family:\'JetBrains Mono\',monospace;">📋 BENCHMARK HISTORY</div>', unsafe_allow_html=True)
        bench_df = pd.DataFrame([{
            "Time": b["timestamp"], "Task": b["task"], "Model": b["model"],
            "RT (s)": b["rt"], "Tokens": b["tokens"], "Speed (c/s)": b["cps"],
        } for b in st.session_state.benchmarks])
        st.dataframe(bench_df, use_container_width=True, hide_index=True)

        if len(st.session_state.benchmarks) > 1:
            fig_bench = go.Figure()
            tasks_bench = list(set(b["task"] for b in st.session_state.benchmarks))
            for task in tasks_bench:
                task_data = [b for b in st.session_state.benchmarks if b["task"] == task]
                fig_bench.add_trace(go.Bar(
                    name=task, x=[b["model"] for b in task_data], y=[b["rt"] for b in task_data],
                    text=[f"{b['rt']}s" for b in task_data], textposition='auto',
                ))
            fig_bench.update_layout(
                title=dict(text="Benchmark: Response Times by Task", font=dict(color="#ff6b35", size=13, family="Cinzel")),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#c8917a"),
                xaxis=dict(gridcolor="rgba(0,0,0,0)", color="#c8917a"),
                yaxis=dict(gridcolor="#2a1015", color="#c8917a", title="RT (s)"),
                barmode='group', legend=dict(font=dict(color="#c8917a"), bgcolor="rgba(0,0,0,0)"),
                margin=dict(t=40, b=40, l=40, r=20),
            )
            st.plotly_chart(fig_bench, use_container_width=True)

        if st.button("🗑 Clear Benchmarks", use_container_width=True):
            st.session_state.benchmarks = []
            st.rerun()
    else:
        st.markdown('<div style="text-align:center;padding:2rem;color:#4a2a22;font-family:\'JetBrains Mono\',monospace;"><div style="font-size:2.5rem;margin-bottom:1rem;">⚡</div><div>Run a benchmark above to see results here</div></div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
# TAB 8: FLASHCARDS
# ══════════════════════════════════════════════════════════════════
with tab_flash:
    st.markdown('<div style="font-family:\'Cinzel\',serif;font-size:1rem;font-weight:700;background:linear-gradient(135deg,#ff6b35,#f7c948);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;letter-spacing:2px;margin-bottom:0.3rem;">🎯 AI FLASHCARD GENERATOR</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.78rem;color:#4a2a22;font-family:\'JetBrains Mono\',monospace;margin-bottom:12px;">Generate stunning AI-powered flashcards · track your study progress · explore with charts</div>', unsafe_allow_html=True)

    col_fc1, col_fc2, col_fc3 = st.columns([2, 2, 2])
    with col_fc1:
        flash_category = st.selectbox("Category", list(FLASHCARD_TOPICS.keys()), key="flash_cat")
    with col_fc2:
        flash_topic = st.selectbox("Topic", FLASHCARD_TOPICS[flash_category], key="flash_topic")
    with col_fc3:
        custom_flash = st.text_input("Custom topic (overrides above)", placeholder="e.g. React hooks, Kubernetes…", key="custom_flash")

    final_topic = custom_flash.strip() if custom_flash.strip() else flash_topic

    if "last_flashcard" not in st.session_state:
        st.session_state.last_flashcard = None

    if st.button(f"🔥 Generate Flashcard: {final_topic}", use_container_width=True, key="gen_flash_btn"):
        if not active_api_key:
            st.error("⚠ No API key configured in the sidebar.")
        else:
            with st.spinner(f"🔥 Crafting flashcard for: {final_topic}…"):
                try:
                    prompt = f"""Create an educational flashcard for the topic: "{final_topic}"

Respond EXACTLY in this format (no extra text before or after):
FRONT: [A sharp, testable question about the topic]
BACK: [A thorough answer in 3-5 sentences — be specific and informative]
EXAMPLE: [A concrete code snippet or real-world example — be specific]
KEY_POINT: [The single most critical thing to remember, in one sentence]
DIFFICULTY: [Easy / Medium / Hard]
CATEGORY: [{flash_category}]"""

                    response = call_ai(
                        provider, model_sel,
                        [{"role": "user", "content": prompt}],
                        "You are an expert educator and technical writer. Create precise, informative flashcards. Always follow the exact format with FRONT:, BACK:, EXAMPLE:, KEY_POINT:, DIFFICULTY:, CATEGORY: labels.",
                        0.5, 900, active_api_key
                    )

                    parsed = {}
                    current_key = None
                    for line in response.strip().split('\n'):
                        matched = False
                        for key in ["FRONT:", "BACK:", "EXAMPLE:", "KEY_POINT:", "DIFFICULTY:", "CATEGORY:"]:
                            if line.strip().upper().startswith(key):
                                current_key = key.replace(":", "").lower()
                                parsed[current_key] = line.strip()[len(key):].strip()
                                matched = True
                                break
                        if not matched and current_key and line.strip():
                            parsed[current_key] = parsed.get(current_key, "") + " " + line.strip()

                    front      = parsed.get("front",      f"What is {final_topic}?")
                    back       = parsed.get("back",       response[:500])
                    example    = parsed.get("example",    "")
                    key_point  = parsed.get("key_point",  "")
                    difficulty = parsed.get("difficulty", "Medium").strip()
                    category   = parsed.get("category",  flash_category)

                    fc_entry = {
                        "topic":      final_topic,
                        "category":   flash_category,
                        "front":      front,
                        "back":       back,
                        "example":    example,
                        "key_point":  key_point,
                        "difficulty": difficulty,
                        "timestamp":  datetime.now().strftime("%H:%M"),
                        "date":       datetime.now().strftime("%d/%m"),
                    }
                    st.session_state.flashcard_history.append(fc_entry)
                    st.session_state.flashcard_log.append({
                        "time":       datetime.now().strftime("%H:%M"),
                        "topic":      final_topic,
                        "category":   flash_category,
                        "difficulty": difficulty,
                    })
                    st.session_state.flashcard_idx += 1
                    st.session_state.last_flashcard = fc_entry

                except Exception as e:
                    st.error(f"⚠ Flashcard generation failed: {str(e)}")
                    st.session_state.last_flashcard = None

    fc = st.session_state.last_flashcard
    if fc:
        diff_color = {"Easy": "#52b788", "Medium": "#f7c948", "Hard": "#e63946"}.get(fc.get("difficulty","Medium"), "#c8917a")
        cat_icons  = {"Python":"🐍","JavaScript":"🌐","ML Concepts":"🧠","System Design":"🏗️","Security":"🔐"}
        cat_icon   = cat_icons.get(fc["category"], "🎯")

        st.markdown(f"""
        <div style="
            background: linear-gradient(145deg, #120608 0%, #0d0406 50%, #060203 100%);
            border: 1px solid #ff6b3530;
            border-radius: 20px;
            padding: 0;
            margin: 16px 0;
            position: relative;
            overflow: hidden;
            box-shadow: 0 8px 40px rgba(255,107,53,0.12), 0 2px 8px rgba(0,0,0,0.4);
        ">
            <div style="height:4px;background:linear-gradient(90deg,#e63946,#ff6b35,#f7c948,#52b788,#74c0fc,#c084fc);border-radius:20px 20px 0 0;"></div>
            <div style="
                padding: 16px 24px 12px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-bottom: 1px solid #2a1015;
                background: linear-gradient(90deg,#1d0b0e22,transparent);
            ">
                <div style="display:flex;align-items:center;gap:10px;">
                    <div style="font-size:1.6rem;">{cat_icon}</div>
                    <div>
                        <div style="font-family:'Cinzel',serif;font-size:0.65rem;color:#4a2a22;letter-spacing:3px;text-transform:uppercase;">Flashcard</div>
                        <div style="font-family:'Cinzel',serif;font-size:0.95rem;color:#ff6b35;font-weight:700;letter-spacing:1px;">{fc["topic"]}</div>
                    </div>
                </div>
                <div style="display:flex;gap:8px;align-items:center;">
                    <span style="font-size:0.65rem;padding:4px 12px;border-radius:20px;background:{diff_color}18;color:{diff_color};border:1px solid {diff_color}44;font-family:'JetBrains Mono',monospace;font-weight:700;">{fc.get("difficulty","Medium").upper()}</span>
                    <span style="font-size:0.65rem;padding:4px 12px;border-radius:20px;background:#c084fc18;color:#c084fc;border:1px solid #c084fc44;font-family:'JetBrains Mono',monospace;">{fc["category"]}</span>
                    <span style="font-size:0.65rem;padding:4px 10px;border-radius:20px;background:#2a1015;color:#4a2a22;font-family:'JetBrains Mono',monospace;">{fc["timestamp"]}</span>
                </div>
            </div>
            <div style="padding:20px 24px;display:grid;grid-template-columns:1fr 1fr;gap:16px;">
                <div style="background:linear-gradient(135deg,#1d0b0e,#120608);border:1px solid #ff6b3530;border-top:3px solid #ff6b35;border-radius:14px;padding:18px;position:relative;">
                    <div style="font-family:'JetBrains Mono',monospace;font-size:0.6rem;color:#ff6b35;letter-spacing:2px;margin-bottom:10px;display:flex;align-items:center;gap:6px;"><span style="display:inline-block;width:6px;height:6px;border-radius:50%;background:#ff6b35;box-shadow:0 0 6px #ff6b35;"></span>QUESTION</div>
                    <div style="font-family:'Crimson Pro',serif;font-size:1.1rem;color:#fdf0e8;line-height:1.65;font-weight:600;">{fc["front"]}</div>
                </div>
                <div style="background:linear-gradient(135deg,#051a10,#060e08);border:1px solid #52b78830;border-top:3px solid #52b788;border-radius:14px;padding:18px;">
                    <div style="font-family:'JetBrains Mono',monospace;font-size:0.6rem;color:#52b788;letter-spacing:2px;margin-bottom:10px;display:flex;align-items:center;gap:6px;"><span style="display:inline-block;width:6px;height:6px;border-radius:50%;background:#52b788;box-shadow:0 0 6px #52b788;"></span>ANSWER</div>
                    <div style="font-family:'Crimson Pro',serif;font-size:0.97rem;color:#d4f0e4;line-height:1.75;">{fc["back"]}</div>
                </div>
            </div>
            <div style="padding:0 24px 20px;display:grid;grid-template-columns:1fr 1fr;gap:16px;">
                <div style="background:linear-gradient(135deg,#07111a,#050d14);border:1px solid #74c0fc30;border-top:3px solid #74c0fc;border-radius:14px;padding:16px;">
                    <div style="font-family:'JetBrains Mono',monospace;font-size:0.6rem;color:#74c0fc;letter-spacing:2px;margin-bottom:10px;display:flex;align-items:center;gap:6px;"><span style="display:inline-block;width:6px;height:6px;border-radius:50%;background:#74c0fc;box-shadow:0 0 6px #74c0fc;"></span>EXAMPLE</div>
                    <div style="font-family:'JetBrains Mono',monospace;font-size:0.82rem;color:#bde0f5;line-height:1.65;white-space:pre-wrap;">{fc.get("example","No example provided.") or "No example provided."}</div>
                </div>
                <div style="background:linear-gradient(135deg,#1a1205,#120e04);border:1px solid #f7c94830;border-top:3px solid #f7c948;border-radius:14px;padding:16px;">
                    <div style="font-family:'JetBrains Mono',monospace;font-size:0.6rem;color:#f7c948;letter-spacing:2px;margin-bottom:10px;display:flex;align-items:center;gap:6px;"><span style="display:inline-block;width:6px;height:6px;border-radius:50%;background:#f7c948;box-shadow:0 0 6px #f7c948;"></span>⭐ KEY POINT</div>
                    <div style="font-family:'Crimson Pro',serif;font-size:1rem;color:#fdf0c8;line-height:1.65;font-weight:600;font-style:italic;">{fc.get("key_point","Remember the core concept!") or "Remember the core concept!"}</div>
                </div>
            </div>
            <div style="height:2px;background:linear-gradient(90deg,transparent,#ff6b3530,transparent);"></div>
        </div>
        """, unsafe_allow_html=True)

        col_a1, col_a2, col_a3 = st.columns(3)
        with col_a1:
            if st.button(f"💬 Ask Phoenix: Explain '{fc['topic']}' deeper", use_container_width=True, key="flash_explain_btn"):
                st.session_state._pending_prompt = (
                    f"Give me a thorough, detailed explanation of: **{fc['topic']}**.\n\n"
                    f"Cover:\n1. Core concept and how it works\n2. Why it matters\n3. Common mistakes or misconceptions\n"
                    f"4. Practical real-world use cases\n5. Best practices and tips\n\nBe specific and use examples."
                )
                st.rerun()
        with col_a2:
            if st.button("🔄 Generate Another on Same Topic", use_container_width=True, key="flash_again_btn"):
                st.session_state.last_flashcard = None
                st.rerun()
        with col_a3:
            if st.button("📥 Save to Notes", use_container_width=True, key="flash_save_note_btn"):
                note_text = f"**{fc['topic']}**\n\nQ: {fc['front']}\n\nA: {fc['back']}\n\nExample: {fc.get('example','')}\n\nKey Point: {fc.get('key_point','')}"
                st.session_state.notes.append({
                    "title": f"Flashcard: {fc['topic']}",
                    "content": note_text,
                    "tag": "💡 Idea",
                    "created": datetime.now().strftime("%H:%M %d/%m"),
                })
                st.success("✅ Saved to Notes tab!")

    st.divider()
    st.markdown('<div style="font-family:\'Cinzel\',serif;font-size:0.85rem;font-weight:700;background:linear-gradient(135deg,#ff6b35,#f7c948);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;letter-spacing:2px;margin-bottom:1rem;">📊 STUDY TRACKER & ANALYTICS</div>', unsafe_allow_html=True)

    fh = st.session_state.flashcard_history

    dur_mins = (datetime.now() - datetime.fromisoformat(st.session_state.session_start)).seconds // 60
    unique_topics    = list(set(f["topic"] for f in fh))
    unique_cats      = list(set(f["category"] for f in fh))
    easy_count       = sum(1 for f in fh if f.get("difficulty") == "Easy")
    medium_count     = sum(1 for f in fh if f.get("difficulty") == "Medium")
    hard_count       = sum(1 for f in fh if f.get("difficulty") == "Hard")

    mc1, mc2, mc3, mc4, mc5 = st.columns(5)
    mc1.metric("📚 Topics Studied",    len(unique_topics))
    mc2.metric("🎯 Cards Generated",   st.session_state.flashcard_idx)
    mc3.metric("🗂️ Categories",        len(unique_cats))
    mc4.metric("⏱️ Study Time",        f"{dur_mins}m")
    mc5.metric("🔥 Streak",            f"{st.session_state.flashcard_idx} cards")

    if not fh:
        st.markdown("""
        <div style="text-align:center;padding:3rem;color:#4a2a22;font-family:'JetBrains Mono',monospace;">
            <div style="font-size:3rem;margin-bottom:1rem;animation:float 3s ease-in-out infinite;display:inline-block;">🎯</div>
            <div>Generate your first flashcard above to see study charts!</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        ch1, ch2 = st.columns(2)

        with ch1:
            cat_counts = Counter(f["category"] for f in fh)
            cat_colors = ["#ff6b35","#f7c948","#52b788","#74c0fc","#c084fc","#e63946","#ff8c42","#67e8f9"]
            fig_cat = go.Figure(go.Bar(
                x=list(cat_counts.keys()),
                y=list(cat_counts.values()),
                marker=dict(color=cat_colors[:len(cat_counts)], line=dict(color='rgba(0,0,0,0)'), opacity=0.9),
                text=list(cat_counts.values()),
                textposition='outside',
                textfont=dict(color='#fdf0e8', size=12, family="Cinzel"),
            ))
            fig_cat.update_layout(
                title=dict(text="📚 Cards by Category", font=dict(color="#ff6b35", size=13, family="Cinzel")),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#c8917a"),
                xaxis=dict(gridcolor="rgba(0,0,0,0)", color="#c8917a", tickangle=-20),
                yaxis=dict(gridcolor="#2a1015", color="#c8917a", title="Cards"),
                margin=dict(t=50, b=60, l=40, r=20), height=300,
            )
            st.plotly_chart(fig_cat, use_container_width=True)

        with ch2:
            diff_vals   = [easy_count, medium_count, hard_count]
            diff_labels = ["Easy", "Medium", "Hard"]
            diff_colors = ["#52b788", "#f7c948", "#e63946"]
            fig_diff = go.Figure(data=[go.Pie(
                labels=diff_labels,
                values=[max(v, 0) for v in diff_vals],
                hole=0.6,
                marker=dict(colors=diff_colors, line=dict(color='#060203', width=3)),
                textfont=dict(color='#fdf0e8', size=12, family="Cinzel"),
                pull=[0.05, 0.05, 0.05],
            )])
            total_cards = max(1, sum(diff_vals))
            fig_diff.update_layout(
                title=dict(text="🎯 Difficulty Distribution", font=dict(color="#ff6b35", size=13, family="Cinzel")),
                paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#c8917a"),
                legend=dict(font=dict(color="#c8917a"), bgcolor="rgba(0,0,0,0)"),
                margin=dict(t=50, b=20, l=20, r=20), height=300,
                annotations=[dict(text=f"<b>{total_cards}</b><br>total", x=0.5, y=0.5,
                    font_size=16, showarrow=False, font=dict(color="#ff6b35", family="Cinzel"))]
            )
            st.plotly_chart(fig_diff, use_container_width=True)

        ch3, ch4 = st.columns(2)

        with ch3:
            fig_time = go.Figure()
            fig_time.add_trace(go.Scatter(
                x=list(range(1, len(fh)+1)),
                y=list(range(1, len(fh)+1)),
                mode='lines+markers',
                name="Cumulative Cards",
                line=dict(color='#ff6b35', width=3),
                marker=dict(
                    color=[{"Easy":"#52b788","Medium":"#f7c948","Hard":"#e63946"}.get(f.get("difficulty","Medium"),"#c8917a") for f in fh],
                    size=12,
                    line=dict(color='#060203', width=2),
                ),
                fill='tozeroy',
                fillcolor='rgba(255,107,53,0.07)',
                text=[f["topic"] for f in fh],
                hovertemplate="Card #%{x}: %{text}<extra></extra>",
            ))
            fig_time.update_layout(
                title=dict(text="📈 Study Progress Timeline", font=dict(color="#ff6b35", size=13, family="Cinzel")),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#c8917a"),
                xaxis=dict(gridcolor="#2a1015", color="#c8917a", title="Card #"),
                yaxis=dict(gridcolor="#2a1015", color="#c8917a", title="Total Cards"),
                showlegend=False,
                margin=dict(t=50, b=40, l=40, r=20), height=300,
            )
            st.plotly_chart(fig_time, use_container_width=True)

        with ch4:
            topic_counts = Counter(f["topic"] for f in fh)
            top_topics   = topic_counts.most_common(8)
            t_names      = [t[0][:25] for t in top_topics]
            t_vals       = [t[1] for t in top_topics]
            t_colors     = ["#ff6b35","#f7c948","#52b788","#74c0fc","#c084fc","#ff8c42","#e63946","#67e8f9"]
            fig_top = go.Figure(go.Bar(
                x=t_vals, y=t_names, orientation='h',
                marker=dict(color=t_colors[:len(t_names)], line=dict(color='rgba(0,0,0,0)'), opacity=0.9),
                text=t_vals, textposition='outside',
                textfont=dict(color='#fdf0e8', size=11),
            ))
            fig_top.update_layout(
                title=dict(text="🔥 Most Studied Topics", font=dict(color="#ff6b35", size=13, family="Cinzel")),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#c8917a"),
                xaxis=dict(gridcolor="#2a1015", color="#c8917a", title="Times"),
                yaxis=dict(gridcolor="rgba(0,0,0,0)", color="#c8917a"),
                margin=dict(t=50, b=20, l=140, r=40), height=300,
            )
            st.plotly_chart(fig_top, use_container_width=True)

        ch5, ch6 = st.columns(2)

        with ch5:
            easy_running   = [1 if f.get("difficulty")=="Easy" else 0 for f in fh]
            medium_running = [1 if f.get("difficulty")=="Medium" else 0 for f in fh]
            hard_running   = [1 if f.get("difficulty")=="Hard" else 0 for f in fh]
            x_idx = list(range(1, len(fh)+1))

            fig_stack = go.Figure()
            fig_stack.add_trace(go.Bar(x=x_idx, y=easy_running, name="Easy", marker_color="#52b788", opacity=0.85))
            fig_stack.add_trace(go.Bar(x=x_idx, y=medium_running, name="Medium", marker_color="#f7c948", opacity=0.85))
            fig_stack.add_trace(go.Bar(x=x_idx, y=hard_running, name="Hard", marker_color="#e63946", opacity=0.85))
            fig_stack.update_layout(
                title=dict(text="🎲 Difficulty per Card", font=dict(color="#ff6b35", size=13, family="Cinzel")),
                barmode='stack',
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#c8917a"),
                xaxis=dict(gridcolor="#2a1015", color="#c8917a", title="Card #"),
                yaxis=dict(gridcolor="#2a1015", color="#c8917a"),
                legend=dict(font=dict(color="#c8917a"), bgcolor="rgba(0,0,0,0)"),
                margin=dict(t=50, b=40, l=40, r=20), height=280,
            )
            st.plotly_chart(fig_stack, use_container_width=True)

        with ch6:
            total = max(1, len(fh))
            categories_rad = list(FLASHCARD_TOPICS.keys())
            cat_vals_rad   = [Counter(f["category"] for f in fh).get(c, 0) / total * 100 for c in categories_rad]
            fig_rad = go.Figure(data=go.Scatterpolar(
                r=cat_vals_rad + [cat_vals_rad[0]],
                theta=categories_rad + [categories_rad[0]],
                fill='toself',
                fillcolor='rgba(255,107,53,0.12)',
                line=dict(color='#ff6b35', width=2.5),
                marker=dict(color='#f7c948', size=8),
                name="Coverage"
            ))
            fig_rad.update_layout(
                title=dict(text="🕸️ Knowledge Coverage Radar", font=dict(color="#ff6b35", size=13, family="Cinzel")),
                polar=dict(
                    bgcolor='rgba(0,0,0,0)',
                    radialaxis=dict(visible=True, range=[0,100], gridcolor='#2a1015', color='#4a2a22',
                                   tickfont=dict(size=8), ticksuffix="%"),
                    angularaxis=dict(gridcolor='#2a1015', color='#c8917a', tickfont=dict(size=10)),
                ),
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#c8917a'),
                showlegend=False,
                margin=dict(t=50, b=20, l=40, r=40), height=280,
            )
            st.plotly_chart(fig_rad, use_container_width=True)

        st.markdown('<div style="font-size:0.72rem;color:#c8917a;margin:10px 0 6px;font-family:\'JetBrains Mono\',monospace;">📋 FLASHCARD HISTORY</div>', unsafe_allow_html=True)
        hist_rows = [{"#": i+1, "Time": f["timestamp"], "Topic": f["topic"],
                      "Category": f["category"], "Difficulty": f.get("difficulty","—")}
                     for i, f in enumerate(reversed(fh[-15:]))]
        if hist_rows:
            st.dataframe(pd.DataFrame(hist_rows), use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════════
# TAB 9: SESSION HEALTH
# ══════════════════════════════════════════════════════════════════
with tab_health:
    st.markdown('<div style="font-family:\'Cinzel\',serif;font-size:1rem;font-weight:700;background:linear-gradient(135deg,#ff6b35,#f7c948);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;letter-spacing:2px;margin-bottom:1rem;">🌡️ SESSION HEALTH DASHBOARD</div>', unsafe_allow_html=True)

    valid_a = [a for a in st.session_state.analytics if a]
    session_dur_sec = (datetime.now() - datetime.fromisoformat(st.session_state.session_start)).seconds
    msg_count = len(st.session_state.messages)

    token_usage_pct  = min(100, (st.session_state.total_tokens / 50000) * 100)
    activity_score   = min(100, (msg_count / 50) * 100)
    positivity_score = (sum(1 for a in valid_a if a.get("sentiment") == "positive") / max(1, len(valid_a))) * 100
    speed_score      = 100 - min(100, ((sum(a.get("response_time",0) for a in valid_a) / max(1,len(valid_a))) / 10) * 100) if valid_a else 50
    overall_health   = (100 - token_usage_pct * 0.3 + positivity_score * 0.4 + speed_score * 0.3)
    overall_health   = max(0, min(100, overall_health))

    health_color = "#52b788" if overall_health > 70 else "#f7c948" if overall_health > 40 else "#e63946"
    fig_health = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=overall_health,
        domain={'x':[0,1],'y':[0,1]},
        title={'text':"Session Health Score", 'font':{'color':'#fdf0e8','size':14,'family':'Cinzel'}},
        number={'font':{'color':health_color,'size':40,'family':'Cinzel'},'suffix':'%'},
        delta={'reference': 70, 'font':{'color':'#c8917a'}},
        gauge={
            'axis':{'range':[0,100],'tickcolor':'#4a2a22','tickfont':{'color':'#4a2a22'}},
            'bar':{'color':health_color,'thickness':0.3},
            'bgcolor':'#2a1015','bordercolor':'#3a1a20',
            'steps':[
                {'range':[0,40],'color':'#1d0406'},
                {'range':[40,70],'color':'#0d0406'},
                {'range':[70,100],'color':'#060203'},
            ],
            'threshold':{'line':{'color':health_color,'width':3},'thickness':0.75,'value':overall_health}
        }
    ))
    fig_health.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#c8917a"),
        height=280, margin=dict(t=50, b=10, l=30, r=30),
    )

    col_hm, col_hd = st.columns([2, 1])
    with col_hm:
        st.plotly_chart(fig_health, use_container_width=True)
    with col_hd:
        dur_str = f"{session_dur_sec//60}m {session_dur_sec%60}s"
        st.markdown(f"""
        <div style="background:#0d0406;border:1px solid #2a1015;border-radius:12px;padding:18px;margin-top:20px;font-family:'JetBrains Mono',monospace;font-size:0.76rem;color:#c8917a;">
            <div style="color:#ff6b35;font-family:'Cinzel',serif;font-size:0.85rem;margin-bottom:12px;">Session Details</div>
            <div style="display:flex;justify-content:space-between;margin-bottom:8px;"><span>Duration</span><span style="color:#f7c948;">{dur_str}</span></div>
            <div style="display:flex;justify-content:space-between;margin-bottom:8px;"><span>Messages</span><span style="color:#ff6b35;">{msg_count}</span></div>
            <div style="display:flex;justify-content:space-between;margin-bottom:8px;"><span>Tokens Used</span><span style="color:#c084fc;">~{st.session_state.total_tokens:,}</span></div>
            <div style="display:flex;justify-content:space-between;margin-bottom:8px;"><span>Notes Saved</span><span style="color:#67e8f9;">{len(st.session_state.notes)}</span></div>
            <div style="display:flex;justify-content:space-between;"><span>Provider</span><span style="color:{pcolor};">{pdata['id'].upper()}</span></div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div style="font-size:0.76rem;color:#c8917a;margin:14px 0 10px;font-family:\'JetBrains Mono\',monospace;">📊 HEALTH BREAKDOWN</div>', unsafe_allow_html=True)

    health_metrics = [
        ("🪙 Token Budget", 100 - token_usage_pct, "#52b788" if token_usage_pct < 50 else "#f7c948" if token_usage_pct < 80 else "#e63946"),
        ("💬 Activity", activity_score, "#74c0fc"),
        ("☀️ Positivity", positivity_score, "#52b788" if positivity_score > 60 else "#f7c948"),
        ("⚡ Speed Score", speed_score, "#ff6b35"),
    ]

    for label, val, color in health_metrics:
        val = max(0, min(100, val))
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:10px;">
            <span style="font-size:0.72rem;color:#c8917a;min-width:140px;font-family:'JetBrains Mono',monospace;">{label}</span>
            <div style="flex:1;height:8px;background:#1d0b0e;border-radius:4px;overflow:hidden;">
                <div style="width:{val:.1f}%;height:100%;background:{color};border-radius:4px;box-shadow:0 0 8px {color};transition:width 0.5s ease;"></div>
            </div>
            <span style="font-size:0.72rem;color:{color};min-width:40px;text-align:right;font-family:'JetBrains Mono',monospace;">{val:.0f}%</span>
        </div>
        """, unsafe_allow_html=True)

    if st.session_state.mood_log:
        st.markdown('<div style="font-size:0.76rem;color:#c8917a;margin:14px 0 8px;font-family:\'JetBrains Mono\',monospace;">😊 CONVERSATION MOOD FLOW</div>', unsafe_allow_html=True)
        ml = st.session_state.mood_log
        sent_map2 = {"positive": 1, "neutral": 0, "negative": -1}
        y_mood = [sent_map2.get(m["sentiment"], 0) for m in ml]
        x_mood = list(range(1, len(ml)+1))
        colors_mood = ["#52b788" if v > 0 else "#e63946" if v < 0 else "#c8917a" for v in y_mood]

        fig_mood = go.Figure()
        fig_mood.add_trace(go.Bar(x=x_mood, y=y_mood, name="Mood",
            marker=dict(color=colors_mood, line=dict(color='rgba(0,0,0,0)'))))
        fig_mood.add_trace(go.Scatter(x=x_mood, y=y_mood, mode='lines', name="Trend",
            line=dict(color='#f7c948', width=2, dash='dot')))
        fig_mood.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#c8917a"),
            xaxis=dict(gridcolor="#2a1015", color="#c8917a", title="Response #"),
            yaxis=dict(gridcolor="#2a1015", color="#c8917a",
                tickvals=[-1,0,1], ticktext=["Neg","Neu","Pos"]),
            showlegend=True, legend=dict(font=dict(color="#c8917a"), bgcolor="rgba(0,0,0,0)"),
            margin=dict(t=20, b=40, l=40, r=20), height=250,
        )
        st.plotly_chart(fig_mood, use_container_width=True)

    st.divider()
    st.markdown('<div style="font-size:0.76rem;color:#c8917a;margin-bottom:8px;font-family:\'JetBrains Mono\',monospace;">💡 SESSION TIPS</div>', unsafe_allow_html=True)
    tips = []
    if token_usage_pct > 70: tips.append(("⚠", "You've used a lot of your token budget. Consider starting a new session.", "#f7c948"))
    if activity_score < 20: tips.append(("💬", "Your session is just getting started! Ask more questions.", "#74c0fc"))
    if positivity_score < 40 and valid_a: tips.append(("☀️", "Responses seem neutral/negative. Try rephrasing questions for better results.", "#ff8c42"))
    if not tips: tips.append(("✅", "Your session looks healthy! Keep exploring.", "#52b788"))

    for icon, tip, color in tips:
        st.markdown(f'<div style="background:{color}0a;border:1px solid {color}22;border-radius:8px;padding:10px 14px;margin-bottom:8px;font-size:0.82rem;color:{color};font-family:\'Crimson Pro\',serif;">{icon} {tip}</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
# TAB 10: MODEL COMPARISONS  ← NEW TAB
# ══════════════════════════════════════════════════════════════════
with tab_modelcomp:
    st.markdown('<div style="font-family:\'Cinzel\',serif;font-size:1rem;font-weight:700;background:linear-gradient(135deg,#ff6b35,#f7c948);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;letter-spacing:2px;margin-bottom:0.3rem;">🆚 MODEL COMPARISONS & AI ANALYSIS</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.78rem;color:#4a2a22;font-family:\'JetBrains Mono\',monospace;margin-bottom:14px;">Live stats auto-update as you chat across different models · switch models in sidebar to add data</div>', unsafe_allow_html=True)

    ms_data = st.session_state.model_stats

    if not ms_data:
        st.markdown("""
        <div style="text-align:center;padding:4rem;color:#4a2a22;font-family:'JetBrains Mono',monospace;">
            <div style="font-size:4rem;margin-bottom:1rem;animation:float 3s ease-in-out infinite;display:inline-block;">🆚</div>
            <div style="font-size:0.9rem;margin-bottom:8px;">No model data yet</div>
            <div style="font-size:0.75rem;color:#3a1a18;">Chat with at least one model to see comparison data.<br>Switch between models in the sidebar to compare multiple.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # ── Build summary table ──
        model_rows = []
        for mkey, ms in ms_data.items():
            calls      = ms["calls"]
            avg_rt     = ms["total_rt"] / max(1, calls)
            avg_tokens = ms["total_tokens"] / max(1, calls)
            avg_chars  = ms["total_chars"] / max(1, calls)
            avg_cps    = avg_chars / max(0.001, avg_rt)
            pos_rate   = ms["sentiments"].count("positive") / max(1, len(ms["sentiments"]))
            min_rt     = min(ms["response_times"]) if ms["response_times"] else 0
            max_rt     = max(ms["response_times"]) if ms["response_times"] else 0
            model_rows.append({
                "mkey": mkey,
                "provider": ms["provider_label"],
                "model": ms["model"],
                "color": ms["color"],
                "calls": calls,
                "avg_rt": avg_rt,
                "avg_tokens": avg_tokens,
                "avg_chars": avg_chars,
                "avg_cps": avg_cps,
                "pos_rate": pos_rate,
                "min_rt": min_rt,
                "max_rt": max_rt,
                "total_tokens": ms["total_tokens"],
            })

        model_rows.sort(key=lambda x: x["avg_rt"])

        # ── Top-level scorecards ──
        st.markdown('<div style="font-size:0.72rem;color:#ff6b35;font-family:\'JetBrains Mono\',monospace;letter-spacing:2px;margin-bottom:10px;">🏆 LEADERBOARD</div>', unsafe_allow_html=True)

        leader_cols = st.columns(min(4, len(model_rows)))
        medals = ["🥇", "🥈", "🥉", "🏅"]
        for i, row in enumerate(model_rows[:4]):
            with leader_cols[i]:
                speed_label = "Fastest" if i == 0 else f"#{i+1} Speed"
                st.markdown(f"""
                <div style="background:linear-gradient(135deg,#0d0406,#060203);border:1px solid {row['color']}33;
                    border-top:3px solid {row['color']};border-radius:12px;padding:14px;text-align:center;margin-bottom:8px;">
                    <div style="font-size:1.8rem;margin-bottom:4px;">{medals[i]}</div>
                    <div style="font-family:'Cinzel',serif;font-size:0.7rem;color:{row['color']};letter-spacing:1px;font-weight:700;">{speed_label}</div>
                    <div style="font-family:'JetBrains Mono',monospace;font-size:0.72rem;color:#c8917a;margin:4px 0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;" title="{row['model']}">{row['model'][:22]}</div>
                    <div style="font-size:0.65rem;color:#4a2a22;font-family:'JetBrains Mono',monospace;">{row['provider'].split()[0]}</div>
                    <div style="font-family:'Cinzel',serif;font-size:1.3rem;color:{row['color']};font-weight:700;margin-top:6px;">{row['avg_rt']:.2f}s</div>
                    <div style="font-size:0.62rem;color:#4a2a22;font-family:'JetBrains Mono',monospace;">avg response time</div>
                    <div style="display:flex;justify-content:center;gap:8px;margin-top:8px;flex-wrap:wrap;">
                        <span style="font-size:0.6rem;padding:2px 8px;border-radius:10px;background:{row['color']}10;color:{row['color']};border:1px solid {row['color']}22;">{row['calls']} calls</span>
                        <span style="font-size:0.6rem;padding:2px 8px;border-radius:10px;background:#f7c94810;color:#f7c948;border:1px solid #f7c94822;">{row['avg_cps']:.0f} c/s</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── ROW 1: Response Time Bar + Token Usage Bar ──
        rc1, rc2 = st.columns(2)

        with rc1:
            model_names = [r["model"][:25] for r in model_rows]
            avg_rts     = [r["avg_rt"] for r in model_rows]
            colors_bar  = [r["color"] for r in model_rows]

            fig_rt = go.Figure(go.Bar(
                x=avg_rts,
                y=model_names,
                orientation='h',
                marker=dict(
                    color=colors_bar,
                    line=dict(color='rgba(0,0,0,0)'),
                    opacity=0.9,
                ),
                text=[f"{v:.2f}s" for v in avg_rts],
                textposition='outside',
                textfont=dict(color='#fdf0e8', size=11),
            ))
            fig_rt.update_layout(
                title=dict(text="⏱ Avg Response Time (lower = faster)", font=dict(color="#ff6b35", size=13, family="Cinzel")),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#c8917a"),
                xaxis=dict(gridcolor="#2a1015", color="#c8917a", title="seconds"),
                yaxis=dict(gridcolor="rgba(0,0,0,0)", color="#c8917a"),
                margin=dict(t=50, b=30, l=10, r=60), height=max(200, len(model_rows)*55),
            )
            st.plotly_chart(fig_rt, use_container_width=True)

        with rc2:
            avg_toks = [r["avg_tokens"] for r in model_rows]
            fig_tok = go.Figure(go.Bar(
                x=avg_toks,
                y=model_names,
                orientation='h',
                marker=dict(
                    color=colors_bar,
                    line=dict(color='rgba(0,0,0,0)'),
                    opacity=0.85,
                ),
                text=[f"~{int(v)}" for v in avg_toks],
                textposition='outside',
                textfont=dict(color='#fdf0e8', size=11),
            ))
            fig_tok.update_layout(
                title=dict(text="⚡ Avg Tokens per Response", font=dict(color="#ff6b35", size=13, family="Cinzel")),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#c8917a"),
                xaxis=dict(gridcolor="#2a1015", color="#c8917a", title="tokens"),
                yaxis=dict(gridcolor="rgba(0,0,0,0)", color="#c8917a"),
                margin=dict(t=50, b=30, l=10, r=60), height=max(200, len(model_rows)*55),
            )
            st.plotly_chart(fig_tok, use_container_width=True)

        # ── ROW 2: Speed (c/s) Bar + Positivity Bar ──
        rc3, rc4 = st.columns(2)

        with rc3:
            avg_cps_vals = [r["avg_cps"] for r in model_rows]
            fig_cps = go.Figure(go.Bar(
                x=avg_cps_vals,
                y=model_names,
                orientation='h',
                marker=dict(
                    color=avg_cps_vals,
                    colorscale=[[0,"#e63946"],[0.4,"#f7c948"],[0.7,"#52b788"],[1,"#67e8f9"]],
                    showscale=True,
                    colorbar=dict(tickfont=dict(color="#c8917a"), title=dict(text="c/s", font=dict(color="#c8917a"))),
                    line=dict(color='rgba(0,0,0,0)'),
                ),
                text=[f"{int(v)} c/s" for v in avg_cps_vals],
                textposition='outside',
                textfont=dict(color='#fdf0e8', size=11),
            ))
            fig_cps.update_layout(
                title=dict(text="🚀 Characters per Second (higher = faster output)", font=dict(color="#ff6b35", size=13, family="Cinzel")),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#c8917a"),
                xaxis=dict(gridcolor="#2a1015", color="#c8917a", title="chars/sec"),
                yaxis=dict(gridcolor="rgba(0,0,0,0)", color="#c8917a"),
                margin=dict(t=50, b=30, l=10, r=80), height=max(200, len(model_rows)*55),
            )
            st.plotly_chart(fig_cps, use_container_width=True)

        with rc4:
            pos_rates = [r["pos_rate"] * 100 for r in model_rows]
            pos_colors_bar = ["#52b788" if v >= 60 else "#f7c948" if v >= 40 else "#e63946" for v in pos_rates]
            fig_pos = go.Figure(go.Bar(
                x=pos_rates,
                y=model_names,
                orientation='h',
                marker=dict(color=pos_colors_bar, line=dict(color='rgba(0,0,0,0)'), opacity=0.9),
                text=[f"{v:.0f}%" for v in pos_rates],
                textposition='outside',
                textfont=dict(color='#fdf0e8', size=11),
            ))
            fig_pos.update_layout(
                title=dict(text="☀️ Positive Sentiment Rate", font=dict(color="#ff6b35", size=13, family="Cinzel")),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#c8917a"),
                xaxis=dict(gridcolor="#2a1015", color="#c8917a", title="%", range=[0, 110]),
                yaxis=dict(gridcolor="rgba(0,0,0,0)", color="#c8917a"),
                margin=dict(t=50, b=30, l=10, r=60), height=max(200, len(model_rows)*55),
            )
            st.plotly_chart(fig_pos, use_container_width=True)

        # ── ROW 3: Multi-metric Radar + Provider Pie ──
        rc5, rc6 = st.columns(2)

        with rc5:
            # Radar: normalize each metric 0-100 across models
            if len(model_rows) >= 1:
                radar_cats = ["Speed", "Output Volume", "Positivity", "Consistency", "Efficiency"]
                max_cps    = max(r["avg_cps"] for r in model_rows) or 1
                max_chars  = max(r["avg_chars"] for r in model_rows) or 1
                min_rt_all = min(r["avg_rt"] for r in model_rows) or 0.001

                fig_radar = go.Figure()
                for row in model_rows:
                    rt_range = (row["max_rt"] - row["min_rt"]) if len(ms_data[row["mkey"]]["response_times"]) > 1 else 0
                    consistency = max(0, 100 - (rt_range / max(row["avg_rt"], 0.001)) * 100)
                    vals = [
                        min(100, (row["avg_cps"] / max_cps) * 100),
                        min(100, (row["avg_chars"] / max_chars) * 100),
                        row["pos_rate"] * 100,
                        consistency,
                        min(100, (row["avg_tokens"] / max(r["avg_tokens"] for r in model_rows)) * 100),
                    ]
                    fig_radar.add_trace(go.Scatterpolar(
                        r=vals + [vals[0]],
                        theta=radar_cats + [radar_cats[0]],
                        fill='toself',
                        fillcolor = "rgba(0, 123, 255, 0.2)",
                        line=dict(color=row['color'], width=2),
                        marker=dict(color=row['color'], size=6),
                        name=row['model'][:20],
                    ))
                fig_radar.update_layout(
                    title=dict(text="🕸️ Multi-Model Radar Comparison", font=dict(color="#ff6b35", size=13, family="Cinzel")),
                    polar=dict(
                        bgcolor='rgba(0,0,0,0)',
                        radialaxis=dict(visible=True, range=[0,100], gridcolor='#2a1015', color='#4a2a22',
                                       tickfont=dict(size=8), ticksuffix="%"),
                        angularaxis=dict(gridcolor='#2a1015', color='#c8917a', tickfont=dict(size=10)),
                    ),
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#c8917a'),
                    legend=dict(font=dict(color="#c8917a"), bgcolor="rgba(0,0,0,0)"),
                    margin=dict(t=50, b=20, l=40, r=40), height=360,
                )
                st.plotly_chart(fig_radar, use_container_width=True)

        with rc6:
            # Total tokens per model (pie)
            tok_labels = [r["model"][:20] for r in model_rows]
            tok_vals2  = [r["total_tokens"] for r in model_rows]
            tok_colors2= [r["color"] for r in model_rows]
            fig_tok_pie = go.Figure(data=[go.Pie(
                labels=tok_labels, values=tok_vals2, hole=0.55,
                marker=dict(colors=tok_colors2, line=dict(color='#060203', width=2)),
                textfont=dict(color='#fdf0e8', size=11),
            )])
            fig_tok_pie.update_layout(
                title=dict(text="🪙 Total Tokens Used per Model", font=dict(color="#ff6b35", size=13, family="Cinzel")),
                paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#c8917a"),
                legend=dict(font=dict(color="#c8917a"), bgcolor="rgba(0,0,0,0)"),
                margin=dict(t=50, b=20, l=20, r=20), height=360,
                annotations=[dict(
                    text=f"<b>{sum(tok_vals2):,}</b><br>total",
                    x=0.5, y=0.5, font_size=14, showarrow=False,
                    font=dict(color="#f7c948", family="Cinzel")
                )]
            )
            st.plotly_chart(fig_tok_pie, use_container_width=True)

        # ── ROW 4: Response time box plot (per model) ──
        if any(len(ms_data[r["mkey"]]["response_times"]) > 1 for r in model_rows):
            st.markdown('<div style="font-size:0.76rem;color:#c8917a;margin:10px 0 6px;font-family:\'JetBrains Mono\',monospace;">📦 RESPONSE TIME DISTRIBUTION PER MODEL</div>', unsafe_allow_html=True)
            fig_box = go.Figure()
            for row in model_rows:
                rts = ms_data[row["mkey"]]["response_times"]
                if rts:
                     color = row["color"]
                     fill_color = hex_to_rgba(color, 0.15)
                     fig_box.add_trace(go.Box(
                         y=rts,
                         name=row["model"][:20],
                         marker_color=row["color"],
                         line_color=row["color"],
                         fillcolor=fill_color,
                         boxmean=True,
                    ))
            fig_box.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#c8917a"),
                yaxis=dict(gridcolor="#2a1015", color="#c8917a", title="Response Time (s)"),
                xaxis=dict(gridcolor="rgba(0,0,0,0)", color="#c8917a"),
                legend=dict(font=dict(color="#c8917a"), bgcolor="rgba(0,0,0,0)"),
                margin=dict(t=20, b=30, l=40, r=20), height=300,
            )
            st.plotly_chart(fig_box, use_container_width=True)

        # ── ROW 5: Call count + cumulative tokens line ──
        rc7, rc8 = st.columns(2)

        with rc7:
            call_counts = [r["calls"] for r in model_rows]
            fig_calls = go.Figure(go.Bar(
                x=[r["model"][:20] for r in model_rows],
                y=call_counts,
                marker=dict(
                    color=call_counts,
                    colorscale=[[0,"#2a1015"],[0.4,"#ff6b35"],[1,"#f7c948"]],
                    line=dict(color='rgba(0,0,0,0)'),
                ),
                text=call_counts,
                textposition='outside',
                textfont=dict(color='#fdf0e8', size=12),
            ))
            fig_calls.update_layout(
                title=dict(text="💬 Total API Calls per Model", font=dict(color="#ff6b35", size=13, family="Cinzel")),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#c8917a"),
                xaxis=dict(gridcolor="rgba(0,0,0,0)", color="#c8917a", tickangle=-20),
                yaxis=dict(gridcolor="#2a1015", color="#c8917a", title="calls"),
                margin=dict(t=50, b=60, l=40, r=20), height=280,
            )
            st.plotly_chart(fig_calls, use_container_width=True)

        with rc8:
            # Scatter: avg_rt vs avg_cps (bubble = total tokens)
            if len(model_rows) >= 1:
                bubble_sizes = [max(10, r["total_tokens"] / 5) for r in model_rows]
                fig_scatter = go.Figure(go.Scatter(
                    x=[r["avg_rt"] for r in model_rows],
                    y=[r["avg_cps"] for r in model_rows],
                    mode='markers+text',
                    marker=dict(
                        size=bubble_sizes,
                        color=[r["color"] for r in model_rows],
                        line=dict(color='#060203', width=2),
                        opacity=0.85,
                        sizemode='diameter',
                        sizeref=max(bubble_sizes)/40,
                    ),
                    text=[r["model"][:15] for r in model_rows],
                    textposition='top center',
                    textfont=dict(color='#c8917a', size=10),
                    hovertemplate="<b>%{text}</b><br>Avg RT: %{x:.2f}s<br>Speed: %{y:.0f} c/s<extra></extra>",
                ))
                fig_scatter.update_layout(
                    title=dict(text="🔴 Speed vs Latency (bubble = total tokens)", font=dict(color="#ff6b35", size=13, family="Cinzel")),
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#c8917a"),
                    xaxis=dict(gridcolor="#2a1015", color="#c8917a", title="Avg Response Time (s) →"),
                    yaxis=dict(gridcolor="#2a1015", color="#c8917a", title="Chars / Second ↑"),
                    margin=dict(t=50, b=50, l=60, r=20), height=280,
                )
                st.plotly_chart(fig_scatter, use_container_width=True)

        # ── Detailed Table ──
        st.markdown('<div style="font-size:0.76rem;color:#c8917a;margin:14px 0 8px;font-family:\'JetBrains Mono\',monospace;">📋 DETAILED MODEL STATS TABLE</div>', unsafe_allow_html=True)
        table_rows = []
        for row in model_rows:
            table_rows.append({
                "Model": row["model"],
                "Provider": row["provider"].split()[0] if row["provider"] else "—",
                "Calls": row["calls"],
                "Avg RT (s)": f"{row['avg_rt']:.2f}",
                "Min RT (s)": f"{row['min_rt']:.2f}",
                "Max RT (s)": f"{row['max_rt']:.2f}",
                "Avg Tokens": f"~{int(row['avg_tokens'])}",
                "Total Tokens": f"~{int(row['total_tokens'])}",
                "Avg Speed (c/s)": f"{row['avg_cps']:.0f}",
                "Avg Chars": f"{int(row['avg_chars'])}",
                "Positivity": f"{row['pos_rate']:.0%}",
            })
        if table_rows:
            st.dataframe(pd.DataFrame(table_rows), use_container_width=True, hide_index=True)

        # ── AI Recommendations ──
        st.divider()
        st.markdown('<div style="font-family:\'Cinzel\',serif;font-size:0.85rem;font-weight:700;background:linear-gradient(135deg,#ff6b35,#f7c948);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;letter-spacing:2px;margin-bottom:10px;">💡 AI-POWERED RECOMMENDATIONS</div>', unsafe_allow_html=True)

        if model_rows:
            fastest     = min(model_rows, key=lambda x: x["avg_rt"])
            most_tokens = max(model_rows, key=lambda x: x["avg_tokens"])
            highest_cps = max(model_rows, key=lambda x: x["avg_cps"])
            most_positive = max(model_rows, key=lambda x: x["pos_rate"])
            most_calls  = max(model_rows, key=lambda x: x["calls"])

            recs = [
                (fastest["color"],       "⚡ Fastest Response",     fastest["model"],        f"{fastest['avg_rt']:.2f}s avg",           "Best for real-time, latency-sensitive applications"),
                (highest_cps["color"],   "🚀 Highest Throughput",   highest_cps["model"],    f"{highest_cps['avg_cps']:.0f} chars/sec",  "Best for long-form content generation"),
                (most_tokens["color"],   "📝 Most Verbose",         most_tokens["model"],    f"~{int(most_tokens['avg_tokens'])} tokens", "Best for detailed explanations and research"),
                (most_positive["color"], "☀️ Most Positive Tone",   most_positive["model"],  f"{most_positive['pos_rate']:.0%} positive", "Best for customer-facing and creative tasks"),
                (most_calls["color"],    "🏆 Most Used This Session", most_calls["model"],   f"{most_calls['calls']} calls",              "Your go-to model for this session"),
            ]

            rec_cols = st.columns(min(3, len(recs)))
            for i, (color, title, model_name, stat, desc) in enumerate(recs):
                with rec_cols[i % len(rec_cols)]:
                    st.markdown(f"""
                    <div style="background:linear-gradient(135deg,#0d0406,#060203);border:1px solid {color}33;
                        border-left:3px solid {color};border-radius:12px;padding:14px;margin-bottom:10px;">
                        <div style="font-size:0.65rem;color:{color};font-family:'JetBrains Mono',monospace;letter-spacing:2px;margin-bottom:6px;">{title}</div>
                        <div style="font-family:'Cinzel',serif;font-size:0.85rem;color:#fdf0e8;font-weight:700;margin-bottom:4px;">{model_name[:28]}</div>
                        <div style="font-size:0.72rem;color:{color};font-family:'JetBrains Mono',monospace;margin-bottom:6px;">{stat}</div>
                        <div style="font-size:0.78rem;color:#c8917a;font-family:'Crimson Pro',serif;line-height:1.5;">{desc}</div>
                    </div>
                    """, unsafe_allow_html=True)

            # ── Use-case matrix ──
            st.markdown('<div style="font-size:0.76rem;color:#c8917a;margin:14px 0 8px;font-family:\'JetBrains Mono\',monospace;">🗺️ USE-CASE BEST-FIT MATRIX</div>', unsafe_allow_html=True)
            use_cases = ["Real-time Chat", "Long Documents", "Code Generation", "Creative Writing", "Data Analysis", "Customer Support"]

            # Score each model per use-case using weighted formula
            matrix_data = []
            for uc in use_cases:
                row_uc = {"Use Case": uc}
                for mr in model_rows:
                    if uc == "Real-time Chat":
                        score = max(0, 100 - mr["avg_rt"] * 20)
                    elif uc == "Long Documents":
                        score = min(100, mr["avg_tokens"] / 5)
                    elif uc == "Code Generation":
                        score = (mr["avg_cps"] / max(r["avg_cps"] for r in model_rows)) * 80 + mr["pos_rate"] * 20
                    elif uc == "Creative Writing":
                        score = mr["pos_rate"] * 60 + (mr["avg_chars"] / max(r["avg_chars"] for r in model_rows)) * 40
                    elif uc == "Data Analysis":
                        score = (mr["avg_tokens"] / max(r["avg_tokens"] for r in model_rows)) * 70 + mr["pos_rate"] * 30
                    else:  # Customer Support
                        score = mr["pos_rate"] * 70 + max(0, 100 - mr["avg_rt"] * 10) * 0.3
                    row_uc[mr["model"][:15]] = f"{min(100,max(0,score)):.0f}%"
                matrix_data.append(row_uc)

            if matrix_data:
                st.dataframe(pd.DataFrame(matrix_data), use_container_width=True, hide_index=True)

            # ── Heatmap of scores ──
            if len(model_rows) >= 2:
                heat_models = [mr["model"][:18] for mr in model_rows]
                heat_scores = []
                for uc in use_cases:
                    row_scores = []
                    for mr in model_rows:
                        if uc == "Real-time Chat":
                            s = max(0, 100 - mr["avg_rt"] * 20)
                        elif uc == "Long Documents":
                            s = min(100, mr["avg_tokens"] / 5)
                        elif uc == "Code Generation":
                            s = (mr["avg_cps"] / max(r["avg_cps"] for r in model_rows)) * 80 + mr["pos_rate"] * 20
                        elif uc == "Creative Writing":
                            s = mr["pos_rate"] * 60 + (mr["avg_chars"] / max(r["avg_chars"] for r in model_rows)) * 40
                        elif uc == "Data Analysis":
                            s = (mr["avg_tokens"] / max(r["avg_tokens"] for r in model_rows)) * 70 + mr["pos_rate"] * 30
                        else:
                            s = mr["pos_rate"] * 70 + max(0, 100 - mr["avg_rt"] * 10) * 0.3
                        row_scores.append(min(100, max(0, s)))
                    heat_scores.append(row_scores)

                fig_heat = go.Figure(data=go.Heatmap(
                    z=heat_scores,
                    x=heat_models,
                    y=use_cases,
                    colorscale=[
                        [0.0, "#1d0406"],
                        [0.3, "#e63946"],
                        [0.6, "#ff6b35"],
                        [0.8, "#f7c948"],
                        [1.0, "#52b788"],
                    ],
                    text=[[f"{v:.0f}%" for v in row] for row in heat_scores],
                    texttemplate="%{text}",
                    textfont=dict(color="white", size=11, family="JetBrains Mono"),
                    hoverongaps=False,
                ))
                fig_heat.update_layout(
                    title=dict(text="🌡️ Performance Heatmap by Use Case", font=dict(color="#ff6b35", size=13, family="Cinzel")),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#c8917a"),
                    xaxis=dict(color="#c8917a", tickangle=-20),
                    yaxis=dict(color="#c8917a"),
                    margin=dict(t=50, b=60, l=140, r=20),
                    height=350,
                )
                st.plotly_chart(fig_heat, use_container_width=True)


# ══════════════════════════════════════════════════════════════════
# TAB 11: SETTINGS
# ══════════════════════════════════════════════════════════════════
with tab_settings:
    st.markdown('<div style="font-family:\'Cinzel\',serif;font-size:1rem;font-weight:700;background:linear-gradient(135deg,#ff6b35,#f7c948);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;letter-spacing:2px;margin-bottom:1rem;">🛠 SETTINGS & CONFIGURATION</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div style="font-size:0.76rem;color:#c8917a;margin-bottom:10px;font-family:\'JetBrains Mono\',monospace;">🔑 API KEYS (ALL PROVIDERS)</div>', unsafe_allow_html=True)
        for pname, pdata_s in PROVIDERS.items():
            pid     = pdata_s["id"]
            current = st.session_state.get(f"api_key_{pid}", os.environ.get(pdata_s["key_env"], ""))
            new_key = st.text_input(
                f"{pname.split('(')[0].strip()}",
                value=current, type="password",
                placeholder=f"Enter {pid} API key…",
                key=f"settings_key_{pid}"
            )
            if new_key and new_key != current:
                st.session_state[f"api_key_{pid}"] = new_key
                os.environ[pdata_s["key_env"]] = new_key
                st.success(f"✅ {pid.upper()} key updated")

    with col2:
        st.markdown('<div style="font-size:0.76rem;color:#c8917a;margin-bottom:10px;font-family:\'JetBrains Mono\',monospace;">ℹ ABOUT PHOENIX v5.0</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="background:#0d0406;border:1px solid #2a1015;border-radius:12px;padding:18px;
            font-size:0.8rem;color:#c8917a;line-height:2.1;font-family:'JetBrains Mono',monospace;">
            <strong style="color:#ff6b35;font-family:'Cinzel',serif;font-size:1rem;">🔥 Phoenix AI Studio v5.0</strong><br><br>
            {''.join(f'<span style="color:{pd["color"]};">{pn.split("(")[0].strip()}</span><br>' for pn, pd in PROVIDERS.items())}
            <br>
            <strong style="color:#fdf0e8;">NEW IN v5.1</strong><br>
            🆚 Model Comparisons Tab (NEW)<br>
            📋 Inline Report Summary (Fixed)<br>
            📈 Deep Stats Dashboard<br>
            🗒️ Session Notes System<br>
            ⚡ Model Benchmarking<br>
            🎯 AI Flashcard Generator<br>
            🌡️ Session Health Monitor<br>
            📊 Radar + Histogram + Scatter charts<br>
            😊 Mood Timeline Tracking<br>
            🔑 Keyword Frequency Map<br>
            ⭐ Prompt Favorites<br>
            🔍 Prompt Library Search<br>
            📖 Readability Analysis<br>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.markdown('<div style="font-size:0.76rem;color:#e63946;margin-bottom:10px;font-family:\'JetBrains Mono\',monospace;">⚠ DANGER ZONE</div>', unsafe_allow_html=True)
    dc1, dc2, dc3, dc4 = st.columns(4)
    with dc1:
        if st.button("🗑 Clear Chat", type="secondary", use_container_width=True):
            st.session_state.messages = []; st.session_state.analytics = []
            st.session_state.total_tokens = 0; st.session_state.session_title = None
            st.success("Chat cleared.")
    with dc2:
        if st.button("🗒️ Clear Notes", type="secondary", use_container_width=True):
            st.session_state.notes = []; st.success("Notes cleared.")
    with dc3:
        if st.button("⚡ Clear Benchmarks", type="secondary", use_container_width=True):
            st.session_state.benchmarks = []; st.success("Benchmarks cleared.")
    with dc4:
        if st.button("🔄 Reset All", type="secondary", use_container_width=True):
            for key in list(st.session_state.keys()): del st.session_state[key]
            st.rerun()
