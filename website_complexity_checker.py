import streamlit as st
from openai import OpenAI

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="Web Scraping Complexity Evaluator",
    page_icon="🕸️",
    layout="centered"
)

st.title("🕸️ Web Scraping Complexity Evaluator")
st.caption("12-Factor Web Scraping Framework • AI-Powered")

# -------------------------------------------------
# OPENAI CONFIG (HARD-LOCKED)
# -------------------------------------------------
MODEL = "gpt-5.2"
API_KEY = st.secrets.get("OPENAI_API_KEY")

if not API_KEY:
    st.error("OpenAI API key is not configured. Please set OPENAI_API_KEY in Streamlit Secrets.")
    st.stop()

# -------------------------------------------------
# FIXED SYSTEM PROMPT (DO NOT MODIFY)
# -------------------------------------------------
SYSTEM_PROMPT = """
You are an expert web scraper. Evaluate the scraping complexity of the following website using the lean expert engine
(4 dimensions: data_accessibility, js_dependency, anti_bot, request_viability). Ignore operational cost and stability risk.

URL: {url}

Rules:
- Score each dimension 0-10 using the following definitions:

Data Accessibility:
0–3 → Public or replayable APIs
4–5 → Static or semi-static HTML
6–8 → JS-hydrated or private APIs
9–10 → Browser-only data

JS / Rendering Dependency:
0 → No JS required
3 → Optional JS
6 → JS required
8 → Stateful hydration
10 → Behavior-dependent rendering

Anti-Bot Defenses:
Add points for each signal detected (cap at 10):
- CAPTCHA → +2
- JS challenge → +1
- TLS / fingerprinting → +2
- Behavioral detection → +2
- Silent degradation → +2
- IP reputation filtering → +1

Request Viability:
0 → Requests work cleanly
3 → Headers required
5 → Cookies required
7 → Session-bound
10 → Requests blocked

Final Score = 0.30*DataAccessibility + 0.20*JSDependency + 0.35*AntiBot + 0.15*RequestViability
Round up if AntiBot >=8, round down if AntiBot <=4

Output required:

1. Summary Table:
| Dimension | Score | Findings | Evidence | Scraping Impact |

2. Final Verdict:
- Final complexity score (1–10)
- Difficulty classification (1–3: Simple, 4–6: Moderate, 7–8: Difficult, 9–10: Extremely Difficult)
- Short expert justification

Return **only these two sections**. Do not include JSON or other content.
"""

# -------------------------------------------------
# USER INPUTS
# -------------------------------------------------
url = st.text_input(
    "Target URL",
    placeholder="https://www.example.com"
)

description = st.text_area(
    "Optional Description (what data you want to scrape)",
    placeholder="e.g. product listings, prices, reviews",
    height=100
)

# -------------------------------------------------
# OPENAI CALL
# -------------------------------------------------
def evaluate_scraping_complexity(url, description):
    client = OpenAI(api_key=API_KEY)

    user_prompt = f"""
Task: Evaluate the web scraping complexity of the following target using the 12-Factor Web Scraping Framework.

Target URL:
{url}

Optional Description:
{description}
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]
    )

    return response.choices[0].message.content

# -------------------------------------------------
# ACTION
# -------------------------------------------------
if st.button("🚀 Evaluate Complexity"):
    if not url:
        st.error("Please enter a target URL.")
    else:
        with st.spinner("Analyzing scraping complexity..."):
            try:
                output = evaluate_scraping_complexity(url, description)
                st.success("Evaluation Complete")
                st.markdown(output)
            except Exception as e:
                st.error(f"Error: {str(e)}")

# -------------------------------------------------
# FOOTER
# -------------------------------------------------
st.markdown("---")
st.caption(
    "⚠️ This tool estimates scraping complexity only. "
    "It does not scrape, crawl, or access the target website."
)
