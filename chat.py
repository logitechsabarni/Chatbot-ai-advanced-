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
        "models": ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro"],
        "default": "gemini-2.0-flash",
        "key_env": "GEMINI_API_KEY",
        "url": "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
        "openai_compat": False,
        "color": "#f7c948",
        "icon": "🌟",
        "desc": "Google Gemini 2.0 Flash + Pro",
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
            "systemInstruction": {"parts": [{"text": system_prompt}]},
            "contents": contents,
            "generationConfig": {"temperature": temperature, "maxOutputTokens": max_tokens},
        }
        resp = requests.post(url, headers=headers, json=payload, timeout=60)
        resp.raise_for_status()
        return resp.json()["candidates"][0]["content"]["parts"][0]["text"]

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
    "🛠 Settings",
])
tab_chat, tab_prompts, tab_analytics, tab_nlp, tab_deepstats, tab_notes, tab_bench, tab_flash, tab_health, tab_settings = tabs


# ══════════════════════════════════════════════════════════════════
# TAB 1: CHAT
# ══════════════════════════════════════════════════════════════════
with tab_chat:
    if not st.session_state.messages:
        st.markdown(f"""
        <div class="msg-animate" style="text-align:center;padding:2.5rem 0 1.5rem;">
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

        suggestions = [
            ("🔥","Explain how transformer attention works"),
            ("🐍","Write a Python async REST API with FastAPI"),
            ("⚡","Compare LLaMA 3 vs GPT-4o architectures"),
            ("🌑","Write a cyberpunk noir short story"),
            ("🔐","Explain SQL injection and prevention"),
            ("🧮","Implement a min-heap in Python"),
        ]
        cols = st.columns(3)
        for i, (icon, prompt) in enumerate(suggestions):
            with cols[i % 3]:
                if st.button(f"{icon}  {prompt}", use_container_width=True, key=f"sugg_{i}"):
                    st.session_state._pending_prompt = prompt
                    st.rerun()
        st.markdown("<br>", unsafe_allow_html=True)

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

        # Track provider usage
        pid = pdata["id"]
        st.session_state.provider_usage[pid] = st.session_state.provider_usage.get(pid, 0) + 1

        # Track daily usage
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

                # Update word frequency
                for word, freq in keywords:
                    st.session_state.word_freq_all[word] = st.session_state.word_freq_all.get(word, 0) + freq

                # Update mood log
                st.session_state.mood_log.append({"time": datetime.now().strftime("%H:%M"), "sentiment": sent, "score": sent_score})

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
    st.markdown('<p style="color:#4a2a22;font-size:0.82rem;margin-bottom:1.2rem;font-family:\'JetBrains Mono\',monospace;">Click any prompt to load it into the chat</p>', unsafe_allow_html=True)

    # Prompt search
    prompt_search = st.text_input("🔍 Search prompts", placeholder="Search library…", key="prompt_search")

    all_prompts_flat = [(cat, p) for cat, prompts in PROMPT_LIBRARY.items() for p in prompts]
    if prompt_search:
        filtered = [(cat, p) for cat, p in all_prompts_flat if prompt_search.lower() in p.lower()]
        st.markdown(f'<div style="font-size:0.72rem;color:#ff6b35;font-family:\'JetBrains Mono\',monospace;margin-bottom:8px;">{len(filtered)} prompts found</div>', unsafe_allow_html=True)
        for cat, prompt in filtered:
            col_p, col_b = st.columns([5, 1])
            with col_p:
                st.markdown(f'<div style="padding:6px 0;color:#e8d5c8;font-family:\'Crimson Pro\',serif;font-size:0.95rem;"><span style="font-size:0.7rem;color:#4a2a22;">{cat}</span> · {prompt}</div>', unsafe_allow_html=True)
            with col_b:
                if st.button("Use", key=f"search_lib_{hash(prompt)}", use_container_width=True):
                    st.session_state._pending_prompt = prompt
                    st.rerun()
    else:
        for category, prompts in PROMPT_LIBRARY.items():
            with st.expander(category, expanded=False):
                for prompt in prompts:
                    col_p, col_b = st.columns([5, 1])
                    with col_p:
                        st.markdown(f'<div style="padding:6px 0;color:#e8d5c8;font-family:\'Crimson Pro\',serif;font-size:0.95rem;">{prompt}</div>', unsafe_allow_html=True)
                    with col_b:
                        if st.button("Use", key=f"lib_{hash(prompt)}", use_container_width=True):
                            st.session_state._pending_prompt = prompt
                            st.rerun()

    st.divider()

    # Favorites section
    st.markdown('<div style="font-size:0.76rem;color:#f7c948;margin-bottom:8px;font-family:\'JetBrains Mono\',monospace;">⭐ FAVORITES</div>', unsafe_allow_html=True)
    if st.session_state.favorites:
        for i, fav in enumerate(st.session_state.favorites):
            col_f, col_fb, col_fd = st.columns([4, 1, 1])
            with col_f:
                st.markdown(f'<div style="padding:5px 0;color:#e8d5c8;font-size:0.9rem;font-family:\'Crimson Pro\',serif;">{fav}</div>', unsafe_allow_html=True)
            with col_fb:
                if st.button("Use", key=f"fav_use_{i}", use_container_width=True):
                    st.session_state._pending_prompt = fav
                    st.rerun()
            with col_fd:
                if st.button("🗑", key=f"fav_del_{i}", use_container_width=True):
                    st.session_state.favorites.pop(i)
                    st.rerun()
    else:
        st.markdown('<div style="color:#4a2a22;font-size:0.8rem;font-family:\'JetBrains Mono\',monospace;">No favorites yet — add your custom prompts below</div>', unsafe_allow_html=True)

    st.divider()
    st.markdown('<div style="font-size:0.8rem;color:#4a2a22;font-family:\'JetBrains Mono\',monospace;margin-bottom:8px;">✏️ CUSTOM PROMPT</div>', unsafe_allow_html=True)
    custom_prompt = st.text_area("", placeholder="Type your own prompt…", height=80, label_visibility="collapsed", key="custom_prompt_input")
    col_cp1, col_cp2 = st.columns(2)
    with col_cp1:
        if st.button("🔥 Send Custom Prompt", use_container_width=True):
            if custom_prompt.strip():
                st.session_state._pending_prompt = custom_prompt.strip()
                st.rerun()
    with col_cp2:
        if st.button("⭐ Save to Favorites", use_container_width=True):
            if custom_prompt.strip() and custom_prompt.strip() not in st.session_state.favorites:
                st.session_state.favorites.append(custom_prompt.strip())
                st.success("Added to favorites!")
                st.rerun()


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

        # ── Metrics row ──
        m1, m2, m3, m4, m5, m6 = st.columns(6)
        m1.metric("Exchanges", len(ai_msgs))
        m2.metric("Avg Length", f"{avg_len} ch")
        m3.metric("Total Tokens", f"~{st.session_state.total_tokens:,}")
        m4.metric("Positive Rate", f"{pos/max(1,len(sentiments)):.0%}")
        m5.metric("Avg Speed", f"{avg_cps:.0f} c/s")
        m6.metric("Avg RT", f"{avg_rt:.1f}s")

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Row 1: Sentiment Pie + Intent Bar ──
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

        # ── Row 2: Response length line + RT scatter ──
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

        # ── Row 3: Radar + Tokens bar ──
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

        # ── Recent Exchanges Table ──
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

        # Keyword frequency bar chart
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
            <div>Enter any text above to run NLP analysis</div>
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
        # ── Provider Usage Pie ──
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

        # ── Sentiment Timeline ──
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

        # ── Word Cloud style (top words bar) ──
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

        # ── Response Speed Distribution (Histogram) ──
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

        # ── Speed vs Length Scatter ──
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

        # ── Readability distribution ──
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

    # Add note
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

    # Display notes
    if st.session_state.notes:
        # Filter by tag
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

        # Export notes
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

                    # Show result
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

    # Benchmark history
    if st.session_state.benchmarks:
        st.markdown('<div style="font-size:0.76rem;color:#c8917a;margin:14px 0 8px;font-family:\'JetBrains Mono\',monospace;">📋 BENCHMARK HISTORY</div>', unsafe_allow_html=True)
        bench_df = pd.DataFrame([{
            "Time": b["timestamp"], "Task": b["task"], "Model": b["model"],
            "RT (s)": b["rt"], "Tokens": b["tokens"], "Speed (c/s)": b["cps"],
        } for b in st.session_state.benchmarks])
        st.dataframe(bench_df, use_container_width=True, hide_index=True)

        # Benchmark comparison chart
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
    st.markdown('<div style="font-family:\'Cinzel\',serif;font-size:1rem;font-weight:700;background:linear-gradient(135deg,#ff6b35,#f7c948);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;letter-spacing:2px;margin-bottom:1rem;">🎯 AI FLASHCARD GENERATOR</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.78rem;color:#4a2a22;font-family:\'JetBrains Mono\',monospace;margin-bottom:12px;">Generate AI-powered flashcards for any topic and test your knowledge</div>', unsafe_allow_html=True)

    col_fc1, col_fc2 = st.columns(2)
    with col_fc1:
        flash_category = st.selectbox("Category", list(FLASHCARD_TOPICS.keys()), key="flash_cat")
        flash_topic = st.selectbox("Topic", FLASHCARD_TOPICS[flash_category], key="flash_topic")
    with col_fc2:
        custom_flash = st.text_input("Or enter custom topic", placeholder="e.g. React hooks, Kubernetes, etc.", key="custom_flash")

    final_topic = custom_flash.strip() if custom_flash.strip() else flash_topic

    if st.button(f"🔥 Generate Flashcard: {final_topic}", use_container_width=True):
        if not active_api_key:
            st.error("⚠ No API key configured.")
        else:
            with st.spinner(f"Generating flashcard for: {final_topic}…"):
                try:
                    prompt = f"""Create a concise, educational flashcard for the topic: "{final_topic}"

Format your response EXACTLY like this:
FRONT: [A clear question or concept to test knowledge]
BACK: [A comprehensive but concise answer (3-6 sentences)]
EXAMPLE: [One concrete code or real-world example]
KEY_POINT: [The single most important thing to remember]"""

                    response = call_ai(provider, model_sel,
                        [{"role":"user","content":prompt}],
                        "You are an expert educator creating clear, accurate flashcards.",
                        0.5, 600, active_api_key)

                    # Parse response
                    lines = response.strip().split('\n')
                    parsed = {}
                    current_key = None
                    for line in lines:
                        for key in ["FRONT:", "BACK:", "EXAMPLE:", "KEY_POINT:"]:
                            if line.startswith(key):
                                current_key = key.replace(":", "").lower()
                                parsed[current_key] = line[len(key):].strip()
                                break
                        else:
                            if current_key and line.strip():
                                parsed[current_key] = parsed.get(current_key, "") + " " + line.strip()

                    front = parsed.get("front", "?")
                    back  = parsed.get("back", response)
                    example = parsed.get("example", "")
                    key_point = parsed.get("key_point", "")

                    st.markdown(f"""
                    <div style="background:linear-gradient(135deg,#0d0406,#060203);border:1px solid #ff6b3540;
                        border-radius:16px;padding:24px;margin:12px 0;position:relative;overflow:hidden;">
                        <div style="position:absolute;top:0;left:0;right:0;height:2px;
                            background:linear-gradient(90deg,transparent,#ff6b35,#f7c948,transparent);"></div>

                        <div style="font-family:'Cinzel',serif;font-size:0.7rem;color:#4a2a22;letter-spacing:2px;margin-bottom:12px;">FLASHCARD · {flash_category.upper()}</div>

                        <div style="background:#0d0406;border:1px solid #2a1015;border-radius:10px;padding:16px;margin-bottom:12px;">
                            <div style="font-size:0.62rem;color:#ff6b35;font-family:'JetBrains Mono',monospace;margin-bottom:8px;">📋 FRONT</div>
                            <div style="color:#fdf0e8;font-size:1.05rem;font-family:'Crimson Pro',serif;line-height:1.6;">{front}</div>
                        </div>

                        <div style="background:#0d0406;border:1px solid #52b78830;border-radius:10px;padding:16px;margin-bottom:12px;">
                            <div style="font-size:0.62rem;color:#52b788;font-family:'JetBrains Mono',monospace;margin-bottom:8px;">✅ BACK</div>
                            <div style="color:#e8d5c8;font-size:0.95rem;font-family:'Crimson Pro',serif;line-height:1.7;">{back}</div>
                        </div>

                        {"" if not example else f'<div style="background:#0d0406;border:1px solid #74c0fc30;border-radius:10px;padding:16px;margin-bottom:12px;"><div style="font-size:0.62rem;color:#74c0fc;font-family:\'JetBrains Mono\',monospace;margin-bottom:8px;">💡 EXAMPLE</div><div style="color:#e8d5c8;font-size:0.9rem;font-family:\'JetBrains Mono\',monospace;line-height:1.6;">{example}</div></div>'}

                        {"" if not key_point else f'<div style="background:linear-gradient(135deg,#f7c94810,#ff6b3508);border:1px solid #f7c94830;border-radius:10px;padding:12px;"><div style="font-size:0.62rem;color:#f7c948;font-family:\'JetBrains Mono\',monospace;margin-bottom:6px;">⭐ KEY POINT</div><div style="color:#f7c948;font-size:0.9rem;font-family:\'Crimson Pro\',serif;font-weight:600;">{key_point}</div></div>'}
                    </div>
                    """, unsafe_allow_html=True)

                    # Send to chat option
                    if st.button(f"💬 Ask Phoenix to explain {final_topic} further", use_container_width=True):
                        st.session_state._pending_prompt = f"Please give me a detailed explanation of: {final_topic}. Include practical examples and common mistakes to avoid."
                        st.rerun()

                except Exception as e:
                    st.error(f"Flashcard generation failed: {e}")

    # Quiz score tracker
    st.divider()
    st.markdown('<div style="font-size:0.76rem;color:#c8917a;margin-bottom:8px;font-family:\'JetBrains Mono\',monospace;">📊 STUDY TRACKER</div>', unsafe_allow_html=True)
    col_qs1, col_qs2, col_qs3 = st.columns(3)
    col_qs1.metric("Topics Studied", len(st.session_state.get("flashcard_history", [])))
    col_qs2.metric("Flashcards Generated", st.session_state.flashcard_idx)
    col_qs3.metric("Session Duration", f"{(datetime.now() - datetime.fromisoformat(st.session_state.session_start)).seconds // 60}m")


# ══════════════════════════════════════════════════════════════════
# TAB 9: SESSION HEALTH
# ══════════════════════════════════════════════════════════════════
with tab_health:
    st.markdown('<div style="font-family:\'Cinzel\',serif;font-size:1rem;font-weight:700;background:linear-gradient(135deg,#ff6b35,#f7c948);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;letter-spacing:2px;margin-bottom:1rem;">🌡️ SESSION HEALTH DASHBOARD</div>', unsafe_allow_html=True)

    valid_a = [a for a in st.session_state.analytics if a]
    session_dur_sec = (datetime.now() - datetime.fromisoformat(st.session_state.session_start)).seconds
    msg_count = len(st.session_state.messages)

    # Health scores
    token_usage_pct  = min(100, (st.session_state.total_tokens / 50000) * 100)
    activity_score   = min(100, (msg_count / 50) * 100)
    positivity_score = (sum(1 for a in valid_a if a.get("sentiment") == "positive") / max(1, len(valid_a))) * 100
    speed_score      = 100 - min(100, ((sum(a.get("response_time",0) for a in valid_a) / max(1,len(valid_a))) / 10) * 100) if valid_a else 50
    overall_health   = (100 - token_usage_pct * 0.3 + positivity_score * 0.4 + speed_score * 0.3)
    overall_health   = max(0, min(100, overall_health))

    # Big health meter
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
            <div style="display:flex;justify-content:space-between;margin-bottom:8px;">
                <span>Duration</span><span style="color:#f7c948;">{dur_str}</span>
            </div>
            <div style="display:flex;justify-content:space-between;margin-bottom:8px;">
                <span>Messages</span><span style="color:#ff6b35;">{msg_count}</span>
            </div>
            <div style="display:flex;justify-content:space-between;margin-bottom:8px;">
                <span>Tokens Used</span><span style="color:#c084fc;">~{st.session_state.total_tokens:,}</span>
            </div>
            <div style="display:flex;justify-content:space-between;margin-bottom:8px;">
                <span>Notes Saved</span><span style="color:#67e8f9;">{len(st.session_state.notes)}</span>
            </div>
            <div style="display:flex;justify-content:space-between;">
                <span>Provider</span><span style="color:{pcolor};">{pdata['id'].upper()}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Health breakdown bars ──
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

    # ── Mood timeline ──
    if st.session_state.mood_log:
        st.markdown('<div style="font-size:0.76rem;color:#c8917a;margin:14px 0 8px;font-family:\'JetBrains Mono\',monospace;">😊 CONVERSATION MOOD FLOW</div>', unsafe_allow_html=True)
        ml = st.session_state.mood_log
        sent_map2 = {"positive": 1, "neutral": 0, "negative": -1}
        y_mood = [sent_map2.get(m["sentiment"], 0) for m in ml]
        x_mood = list(range(1, len(ml)+1))
        colors_mood = ["#52b788" if v > 0 else "#e63946" if v < 0 else "#c8917a" for v in y_mood]

        fig_mood = go.Figure()
        fig_mood.add_trace(go.Bar(
            x=x_mood, y=y_mood, name="Mood",
            marker=dict(color=colors_mood, line=dict(color='rgba(0,0,0,0)')),
        ))
        fig_mood.add_trace(go.Scatter(
            x=x_mood, y=y_mood, mode='lines', name="Trend",
            line=dict(color='#f7c948', width=2, dash='dot'),
        ))
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

    # Tips
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
# TAB 10: SETTINGS
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
            <strong style="color:#fdf0e8;">NEW IN v5.0</strong><br>
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
