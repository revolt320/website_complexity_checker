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
MODEL = "gpt-4.1"
API_KEY = st.secrets.get("OPENAI_API_KEY")

if not API_KEY:
    st.error("OpenAI API key is not configured. Please set OPENAI_API_KEY in Streamlit Secrets.")
    st.stop()

# -------------------------------------------------
# FIXED SYSTEM PROMPT (DO NOT MODIFY)
# -------------------------------------------------
SYSTEM_PROMPT = """
You are a web scraping complexity evaluation agent.

Your task is to evaluate the web scraping complexity of a given target URL using the 12-Factor Web Scraping Framework.

Scoring Rules:
- Each factor must be evaluated twice independently and then averaged.
- Scores must be integers from 1 (Very Easy) to 5 (Very Hard).
- Use practical scraping assumptions based on visible site behavior and common industry constraints.

Fixed Factor Priority Weights:
- Page Structure Stability — 12%
- Pagination Pattern — 6%
- Dynamic Content Loading — 10%
- API Availability — 10%
- Anti-Bot Measures — 14%
- Data Volume — 10%
- Authentication Requirements — 4%
- URL Patterns & Discovery — 6%
- Geographic/IP Restrictions — 8%
- Content Type — 2%
- Required Post-Processing — 12%
- Change Frequency — 6%

Output Requirements (STRICT):
Your response must contain exactly two sections:

1. 12-Factor Analysis Table
Include all 12 factors in the exact order.
For each factor provide:
- Average Score (1–5)
- One concise, single-line justification

2. Final Complexity Score (Weighted Average)
Output ONLY:
- Final weighted score (rounded to 2 decimals)
- Complexity label:
  1–2 → Easy
  2–3 → Medium
  3–4 → Hard
  4–5 → Very Hard

No explanations, no breakdowns, no extra text.
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
