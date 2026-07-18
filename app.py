import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

app = dash.Dash(
    __name__,
    external_stylesheets=[
        "https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;700&family=Inter:wght@300;400;500;600;700;800&display=swap",
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css",
    ],
    title="Abhineet Sharma | Data Scientist & AI Engineer",
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"},
        {"name": "description", "content": "Data Scientist and AI Engineer specializing in GenAI, LangGraph, RAG pipelines, and multi-agent systems."},
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
    "name": "QuantPulse",
    "hackathon": "AlgoFest Hackathon 2026",
    "status": "Deployed",
    "status_color": "#00ffa3",
    "tagline": "Algorithmic portfolio risk intelligence with terminal aesthetic",
    "description": (
        "Single-day build of a quantitative portfolio risk platform. Combines a "
        "from-scratch risk engine (VaR, Sharpe, Sortino, Beta, CVaR, Max Drawdown) "
        "with a LangGraph agent for natural-language risk queries and live market "
        "news via Tavily — all wrapped in a Bloomberg-style terminal UI."
    ),
    "highlights": [
        "Full quant engine: VaR, CVaR, Sharpe, Sortino, Beta, Max Drawdown",
        "LangGraph agent orchestrating metrics + Tavily news retrieval",
        "9-chart Plotly Dash dashboard with hacker/terminal aesthetic",
        "Shipped end-to-end in a single hackathon day",
    ],
    "stack": ["LangGraph", "Amazon Nova Lite", "Tavily", "Alpha Vantage", "Plotly Dash", "Railway"],
    "github": "https://github.com/divergent99/quantpulse",
    "live": "https://web-production-12187.up.railway.app/",
    "icon": "fa-chart-line",
    "accent": "#ec4899",
},
]

# Deployed projects from the latest public GitHub portfolio refresh.
# The original showcase cards above are intentionally retained.
PROJECTS.extend([
    {
        "name": "ZeroDay", "hackathon": "Cyber Incident Simulation", "status": "Deployed", "status_color": "#00ffa3",
        "tagline": "Cinematic cyber incident command simulator",
        "description": "Triage global infrastructure threats, deploy specialist teams, investigate live intelligence, and make time-critical decisions with branching consequences.",
        "highlights": ["Branching incident scenarios", "Specialist team deployment", "AI-powered live intelligence", "Responsive command-center interface"],
        "stack": ["React", "FastAPI", "AI Agents", "JavaScript"], "github": "https://github.com/divergent99/ZeroDay",
        "live": "https://zero-day-blue.vercel.app/", "icon": "fa-shield-halved", "accent": "#ef4444",
    },
    {
        "name": "Enough", "hackathon": "OpenAI Realtime Experience", "status": "Deployed", "status_color": "#00ffa3",
        "tagline": "A private AI companion for overwhelming days",
        "description": "A privacy-conscious conversational companion designed for moments of grief, panic, and emotional overload, with a calm real-time voice experience.",
        "highlights": ["Realtime voice interaction", "Privacy-conscious experience", "Supportive conversational design", "Low-friction crisis interface"],
        "stack": ["GPT-5.6", "OpenAI Realtime API", "Python", "Railway"], "github": "https://github.com/divergent99/Enough",
        "live": "https://web-production-bc492.up.railway.app/", "icon": "fa-heart", "accent": "#f472b6",
    },
    {
        "name": "PitWall AI", "hackathon": "AI Race Strategy Lab", "status": "Deployed", "status_color": "#00ffa3",
        "tagline": "Explainable Formula 1 race strategy intelligence",
        "description": "Simulates race scenarios, models uncertainty and rival reactions, and uses AI to explain every strategic call like a virtual pit wall.",
        "highlights": ["Race scenario simulation", "Rival reaction modelling", "Uncertainty-aware strategy", "Explainable strategic calls"],
        "stack": ["GPT-5.6", "React", "JavaScript", "Railway"], "github": "https://github.com/divergent99/Pitwall.AI",
        "live": "https://web-production-4f803.up.railway.app/", "icon": "fa-flag-checkered", "accent": "#ef4444",
    },
    {
        "name": "Trade Impact Agent", "hackathon": "Live Agentic Sports Analytics", "status": "Deployed", "status_color": "#00ffa3",
        "tagline": "Real-time agentic NBA trade analysis",
        "description": "A LangGraph agent pulls current rosters, stats, injuries, and news to evaluate and grade NBA trades with evidence-backed analysis.",
        "highlights": ["Live roster and stats retrieval", "Injury and news context", "Evidence-backed trade grades", "Agentic analysis workflow"],
        "stack": ["LangGraph", "Claude", "React", "JavaScript"], "github": "https://github.com/divergent99/trade-impact-agent",
        "live": "https://trade-impact-agent.vercel.app/", "icon": "fa-basketball", "accent": "#f97316",
    },
    {
        "name": "CareerTrack", "hackathon": "Agentic Memory System", "status": "Deployed", "status_color": "#00ffa3",
        "tagline": "A persistent AI memory for your job search",
        "description": "Ingests Gmail and remembers applications, interviews, and rejections, turning a fragmented job hunt into a searchable, context-aware workflow.",
        "highlights": ["Gmail application ingestion", "Persistent job-search memory", "Vector-based semantic retrieval", "Interview and status tracking"],
        "stack": ["CockroachDB", "Vector Search", "MCP", "AWS Bedrock", "React"], "github": "https://github.com/divergent99/CareerTrack",
        "live": "https://career-track-chi.vercel.app/", "icon": "fa-route", "accent": "#3b82f6",
    },
    {
        "name": "CoreMap", "hackathon": "Personalized GenAI Learning", "status": "Deployed", "status_color": "#00ffa3",
        "tagline": "Signal-first roadmap for learning GenAI",
        "description": "Builds personalized learning roadmaps, filters live AI news by signal versus hype, and provides an interactive architecture simulator.",
        "highlights": ["Personalized learning roadmap", "Signal-vs-hype news filtering", "Interactive architecture graphs", "Live AI news retrieval"],
        "stack": ["Next.js", "TypeScript", "Claude Sonnet", "Tavily", "DynamoDB"], "github": "https://github.com/divergent99/coremap",
        "live": "https://coremap.vercel.app/", "icon": "fa-map", "accent": "#8b5cf6",
    },
    {
        "name": "Blast Radius Dashboard", "hackathon": "GitLab Developer Tooling", "status": "Deployed", "status_color": "#00ffa3",
        "tagline": "Visualize merge-request risk before it ships",
        "description": "Maps GitLab merge-request impact through a dependency graph, identifies files at risk, and adds AI-powered codebase exploration.",
        "highlights": ["Merge-request impact analysis", "Interactive dependency graph", "At-risk file identification", "AI codebase chat"],
        "stack": ["React", "Vite", "GitLab Orbit", "Claude", "FastAPI"], "github": "https://github.com/divergent99/blast-radius-dashboard",
        "live": "https://blast-radius-dashboard.vercel.app/", "icon": "fa-circle-nodes", "accent": "#f59e0b",
    },
    {
        "name": "Roast My Portfolio", "hackathon": "AI Investment Experience", "status": "Deployed", "status_color": "#00ffa3",
        "tagline": "Brutally honest AI feedback on your holdings",
        "description": "Upload a portfolio screenshot and receive direct, entertaining analysis that turns a dense set of holdings into clear feedback.",
        "highlights": ["Screenshot-based portfolio input", "AI-generated investment critique", "Fast visual workflow", "Shareable results experience"],
        "stack": ["React", "JavaScript", "Vision AI", "Vercel"], "github": "https://github.com/divergent99/roast-my-portfolio",
        "live": "https://roast-my-portfolio-two.vercel.app/", "icon": "fa-fire-flame-curved", "accent": "#ec4899",
    },
    {
        "name": "Kalam", "hackathon": "Applied GenAI Project", "status": "Deployed", "status_color": "#00ffa3",
        "tagline": "AI-powered preparation companion for IAS aspirants",
        "description": "A focused learning and preparation platform built to help IAS aspirants navigate their civil-services journey with an AI-powered experience.",
        "highlights": ["Designed for IAS aspirants", "AI-assisted preparation", "Focused learning experience", "Production Railway deployment"],
        "stack": ["Python", "AI", "Railway"], "github": "https://github.com/divergent99/Kalam",
        "live": "https://kalam-prod-test.up.railway.app/", "icon": "fa-pen-fancy", "accent": "#14b8a6",
    },
    {
        "name": "GenAI Guide", "hackathon": "GenAI Learning Resource", "status": "Deployed", "status_color": "#00ffa3",
        "tagline": "A practical field guide to generative AI",
        "description": "An accessible, web-based guide that organizes core generative-AI concepts into a practical learning experience.",
        "highlights": ["Structured GenAI learning path", "Web-first reference experience", "Practical concept breakdowns", "Production Railway deployment"],
        "stack": ["HTML", "CSS", "JavaScript", "Railway"], "github": "https://github.com/divergent99/GenAI-Guide",
        "live": "https://genai-guide-production.up.railway.app/", "icon": "fa-book-open", "accent": "#06b6d4",
    },
])

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
        "role": "Data Scientist",
        "company": "GEDU Services",
        "company_url": "https://geduservices.com/",
        "dates": "Jul 2026 — Present",
        "accent": "#00ffa3",
        "active": True,
        "desc": "Working as a Data Scientist at GEDU Services, supporting data-led innovation across a global education services organization.",
        "bullets": [],
        "tech": ["Data Science", "Machine Learning", "Generative AI", "Python"],
    },
    {
        "role": "Associate (AI Engineer)",
        "company": "Alvarez & Marsal",
        "company_url": "https://www.alvarezandmarsal.com",
        "dates": "Jan 2025 — May 2026",
        "accent": "#6366f1",
        "active": False,
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

                html.Div("// Data Scientist & AI Engineer", className="hero-eyebrow reveal reveal-delay-1"),

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
                        html.Div("10+", className="stat-num", style={"color": "#6366f1"}),
                        html.Div("Hackathons", className="stat-label"),
                    ]),
                    html.Div([
                        html.Div("3.5+", className="stat-num", style={"color": "#00ffa3"}),
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
                html.H2("Selected AI Projects", className="section-title"),
                html.P("Deployed products and hackathon systems — built under real deadlines and shipped to production.", className="section-sub"),
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
