# AI Practice Framework — Interactive Streamlit App
# -------------------------------------------------
# How to run locally:
#   1) pip install streamlit plotly graphviz streamlit-lottie
#   2) streamlit run ai_practice_streamlit_app.py
#
# Notes:
# - Lottie animations are optional; the app gracefully falls back if the library or network isn't available.
# - Use the left sidebar to navigate, or enable "Showcase Mode" for a slide-like experience.

import json
import time
from typing import Dict, List

import streamlit as st

# Optional imports (handled gracefully)
try:
    from streamlit_lottie import st_lottie
    _HAS_LOTTIE = True
except Exception:
    _HAS_LOTTIE = False

import plotly.graph_objects as go

st.set_page_config(
    page_title="AI Practice — Interactive",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Content (editable)
# -----------------------------
PILLARS: List[Dict] = [
    {
        "name": "Strategy & Advisory",
        "tag": "Strategy",
        "points": [
            "Develop enterprise-grade AI roadmaps aligned with business strategy, regulatory requirements, and industry best practices.",
            "Define investment priorities, establish AI maturity benchmarks, and guide organizations on maximizing ROI from AI initiatives.",
        ],
    },
    {
        "name": "Governance & Compliance",
        "tag": "Governance",
        "points": [
            "Establish robust AI governance frameworks, policies, and risk controls in line with MAS FEAT, NIST AI RMF, EU AI Act, and SR 11-7.",
            "Ensure responsible adoption of AI through oversight on data usage, model auditability, and regulatory reporting.",
        ],
    },
    {
        "name": "Innovation & Use Cases",
        "tag": "Innovation",
        "points": [
            "Identify, prioritize, and deliver high-value AI/ML and Generative AI use cases across customer experience, compliance, operations, and finance.",
            "Incubate new AI-driven business models via pilots and proofs-of-value to accelerate enterprise adoption.",
        ],
    },
    {
        "name": "Technology & Architecture",
        "tag": "Architecture",
        "points": [
            "Design scalable AI platforms and reference architectures with MLOps, vector databases, RAG, and agentic AI.",
            "Ensure interoperability across AWS/Azure/GCP with secure data integration and deployment.",
        ],
    },
    {
        "name": "Validation & Risk Management",
        "tag": "Validation",
        "points": [
            "Perform independent model validation, stress testing, fairness analysis, and explainability reviews.",
            "Implement continuous monitoring to detect drift, bias, and emerging risks in production.",
        ],
    },
    {
        "name": "Delivery & Scale",
        "tag": "Delivery",
        "points": [
            "Implement AI solutions through agile, iterative execution methods.",
            "Scale to enterprise level via automation, cloud-native platforms, and cross-functional coordination.",
        ],
    },
    {
        "name": "Capability Building",
        "tag": "Enablement",
        "points": [
            "Build AI literacy across the workforce—from business users to technical teams.",
            "Provide training in prompt engineering, data science, ML engineering, and Responsible AI practices.",
        ],
    },
    {
        "name": "Partnerships & Ecosystem",
        "tag": "Ecosystem",
        "points": [
            "Forge collaborations with hyperscalers, research institutions, regulators, and startups.",
            "Leverage ecosystem partnerships for co-innovation and access to emerging technologies.",
        ],
    },
]

KEY_ACTIVITIES: List[str] = [
    "Establish AI Centers of Excellence (CoEs) for governance consistency, knowledge sharing, and innovation scaling.",
    "Develop multi-agent AI solutions for process automation, decision support, and next-gen customer engagement.",
    "Enable advanced data capabilities using RAG, NLP analytics, and knowledge extraction for compliance, operations, and finance.",
    "Drive AI-powered transformation in customer experience, workforce intelligence, operational resilience, and productivity.",
    "Conduct AI maturity assessments and readiness diagnostics (e.g., AIRE™: Assess – Integrate – Realize – Elevate).",
    "Deliver explainable AI dashboards for transparency to regulators, auditors, and business leaders.",
    "Implement ethical nudges, risk guardrails, and AI safety protocols for fairness, accountability, and societal alignment.",
]

# Default maturity values (editable in UI)
DEFAULT_MATURITY = {
    "Strategy": 3,
    "Governance": 2,
    "Innovation": 3,
    "Architecture": 2,
    "Validation": 2,
    "Delivery": 3,
    "Enablement": 2,
    "Ecosystem": 2,
}

# -----------------------------
# Styles
# -----------------------------
CUSTOM_CSS = """
<style>
/***** Global *****/
:root { --brand:#6B4EFF; --ink:#0F1224; --muted:#6C7280; --bg:#0a0a0a; }

.block-container { padding-top: 1rem; }

.hero {
  padding: 2.5rem 2rem; border-radius: 24px;
  background: radial-gradient(1200px 500px at 10% -10%, rgba(107,78,255,.25), transparent),
              linear-gradient(135deg, rgba(107,78,255,.18), rgba(0,0,0,.35));
  border: 1px solid rgba(107,78,255,.25);
  box-shadow: 0 10px 35px rgba(0,0,0,.35);
  color: white;
}
.hero h1 { font-size: 2.35rem; margin: 0 0 .4rem 0; }
.hero p { opacity:.9; font-size: 1.05rem; }

.tag {
  display:inline-block; padding:.25rem .6rem; border-radius:999px; font-size:.75rem;
  background: rgba(107,78,255,.18); color:#E8E5FF; border:1px solid rgba(107,78,255,.35);
  margin: 0 .35rem .35rem 0; animation: pulse 2.5s infinite;
}
@keyframes pulse { 0%{transform:scale(1)} 50%{transform:scale(1.03)} 100%{transform:scale(1)} }

/***** Cards *****/
.grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 14px; }
.card {
  background: rgba(255,255,255,.03); border: 1px solid rgba(255,255,255,.075);
  border-radius: 18px; padding: 1rem 1rem 1rem 1rem; transition: all .25s ease; position:relative;
}
.card:hover { transform: translateY(-2px); box-shadow: 0 8px 22px rgba(0,0,0,.25); border-color: rgba(107,78,255,.45); }
.card h4 { margin:.25rem 0 .35rem 0; }
.card small { color: #B6B9C5; }
.card ul { margin:.5rem 0 0 1rem; }

.badge { position:absolute; top:10px; right:12px; font-size:.7rem; opacity:.9 }

/***** Pillar detail panel *****/
.panel {
  padding: 1rem 1.2rem; border-radius: 16px; border:1px solid rgba(255,255,255,.08);
  background: linear-gradient(180deg, rgba(107,78,255,.10), rgba(107,78,255,.03));
}

/***** Footer *****/
.footer { color:#A7ADBD; font-size:.85rem; margin-top: 1rem; }
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# -----------------------------
# Helper Functions
# -----------------------------

def load_lottie_url(url: str):
    if not _HAS_LOTTIE:
        return None
    import requests
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return r.json()
    except Exception:
        return None
    return None


def section_header(title: str, subtitle: str = ""):
    st.markdown(
        f"""
        <div class="hero">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def pillar_card(p: Dict):
    with st.container(border=False):
        st.markdown(
            f"""
            <div class="card">
                <div class="badge tag">{p['tag']}</div>
                <h4>{p['name']}</h4>
                <small>Click to expand details</small>
            </div>
            """,
            unsafe_allow_html=True,
        )
        with st.expander("Details", expanded=False):
            for pt in p["points"]:
                st.markdown(f"- {pt}")


def radar_chart(scores: Dict[str, int]):
    categories = list(scores.keys())
    values = list(scores.values())
    # Close the loop for radar
    categories += categories[:1]
    values += values[:1]
    fig = go.Figure(
        data=[
            go.Scatterpolar(r=values, theta=categories, fill="toself", name="Maturity (0-5)")
        ]
    )
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])), showlegend=False, height=520)
    st.plotly_chart(fig, use_container_width=True, theme="streamlit")


def progress_demo():
    prog = st.progress(0, text="Calibrating capabilities…")
    for i in range(0, 101, 5):
        time.sleep(0.02)
        prog.progress(i, text=f"Calibrating capabilities… {i}%")
    time.sleep(0.2)


def ecosystem_graphviz():
    import graphviz
    dot = graphviz.Digraph()
    dot.attr(rankdir='LR', bgcolor='transparent')

    dot.node('CoE', 'AI CoE', shape='folder', style='filled', color='green', fontcolor='green')
    dot.node('Gov', 'Governance\n(MAS FEAT, NIST, EU AI Act, SR11-7)', color='green', fontcolor='green')
    dot.node('Arch', 'Tech & Architecture\n(MLOps, RAG, Agentic)', color='green', fontcolor='green')
    dot.node('Val', 'Validation & Risk', color='green', fontcolor='green')
    dot.node('Del', 'Delivery & Scale', color='green', fontcolor='green')
    dot.node('Use', 'Innovation & Use Cases', color='green', fontcolor='green')
    dot.node('Cap', 'Capability Building', color='green', fontcolor='green')
    dot.node('Eco', 'Partnerships & Ecosystem', color='green', fontcolor='green')
    # Add top flow circles with green color and font
    nodes = ['CoE Gov', 'CoE Arch', 'CoE Val', 'CoE Del', 'CoE Use', 'CoE Cap', 'CoE Eco']
    for node in nodes:
        dot.node(node, node, color='green', fontcolor='green')
    for i in range(len(nodes)-1):
        dot.edge(nodes[i], nodes[i+1], color='green')
    dot.edge('Gov', 'Use', label='Policy → Pipeline', color='green')
    dot.edge('Arch', 'Del', label='Platform → Delivery', color='green')
    dot.edge('Val', 'Del', label='Controls → Release', color='green')
    dot.edge('Use', 'Cap', label='Skills Demand', color='green')
    dot.edge('Eco', 'Use', label='Co‑innovation', color='green')

    st.graphviz_chart(dot, use_container_width=True)


# -----------------------------
# Sidebar — Navigation & Modes
# -----------------------------
if "_page" not in st.session_state:
    st.session_state._page = "Overview"
if "_showcase" not in st.session_state:
    st.session_state._showcase = False
if "_slide" not in st.session_state:
    st.session_state._slide = 0

st.sidebar.title("AI Practice Framework")
nav = st.sidebar.radio(
    "Navigate",
    ["Overview", "Core Pillars", "Key Activities", "Maturity Diagnostic", "Ecosystem Map", "Showcase Mode", "Project List", "Projects Case Studies"],
    index=["Overview", "Core Pillars", "Key Activities", "Maturity Diagnostic", "Ecosystem Map", "Showcase Mode", "Project List", "Projects Case Studies"].index(st.session_state._page) if st.session_state._page in ["Overview", "Core Pillars", "Key Activities", "Maturity Diagnostic", "Ecosystem Map", "Showcase Mode", "Project List", "Projects Case Studies"] else 0,
)
st.session_state._page = nav

st.sidebar.markdown("---")
st.sidebar.checkbox("Enable Showcase Mode", value=st.session_state._showcase, key="_showcase")

if st.sidebar.button("Reset State"):
    for k in ["_slide",]:
        st.session_state[k] = 0
    st.rerun()

# -----------------------------
# Pages
# -----------------------------
if st.session_state._page == "Project List":
    section_header("Agentic AI / LLM Project Portfolio", "A showcase of unique agentic AI and LLM-powered solutions.")
    st.markdown(
        """
<table>
<thead>
<tr><th>Project</th><th>Domain</th><th>Agentic AI / LLM Uniqueness</th><th>Customer Value</th></tr>
</thead>
<tbody>
<tr><td>DiscoverIQ</td><td>Banking / Discovery</td><td>Dynamic Q&A engine (fixed + LLM-generated questions); Role-based (User/Admin); insights, discrepancies, instant functional spec</td><td>Understand client objectives faster; automate discovery & documentation</td></tr>
<tr><td>DataIQ</td><td>Data Strategy & Ops</td><td>Adaptive Q&A engine focused on enterprise data landscape (sources, quality, governance, analytics readiness); auto-generates heatmaps & gap analysis</td><td>Accelerates data discovery, highlights gaps, and builds roadmap for modernization</td></tr>
<tr><td>AIGovernanceIQ</td><td>Governance & Compliance</td><td>Agentic AI–driven discovery engine for AI policies, risk controls, compliance alignment (NIST, MAS FEAT, EU AI Act); produces governance scorecards</td><td>Simplifies regulatory alignment, provides continuous governance insights</td></tr>
<tr><td>AISafetyIQ</td><td>AI Risk & Safety</td><td>Interactive diagnostic chat for adversarial risk, model robustness, bias & fairness; generates mitigation playbooks and guardrails</td><td>Identifies AI risks early, reduces compliance exposure, improves model trustworthiness</td></tr>
<tr><td>PeopleInsight</td><td>HR / Workforce Analytics</td><td>Predictive, prescriptive, autonomous people analytics using Agentic AI</td><td>Next-gen HR intelligence beyond dashboards</td></tr>
<tr><td>OnyxGreen</td><td>Compliance</td><td>Due diligence & compliance automation; autonomous guardrails</td><td>Continuous monitoring of sanctions, regulations, risks</td></tr>
<tr><td>HotelZ Backoffice Automation</td><td>Hospitality Shared Services</td><td>Multi-agent workflow (memory agents + validation agents) for HR, Finance, Procurement, IT</td><td>Efficiency, transparency, fraud prevention in hotel ops</td></tr>
<tr><td>EagleEye</td><td>AI Observability & Security</td><td>Multi-agent MCP architecture (AI Security Agent, explainability, connectors)</td><td>Risk mitigation, explainability, compliance</td></tr>
<tr><td>AI Strategy Orchestrator</td><td>Enterprise Strategy</td><td>LangGraph hierarchical orchestration; agents simulate governance, stakeholder mgmt, AI culture</td><td>Mock VP-level AI strategy tool with PDF + prototype</td></tr>
<tr><td>Wealth Management Agentic AI</td><td>Finance</td><td>Autonomous life-event orchestration, compliance guardrails, portfolio simulations</td><td>Differentiated digital wealth advisory</td></tr>
<tr><td>IT Help Desk Agent</td><td>IT Ops</td><td>L0/L1 issue resolution with screenshot analysis; escalation loop</td><td>Reduced IT support load; faster issue resolution</td></tr>
<tr><td>Prompt Injection Tester</td><td>Cybersecurity</td><td>Streamlit app testing bots against jailbreak, override, leakage</td><td>Strengthens chatbot resilience</td></tr>
<tr><td>Multi-Agent RAG Chatbot</td><td>Enterprise Knowledge Mgmt</td><td>LangGraph orchestration; MongoDB memory; FAISS retrieval; explainability & confidence index</td><td>Reliable enterprise-grade chatbot</td></tr>
<tr><td>AIRE™ Framework</td><td>AI Readiness</td><td>Proprietary maturity framework; adaptive questionnaire → dashboard</td><td>Differentiates AI consulting; aligns with NIST, FEAT, EU AI Act</td></tr>
<tr><td>Pulse+</td><td>Workforce / Employee Well-being</td><td>AI-powered pulse survey & sentiment agent; tracks stress, morale, productivity in real time</td><td>Gives HR & leadership early warning signals</td></tr>
<tr><td>KYC / AML Agent</td><td>Banking / Compliance</td><td>Multi-agent due diligence (doc parsing, anomaly detection, sanctions screening); smart memory for clients</td><td>Cuts onboarding time, reduces fraud & compliance breaches</td></tr>
</tbody>
</table>
        """,
        unsafe_allow_html=True
    )
elif st.session_state._page == "Projects Case Studies":
    section_header("Case #1 : AML – Mule and Shell Accounts", "Project to identify Money Mule & Shell Accounts for SG / HK")
    st.markdown("""
**Project Background:** To Identify the Money Mule & Shell Accounts for SG / HK


**Solutions**

A model-based solution is developed, with a set of defined detection features, to identify the money mule /Shell behaviors based on specific red flags, known money mules from external sources (e.g, police orders) and/or previous financial crime cases investigated internally with money mule /Shell accounts identified.
Based on the identified money mule/Shell behaviors, the solution will detect potential money mule/Shell accounts by leveraging static client data as well as dynamic transaction data. Triggering conditions will be adjusted from time to time automatically based on investigation result of each output and/or known money mules/Shell from external sources. Running frequency is expected to be on monthly basis.

**Data Sources**

**Transactional Data** from Payment and Core Banking. Client uses industry leading products like Detica, Actimize and Mantas for transaction monitoring
**Tools Used** : Oracle PE data model and analytics platform, XG boost base algorithm and Python scripts

**Modelling Process & Investigation flow**
Data Sourcing --> Feature development (RedFlags are mapped to workable feature) --> Model development --> Model output validation --> Model implementation -> Alert generation--> Investigation

**Model Accuracy** : 98%. Model has predicted 10 – 15% of accounts as a potential Mule customer

**Challenges**
1. Data Sourcing for the look back period for past 18 months
2. Data Analytics tools capacity to load large data set
3. Availability of the environments with packages for supporting the statistical algorithms
4. Data platform with compatibilities with Data Analytical tools.
""")
    st.image("case1.png", caption="Case #1 : AML – Mule and Shell Accounts", use_column_width=True)

    
elif st.session_state._page == "Overview":
    section_header(
        "AI Practice Framework",
        "A modern, animated walkthrough of the core pillars, key activities, and an interactive maturity diagnostic.",
    )

    col1, col2 = st.columns([1.4, 1])
    with col1:
        st.markdown("### Why this matters")
        st.write(
            """
            - Align AI with strategy, outcomes, and regulation.
            - De-risk models with robust governance and validation.
            - Build platforms that scale across cloud and data boundaries.
            - Upskill teams and leverage ecosystem partnerships.
            """
        )
        progress_demo()
        st.caption("Tip: Use the left nav to jump between sections. Try the **Maturity Diagnostic** to make the session interactive.")

    with col2:
        if _HAS_LOTTIE:
            # Fallback animation if offline will be ignored silently
            anim = load_lottie_url("https://assets6.lottiefiles.com/packages/lf20_Stt1R5.json")
            if anim:
                st_lottie(anim, height=320, key="intro_anim")
        st.markdown(
            """
            <div class="panel">
            <b>Presentation Mode</b><br/>
            Turn on <span class="tag">Showcase Mode</span> in the sidebar to step through a Jobs‑style narrative.
            </div>
            """,
            unsafe_allow_html=True,
        )

elif st.session_state._page == "Core Pillars":
    section_header("Core Pillars", "Explore the 8 pillars that make an AI Practice resilient and scalable.")

    st.markdown('<div class="grid">', unsafe_allow_html=True)
    for p in PILLARS:
        pillar_card(p)
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state._page == "Key Activities":
    section_header("Key Activities", "What we do to operationalize strategy and deliver outcomes.")

    for i, item in enumerate(KEY_ACTIVITIES, start=1):
        with st.container(border=True):
            st.markdown(f"**{i}. {item}**")

elif st.session_state._page == "Maturity Diagnostic":
    section_header("Interactive Maturity Diagnostic", "Quickly gauge your organization's readiness across the AI Practice pillars.")

    # Sliders
    st.subheader("Set your current maturity (0–5)")
    cols = st.columns(4)
    keys = ["Strategy", "Governance", "Innovation", "Architecture", "Validation", "Delivery", "Enablement", "Ecosystem"]

    values = {}
    for idx, k in enumerate(keys):
        with cols[idx % 4]:
            values[k] = st.slider(k, 0, 5, value=DEFAULT_MATURITY.get(k, 2))

    st.markdown("---")
    colA, colB = st.columns([1.3, 1])
    with colA:
        radar_chart(values)
    with colB:
        total = sum(values.values())
        pct = round((total / (len(values) * 5)) * 100)
        st.metric(label="Overall Maturity", value=f"{pct}%")
        st.write("**Interpretation**")
        st.write(
            """
            - **0–30%**: Foundational — prioritize governance, platform, and 1–2 high‑value use cases.
            - **31–65%**: Emerging — scale CoE, standardize MLOps, and expand training & controls.
            - **66–100%**: Scaling — accelerate multi‑agent automation and cross‑cloud deployments.
            """
        )
        if st.button("Animate Improvement Plan"):
            progress_demo()
            st.success("Proposed 90‑day plan generated. (Narrate next steps live while the radar updates.)")

    st.markdown("---")
    with st.expander("Download your snapshot"):
        payload = {"maturity": values}
        st.download_button("Download JSON", data=json.dumps(payload, indent=2), file_name="ai_practice_maturity.json")

elif st.session_state._page == "Ecosystem Map":
    section_header("Ecosystem & Flow", "How the CoE orchestrates governance, platforms, delivery, and outcomes with partners.")
    ecosystem_graphviz()

elif st.session_state._page == "Showcase Mode":
    # Do not assign to st.session_state._showcase after widget instantiation
    # Use the value from session_state instead
    slides = [
        {
            "title": "Vision",
            "subtitle": "From ambition to outcomes — a simple, elegant path to enterprise AI.",
            "body": [
                "Craft strategy that lands: goals → use cases → architecture → adoption.",
                "Design for explainability, compliance, and trust from day zero.",
            ],
        },
        {
            "title": "The 8 Pillars",
            "subtitle": "Resilient systems are built from balanced capabilities.",
            "body": [p['name'] for p in PILLARS],
        },
        {
            "title": "From Idea to Scale",
            "subtitle": "Pilot fast. Validate early. Scale what works.",
            "body": [
                "CoE standardizes patterns and guardrails.",
                "Multi‑agent automations amplify productivity and CX.",
            ],
        },
        {
            "title": "Maturity in Minutes",
            "subtitle": "A lightweight diagnostic sparks the right conversation.",
            "body": [
                "Assess → Prioritize → Roadmap (AIRE™).",
                "Visualize maturity and narrate a 90‑day plan.",
            ],
        },
    ]

    idx = st.session_state._slide

    section_header(slides[idx]["title"], slides[idx]["subtitle"])
    with st.container(border=True):
        for b in slides[idx]["body"]:
            st.markdown(f"- {b}")
    st.markdown(" ")

    c1, c2, c3 = st.columns([1,1,6])
    with c1:
        if st.button("◀ Prev", disabled=(idx == 0)):
            st.session_state._slide = max(0, idx - 1)
            st.rerun()
    with c2:
        if st.button("Next ▶", disabled=(idx == len(slides)-1)):
            st.session_state._slide = min(len(slides)-1, idx + 1)
            st.rerun()

    st.caption("Tip: Pair this with voiceover or a live demo of the diagnostic.")

# -----------------------------
# Footer
# -----------------------------
st.markdown(
    """
    <div class="footer">
    Built with ❤️ in Streamlit · RAG, Agentic AI, and enterprise‑grade governance ready.
    </div>
    """,
    unsafe_allow_html=True,
)
