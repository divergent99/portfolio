import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

app = dash.Dash(
    __name__,
    external_stylesheets=[
        "https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;700&family=Inter:wght@300;400;500;600;700;800&display=swap",
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css",
    ],
    title="Abhineet Sharma | AI Engineer",
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"},
        {"name": "description", "content": "AI Engineer specializing in GenAI, LangGraph, RAG pipelines, and multi-agent systems."},
    ],
    suppress_callback_exceptions=True,
)
server = app.server

# ══════════════════════════════════════════════════════════════════
# DATA
# ══════════════════════════════════════════════════════════════════

PROJECTS = [
    {
        "name": "VaultDesk",
        "hackathon": "Auth0 'Authorized to Act' Hackathon",
        "status": "Deployed",
        "status_color": "#00ffa3",
        "tagline": "AI-powered M&A deal room with guardian push approvals",
        "description": (
            "Enterprise-grade M&A deal room assistant built on Auth0 Token Vault. "
            "Features CIBA Guardian push approval before any email or calendar action, "
            "a LangGraph multi-agent backend, and a 28-file modular architecture "
            "deployed on Railway."
        ),
        "highlights": [
            "CIBA Guardian push approval flow before sensitive actions",
            "Gmail + Google Calendar tool integration via Auth0 Token Vault",
            "Single-process FastAPI + Dash via WSGIMiddleware",
            "Full production deploy on Railway",
        ],
        "stack": ["LangGraph", "Auth0 Token Vault", "Amazon Nova Lite", "FastAPI", "Dash", "Gmail API"],
        "github": "https://github.com/divergent99/vaultdesk",
        "live": "https://vaultdesk-production.up.railway.app",
        "icon": "fa-vault",
        "accent": "#6366f1",
    },
    {
        "name": "NovaDD",
        "hackathon": "Amazon Nova AI Hackathon",
        "status": "Submitted",
        "status_color": "#f59e0b",
        "tagline": "M&A due diligence RAG pipeline with extended thinking",
        "description": (
            "Multi-agent virtual data room intelligence platform. Processes deal documents "
            "through a ChromaDB RAG pipeline and surfaces structured diligence insights "
            "via a Dash frontend, powered by Amazon Bedrock Nova 2 with Extended Thinking."
        ),
        "highlights": [
            "Amazon Bedrock Nova 2 Lite with Extended Thinking enabled",
            "ChromaDB vector store for semantic document retrieval",
            "Multi-agent LangGraph pipeline for structured diligence",
            "Team of 4 — collaborative hackathon build",
        ],
        "stack": ["Amazon Bedrock Nova 2", "Extended Thinking", "LangGraph", "ChromaDB", "FastAPI", "Dash"],
        "github": "https://github.com/divergent99/VDR-Intelligence",
        "live": None,
        "icon": "fa-magnifying-glass-chart",
        "accent": "#f59e0b",
    },
    {
        "name": "Verdikt",
        "hackathon": "HackHazards '26",
        "status": "Submitted",
        "status_color": "#f59e0b",
        "tagline": "Parallel analyst council for multi-perspective due diligence",
        "description": (
            "Five specialist agents — Legal, Financial, Market, Ops, Risk — analyze "
            "deals concurrently using Groq's ultra-fast inference. A Senior Partner "
            "synthesis agent consolidates all findings into a structured investment thesis."
        ),
        "highlights": [
            "5 parallel specialist agents + Senior Partner synthesis layer",
            "Groq llama-3.3-70b-versatile for sub-second inference",
            "SentenceTransformers for semantic document chunking",
            "Full src/verdikt/ modular package structure",
        ],
        "stack": ["Groq llama-3.3-70b", "LangGraph", "ChromaDB", "SentenceTransformers", "Dash", "FastAPI"],
        "github": "https://github.com/divergent99/verdikt",
        "live": None,
        "icon": "fa-scale-balanced",
        "accent": "#10b981",
    },
    {
        "name": "VDR Voice Intelligence",
        "hackathon": "Gemini Live Agent Challenge",
        "status": "Built",
        "status_color": "#3b82f6",
        "tagline": "Voice-first document intelligence via Gemini Live API",
        "description": (
            "Analysts speak their questions and get spoken + visual responses back. "
            "A real-time WebSocket audio pipeline streams Gemini Live API responses "
            "directly into a Dash interface, eliminating the keyboard entirely."
        ),
        "highlights": [
            "Gemini Live API for real-time voice understanding",
            "WebSocket audio pipeline for streaming bi-directional audio",
            "Voice + visual output for diligence findings",
            "FastAPI + Dash single-app architecture",
        ],
        "stack": ["Gemini Live API", "WebSocket", "FastAPI", "Dash", "Google Cloud Run"],
        "github": "https://github.com/divergent99",
        "live": None,
        "icon": "fa-microphone-lines",
        "accent": "#3b82f6",
    },
    {
        "name": "Agents Assemble",
        "hackathon": "Devpost Healthcare AI — $25K Prize",
        "status": "In Progress",
        "status_color": "#ec4899",
        "tagline": "Uninsured patient navigator using MCP + HL7 FHIR",
        "description": (
            "Healthcare AI platform reading HL7 FHIR patient profiles via MCP to guide "
            "uninsured patients through care options, costs, and coverage eligibility. "
            "Built on A2A protocol for multi-agent coordination across care services."
        ),
        "highlights": [
            "MCP server reading HL7 FHIR patient profiles",
            "A2A protocol for multi-agent care navigation",
            "$25K prize pool — active submission",
            "Covers care options, costs, and coverage eligibility",
        ],
        "stack": ["MCP", "A2A Protocol", "HL7 FHIR", "LangGraph", "FastAPI", "Dash"],
        "github": "https://github.com/divergent99",
        "live": None,
        "icon": "fa-hospital-user",
        "accent": "#ec4899",
    },
]

SKILL_CATS = [
    {
        "label": "// Agentic AI",
        "color": "#6366f1",
        "skills": [
            ("LangGraph", "fa-diagram-project"),
            ("LangChain", "fa-link"),
            ("LlamaIndex", "fa-layer-group"),
            ("CrewAI", "fa-users-gear"),
            ("MCP / A2A", "fa-plug"),
        ],
    },
    {
        "label": "// LLMs & Cloud",
        "color": "#f59e0b",
        "skills": [
            ("Azure OpenAI", "fa-cloud"),
            ("AWS Bedrock", "fa-cloud"),
            ("Gemini Live", "fa-microphone"),
            ("Groq", "fa-bolt"),
            ("HuggingFace", "fa-face-smile"),
            ("OpenAI Whisper", "fa-wave-square"),
        ],
    },
    {
        "label": "// RAG & Vector",
        "color": "#10b981",
        "skills": [
            ("ChromaDB", "fa-database"),
            ("Docling / MinerU", "fa-file-lines"),
            ("Vector Search", "fa-magnifying-glass"),
            ("Semantic Chunking", "fa-scissors"),
        ],
    },
    {
        "label": "// Data & ML",
        "color": "#3b82f6",
        "skills": [
            ("TensorFlow", "fa-brain"),
            ("GLoVe Embeddings", "fa-network-wired"),
            ("Google BigQuery", "fa-table"),
            ("DuckDB", "fa-database"),
            ("RFM / CLV / Churn", "fa-chart-line"),
        ],
    },
    {
        "label": "// Backend & DevOps",
        "color": "#8b5cf6",
        "skills": [
            ("FastAPI", "fa-rocket"),
            ("Docker", "fa-docker"),
            ("CI/CD", "fa-gears"),
            ("Python", "fa-python"),
            ("SQL", "fa-code"),
        ],
    },
    {
        "label": "// Frontend",
        "color": "#ec4899",
        "skills": [
            ("Plotly Dash", "fa-chart-bar"),
            ("Streamlit", "fa-display"),
            ("Gradio", "fa-sliders"),
            ("React", "fa-react"),
        ],
    },
]

EXPERIENCE = [
    {
        "role": "Associate (AI Engineer)",
        "company": "Alvarez & Marsal",
        "company_url": "https://www.alvarezandmarsal.com",
        "dates": "Jan 2025 — Present",
        "accent": "#6366f1",
        "active": True,
        "desc": "Building production GenAI systems for the GCC Gen Platform initiative, supporting CDD and PE deal teams with LLM-driven automation, conversational agents, and document intelligence pipelines.",
        "bullets": [
            "Engineered OCR + ASR ingestion with LLM-based extraction (Whisper, pytesseract), increasing data capture accuracy by 35%",
            "Operationalized conversational agents with LangGraph for real-time metric retrieval, enabling 20+ executive briefings per quarter",
            "Deployed containerized microservices via FastAPI, Docker, and CI/CD, improving service reliability by 40%",
            "Spearheaded ML-driven onboarding optimization cutting processing time 28% and saving $120K annually",
            "Implemented automated testing and monitoring to reduce production bugs by 60%",
        ],
        "tech": ["LangGraph", "LangChain", "LlamaIndex", "Azure OpenAI", "OpenAI Whisper", "pytesseract", "FastAPI", "Docker", "CI/CD"],
    },
    {
        "role": "Data Scientist",
        "company": "Newgen Software",
        "company_url": "https://www.newgensoft.com",
        "dates": "Oct 2022 — Dec 2024",
        "accent": "#10b981",
        "active": False,
        "desc": "Built enterprise GenAI applications, recommendation systems, and classical ML pipelines for e-commerce and BFSI clients. Focused on RAG, multi-agent workflows, and embedding-based systems.",
        "bullets": [
            "Built enterprise GenAI apps with RAG and multi-agent workflows, reducing average query time by 65%",
            "Created embedding-based recommendations with GLoVe and product catalogs, increasing CTR by 18%",
            "Implemented classical ML for e-commerce and BFSI (RFM, CLV, forecasting, churn, uplift, STP scorecards), improving retention by 22%",
            "Expanded automated testing for ML pipelines, improving release stability and reducing post-deployment issues",
        ],
        "tech": ["LangChain", "LlamaIndex", "Azure OpenAI", "AWS Bedrock", "GLoVe", "TensorFlow", "HuggingFace", "BigQuery", "GCP", "Streamlit", "Gradio"],
    },
]

# ══════════════════════════════════════════════════════════════════
# COMPONENT BUILDERS
# ══════════════════════════════════════════════════════════════════

def stack_tag(text, accent):
    return html.Span(text, className="stack-tag", style={
        "color": accent,
        "borderColor": f"{accent}44",
        "backgroundColor": f"{accent}0f",
    })


def project_card(p, delay=0):
    icon_is_brand = p["icon"] in ("fa-docker", "fa-python", "fa-react", "fa-aws", "fa-google")
    icon_class = f"fa-brands {p['icon']}" if icon_is_brand else f"fa-solid {p['icon']}"

    live_link = html.A(
        [html.I(className="fa-solid fa-arrow-up-right-from-square"), " Live"],
        href=p["live"], target="_blank",
        className="card-link live",
    ) if p["live"] else html.Span("")

    return html.Div(
        [
            # top row
            html.Div([
                html.Div([
                    html.Div(
                        html.I(className=icon_class),
                        className="card-icon",
                        style={"background": f"{p['accent']}1a", "color": p["accent"]},
                    ),
                    html.Span(p["name"], className="glitch"),
                ], className="card-title"),
                html.Span(p["status"], className="status-badge", style={
                    "color": p["status_color"],
                    "borderColor": f"{p['status_color']}44",
                    "backgroundColor": f"{p['status_color']}10",
                }),
            ], className="card-header"),

            # hackathon
            html.Div([
                html.I(className="fa-solid fa-trophy", style={"fontSize": "10px"}),
                p["hackathon"],
            ], className="hackathon-tag"),

            html.P(p["tagline"], className="card-tagline"),
            html.P(p["description"], className="card-desc"),

            # highlights
            html.Div([
                html.Div([
                    html.I(className="fa-solid fa-chevron-right", style={"color": p["accent"]}),
                    html.Span(h),
                ], className="card-highlight")
                for h in p["highlights"]
            ], className="card-highlights"),

            # stack
            html.Div([stack_tag(s, p["accent"]) for s in p["stack"]], className="card-stack"),

            # links
            html.Div([
                html.A(
                    [html.I(className="fa-brands fa-github"), " Code"],
                    href=p["github"], target="_blank",
                    className="card-link",
                ),
                live_link,
            ], className="card-links"),

            html.Div(className="card-accent-bar", style={
                "background": f"linear-gradient(90deg, {p['accent']}, transparent)",
            }),
        ],
        className=f"project-card reveal reveal-delay-{(delay%4)+1}",
        style={"--card-accent": p["accent"]},
    )


def skill_section(cat):
    return html.Div([
        html.Div(cat["label"], className="skill-cat-label", style={"color": cat["color"]}),
        html.Div([
            html.Div([
                html.I(className=f"fa-brands {ico}" if ico in ("fa-docker","fa-python","fa-react") else f"fa-solid {ico}",
                       style={"color": cat["color"]}),
                html.Span(name),
            ], className="skill-chip",
               style={"borderColor": f"{cat['color']}22"})
            for name, ico in cat["skills"]
        ], className="skill-row"),
    ])


def timeline_item(exp):
    return html.Div([
        html.Div(className="timeline-dot" + (" active" if exp["active"] else ""),
                 style={"borderColor": exp["accent"], "boxShadow": f"0 0 0 4px {exp['accent']}22" if exp["active"] else "none"}),
        html.Div([
            html.Div(exp["company"], className="tl-company", style={"color": exp["accent"]}),
            html.Div(exp["role"], className="tl-role"),
            html.Div(exp["dates"], className="tl-date"),
            html.P(exp["desc"], className="tl-desc"),
            html.Ul([html.Li(b) for b in exp["bullets"]], className="tl-bullets"),
            html.Div([
                html.Span(t, className="tl-tech") for t in exp["tech"]
            ], className="tl-tech-row"),
        ]),
    ], className="timeline-item reveal")


# ══════════════════════════════════════════════════════════════════
# LAYOUT
# ══════════════════════════════════════════════════════════════════

app.layout = html.Div([

    # ── Background layers ──────────────────────────────────────────
    html.Canvas(id="particle-canvas"),
    html.Div(id="grid-scan-bg"),
    html.Div(className="grid-scan-v"),
    html.Div(className="aurora", children=[
        html.Div(className="aurora-blob"),
        html.Div(className="aurora-blob"),
        html.Div(className="aurora-blob"),
    ]),
    html.Div(className="noise-overlay"),

    # ── Page content ───────────────────────────────────────────────
    html.Div([

        # ── NAV ───────────────────────────────────────────────────
        html.Nav([
            html.Div([
                html.Span("abhineet", className="accent"),
                html.Span(".sharma", className="dim"),
            ], className="nav-logo"),
            html.Div([
                html.A("about",      href="#hero"),
                html.A("projects",   href="#projects"),
                html.A("skills",     href="#skills"),
                html.A("experience", href="#experience"),
                html.A("contact",    href="#contact"),
            ], className="nav-links"),
        ], id="navbar"),

        # ── HERO ──────────────────────────────────────────────────
        html.Section([
            html.Div([
                # status pill
                html.Div([
                    html.Span(className="dot"),
                    "Available for freelance & consulting",
                ], className="status-pill reveal"),

                html.Div("// AI Engineer", className="hero-eyebrow reveal reveal-delay-1"),

                html.H1([
                    html.Span("Abhineet "),
                    html.Span("Sharma", className="word-ai glitch"),
                ], className="hero-name reveal reveal-delay-2"),

                html.Div([
                    html.Span(id="typewriter-text"),
                    html.Span(className="typewriter-cursor"),
                ], className="hero-role reveal reveal-delay-2"),

                html.P(
                    "3+ years building production GenAI systems for enterprise. "
                    "LLM fine-tuning, RAG pipelines, multi-agent orchestration, "
                    "and full-stack AI apps — shipped under real deadlines.",
                    className="hero-desc reveal reveal-delay-3",
                ),

                html.Div([
                    html.A(
                        [html.I(className="fa-solid fa-rocket"), " View Projects"],
                        href="#projects", className="btn-primary",
                    ),
                    html.A(
                        [html.I(className="fa-brands fa-github"), " GitHub"],
                        href="https://github.com/divergent99", target="_blank",
                        className="btn-ghost",
                    ),
                ], className="hero-ctas reveal reveal-delay-3"),

                html.Div([
                    html.Div([
                        html.Div("5+", className="stat-num", style={"color": "#6366f1"}),
                        html.Div("Hackathons", className="stat-label"),
                    ]),
                    html.Div([
                        html.Div("3+", className="stat-num", style={"color": "#00ffa3"}),
                        html.Div("Years Experience", className="stat-label"),
                    ]),
                    html.Div([
                        html.Div("2x", className="stat-num", style={"color": "#f59e0b"}),
                        html.Div("Faster Reporting", className="stat-label"),
                    ]),
                    html.Div([
                        html.Div("65%", className="stat-num", style={"color": "#3b82f6"}),
                        html.Div("Query Time Reduction", className="stat-label"),
                    ]),
                ], className="hero-stats reveal reveal-delay-4"),

            ], className="container"),
        ], id="hero"),

        # ── PROJECTS ──────────────────────────────────────────────
        html.Section([
            html.Div([
                html.Div("02. WORK", className="section-label"),
                html.H2("Hackathon Projects", className="section-title"),
                html.P("Production-grade AI systems built under fire — real deadlines, real deployment.", className="section-sub"),
                html.Div(className="title-line"),
                html.Div(
                    [project_card(p, i) for i, p in enumerate(PROJECTS)],
                    className="projects-grid",
                ),
            ], className="container"),
        ], id="projects", className="section"),

        # ── SKILLS ────────────────────────────────────────────────
        html.Section([
            html.Div([
                html.Div("03. STACK", className="section-label"),
                html.H2("Technical Skills", className="section-title"),
                html.P("The full toolkit — from LLM orchestration to production deployment.", className="section-sub"),
                html.Div(className="title-line"),
                html.Div(
                    [skill_section(c) for c in SKILL_CATS],
                    className="skill-categories",
                ),
            ], className="container"),
        ], id="skills", className="section"),

        # ── EXPERIENCE ────────────────────────────────────────────
        html.Section([
            html.Div([
                html.Div("04. EXPERIENCE", className="section-label"),
                html.H2("Work Experience", className="section-title"),
                html.P("3+ years delivering AI in production environments.", className="section-sub"),
                html.Div(className="title-line"),
                html.Div(
                    [timeline_item(e) for e in EXPERIENCE],
                    className="timeline",
                ),
            ], className="container"),
        ], id="experience", className="section"),

        # ── CONTACT ───────────────────────────────────────────────
        html.Section([
            html.Div([
                html.Div("05. CONTACT", className="section-label"),
                html.H2("Let's Build Together", className="section-title"),
                html.P("Open to freelance projects, consulting, and collaborations.", className="section-sub"),
                html.Div(className="title-line"),
                html.Div([
                    # links column
                    html.Div([
                        html.A([
                            html.I(className="fa-brands fa-github", style={"color": "#94a3b8"}),
                            html.Div([
                                html.Div("GitHub", className="contact-link-label"),
                                html.Div("divergent99", className="contact-link-sub"),
                            ]),
                        ], href="https://github.com/divergent99", target="_blank",
                           className="contact-link-item reveal"),

                        html.A([
                            html.I(className="fa-brands fa-linkedin", style={"color": "#0a66c2"}),
                            html.Div([
                                html.Div("LinkedIn", className="contact-link-label"),
                                html.Div("abhineet-sharma-", className="contact-link-sub"),
                            ]),
                        ], href="https://linkedin.com/in/abhineet-sharma-/", target="_blank",
                           className="contact-link-item reveal reveal-delay-1"),

                        html.A([
                            html.I(className="fa-solid fa-envelope", style={"color": "#6366f1"}),
                            html.Div([
                                html.Div("Email", className="contact-link-label"),
                                html.Div("abhineetsharma77@gmail.com", className="contact-link-sub"),
                            ]),
                        ], href="mailto:abhineetsharma77@gmail.com",
                           className="contact-link-item reveal reveal-delay-2"),

                        html.A([
                            html.I(className="fa-solid fa-pen-nib", style={"color": "#94a3b8"}),
                            html.Div([
                                html.Div("Medium Blog", className="contact-link-label"),
                                html.Div("abhineetsharma77", className="contact-link-sub"),
                            ]),
                        ], href="https://abhineetsharma77.medium.com/", target="_blank",
                           className="contact-link-item reveal reveal-delay-3"),

                        html.A([
                            html.I(className="fa-solid fa-store", style={"color": "#f59e0b"}),
                            html.Div([
                                html.Div("PromptBase", className="contact-link-label"),
                                html.Div("akriceus", className="contact-link-sub"),
                            ]),
                        ], href="https://promptbase.com/profile/akriceus", target="_blank",
                           className="contact-link-item reveal reveal-delay-4"),
                    ], className="contact-links"),

                    # CTA card
                    html.Div([
                        html.I(className="fa-solid fa-satellite-dish cta-icon"),
                        html.H3("Open to Projects", className="cta-title"),
                        html.P(
                            "GenAI pipelines, RAG systems, multi-agent architectures, "
                            "and enterprise AI — let's scope something.",
                            className="cta-sub",
                        ),
                        html.A("Get in touch", href="mailto:abhineetsharma77@gmail.com",
                               className="btn-primary"),
                    ], className="contact-cta-card reveal reveal-delay-2"),

                ], className="contact-grid"),
            ], className="container"),
        ], id="contact", className="section"),

        # ── FOOTER ────────────────────────────────────────────────
        html.Footer([
            html.Span("Built with "),
            html.Span("Plotly Dash", className="accent"),
            html.Span(" · Inspired by "),
            html.Span("ReactBits", className="accent"),
            html.Span(" · Abhineet Sharma © 2026"),
        ]),

    ], className="page-wrap"),

], style={"position": "relative"})


if __name__ == "__main__":
    app.run(debug=False, port=8060)
