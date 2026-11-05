import dash
from dash import html

# ══════════════════════════════════════════════════════════════════
# APP
# ══════════════════════════════════════════════════════════════════

FONTS = (
    "https://fonts.googleapis.com/css2?"
    "family=Shippori+Mincho:wght@500;700;800"
    "&family=Inter:wght@300;400;500;600;700"
    "&family=JetBrains+Mono:wght@400;500;700&display=swap"
)

app = dash.Dash(
    __name__,
    external_stylesheets=[
        FONTS,
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css",
    ],
    title="Abhineet Sharma | Data Scientist & AI Engineer",
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1, viewport-fit=cover"},
        {"name": "description", "content": "Abhineet Sharma, Data Scientist and AI Engineer with 4+ years building GenAI systems: LangGraph agents, RAG pipelines, and production ML."},
        {"name": "theme-color", "content": "#070b14"},
        {"property": "og:title", "content": "Abhineet Sharma | Data Scientist & AI Engineer"},
        {"property": "og:description", "content": "4+ years shipping GenAI, RAG and multi-agent systems. Built in the rain."},
        {"property": "og:image", "content": "/assets/img/og.jpg"},
        {"name": "twitter:card", "content": "summary_large_image"},
    ],
    suppress_callback_exceptions=True,
)
server = app.server

# The page is server-rendered to plain HTML (see render_page at the bottom).

# ══════════════════════════════════════════════════════════════════
# DATA
# ══════════════════════════════════════════════════════════════════

YEARS = "4+"

PROJECTS = [
    {
        "name": "VaultDesk", "hackathon": "Auth0 'Authorized to Act' Hackathon", "status": "Deployed",
        "tagline": "AI-powered M&A deal room with guardian push approvals",
        "description": "Enterprise-grade M&A deal room assistant built on Auth0 Token Vault. CIBA Guardian push approval before any email or calendar action, a LangGraph multi-agent backend, and a 28-file modular architecture on Railway.",
        "highlights": ["CIBA Guardian push approval before sensitive actions", "Gmail + Calendar tools via Auth0 Token Vault", "Single-process FastAPI + Dash via WSGIMiddleware"],
        "stack": ["LangGraph", "Auth0 Token Vault", "Amazon Nova Lite", "FastAPI", "Dash", "Gmail API"],
        "github": "https://github.com/divergent99/vaultdesk", "live": "https://vaultdesk-production.up.railway.app",
        "icon": "fa-vault", "tags": "agents finance",
    },
    {
        "name": "QuantPulse", "hackathon": "AlgoFest Hackathon 2026", "status": "Deployed",
        "tagline": "Algorithmic portfolio risk intelligence, terminal style",
        "description": "Single-day build of a quant risk platform. A from-scratch risk engine (VaR, CVaR, Sharpe, Sortino, Beta, Max Drawdown) plus a LangGraph agent for natural-language risk queries and live market news via Tavily.",
        "highlights": ["Full quant engine built from scratch", "LangGraph agent orchestrating metrics + news", "9-chart Bloomberg-style Dash dashboard"],
        "stack": ["LangGraph", "Amazon Nova Lite", "Tavily", "Alpha Vantage", "Plotly Dash", "Railway"],
        "github": "https://github.com/divergent99/quantpulse", "live": "https://web-production-12187.up.railway.app/",
        "icon": "fa-chart-line", "tags": "agents finance",
    },
    {
        "name": "Verdikt", "hackathon": "HackHazards '26", "status": "Submitted",
        "tagline": "Parallel analyst council for multi-perspective due diligence",
        "description": "Five specialist agents (Legal, Financial, Market, Ops, Risk) analyze deals concurrently on Groq. A Senior Partner agent consolidates everything into a structured investment thesis.",
        "highlights": ["5 parallel specialists + synthesis layer", "Groq llama-3.3-70b for sub-second inference", "SentenceTransformers semantic chunking"],
        "stack": ["Groq llama-3.3-70b", "LangGraph", "ChromaDB", "SentenceTransformers", "Dash", "FastAPI"],
        "github": "https://github.com/divergent99/verdikt", "live": None,
        "icon": "fa-scale-balanced", "tags": "agents finance rag",
    },
    {
        "name": "Change Impact Lab", "hackathon": "Jira Change Intelligence", "status": "Deployed",
        "tagline": "Know what a Jira change could break before the sprint does",
        "description": "A read-only change-intelligence workspace that traverses direct and downstream Jira relationships, shows the evidence behind every connection, and answers grounded questions about the visible work.",
        "highlights": ["Deterministic blast-radius traversal", "Evidence-backed relationship graph", "Grounded chat with Jira citations"],
        "stack": ["Next.js 16", "React 19", "Jira Cloud API", "OpenAI Responses API", "TypeScript"],
        "github": "https://github.com/divergent99/ImpactLab", "live": "https://impactlab-production.up.railway.app/",
        "icon": "fa-arrows-to-circle", "tags": "devtools agents",
    },
    {
        "name": "NovaDD", "hackathon": "Amazon Nova AI Hackathon", "status": "Submitted",
        "tagline": "M&A due diligence RAG pipeline with extended thinking",
        "description": "Multi-agent virtual data room intelligence. Deal documents flow through a ChromaDB RAG pipeline and surface as structured diligence insights, powered by Amazon Bedrock Nova 2 with Extended Thinking.",
        "highlights": ["Bedrock Nova 2 Lite with Extended Thinking", "ChromaDB semantic document retrieval", "Team of 4, collaborative build"],
        "stack": ["Amazon Bedrock Nova 2", "LangGraph", "ChromaDB", "FastAPI", "Dash"],
        "github": "https://github.com/divergent99/VDR-Intelligence", "live": None,
        "icon": "fa-magnifying-glass-chart", "tags": "agents finance rag",
    },
    {
        "name": "Blast Radius Dashboard", "hackathon": "GitLab Transcend Hackathon", "status": "Deployed",
        "tagline": "See merge-request risk before it ships",
        "description": "Maps GitLab merge-request impact through a dependency graph, flags at-risk files, and adds AI-powered codebase exploration.",
        "highlights": ["Merge-request impact analysis", "Interactive dependency graph", "AI codebase chat"],
        "stack": ["React", "Vite", "GitLab Orbit", "Claude", "FastAPI"],
        "github": "https://github.com/divergent99/blast-radius-dashboard", "live": "https://blast-radius-dashboard.vercel.app/",
        "icon": "fa-circle-nodes", "tags": "devtools",
    },
    {
        "name": "CareerTrack", "hackathon": "Agentic Memory System", "status": "Deployed",
        "tagline": "A persistent AI memory for your job search",
        "description": "Ingests Gmail and remembers applications, interviews and rejections, turning a scattered job hunt into a searchable, context-aware workflow.",
        "highlights": ["Gmail application ingestion", "Vector-based semantic retrieval", "Interview and status tracking"],
        "stack": ["CockroachDB", "Vector Search", "MCP", "AWS Bedrock", "React"],
        "github": "https://github.com/divergent99/CareerTrack", "live": "https://career-track-chi.vercel.app/",
        "icon": "fa-route", "tags": "agents rag",
    },
    {
        "name": "Trade Impact Agent", "hackathon": "Live Agentic Sports Analytics", "status": "Deployed",
        "tagline": "Real-time agentic NBA trade analysis",
        "description": "A LangGraph agent pulls live rosters, stats, injuries and news to evaluate and grade NBA trades with evidence-backed analysis.",
        "highlights": ["Live roster and stats retrieval", "Injury and news context", "Evidence-backed trade grades"],
        "stack": ["LangGraph", "Claude", "React", "JavaScript"],
        "github": "https://github.com/divergent99/trade-impact-agent", "live": "https://trade-impact-agent.vercel.app/",
        "icon": "fa-basketball", "tags": "agents play",
    },
    {
        "name": "PitWall AI", "hackathon": "AI Race Strategy Lab", "status": "Deployed",
        "tagline": "Explainable Formula 1 race strategy intelligence",
        "description": "Simulates race scenarios, models uncertainty and rival reactions, and explains every strategic call like a virtual pit wall.",
        "highlights": ["Race scenario simulation", "Rival reaction modelling", "Explainable strategic calls"],
        "stack": ["GPT-5.6", "React", "JavaScript", "Railway"],
        "github": "https://github.com/divergent99/Pitwall.AI", "live": "https://web-production-4f803.up.railway.app/",
        "icon": "fa-flag-checkered", "tags": "play",
    },
    {
        "name": "ZeroDay", "hackathon": "Cyber Incident Simulation", "status": "Deployed",
        "tagline": "Cinematic cyber incident command simulator",
        "description": "Triage global infrastructure threats, deploy specialist teams, investigate live intelligence, and make time-critical calls with branching consequences.",
        "highlights": ["Branching incident scenarios", "Specialist team deployment", "AI-powered live intelligence"],
        "stack": ["React", "FastAPI", "AI Agents", "JavaScript"],
        "github": "https://github.com/divergent99/ZeroDay", "live": "https://zero-day-blue.vercel.app/",
        "icon": "fa-shield-halved", "tags": "play agents",
    },
    {
        "name": "VDR Voice Intelligence", "hackathon": "Gemini Live Agent Challenge", "status": "Built",
        "tagline": "Voice-first document intelligence via Gemini Live",
        "description": "Analysts speak their questions and get spoken + visual answers back. A real-time WebSocket audio pipeline streams Gemini Live responses straight into the UI. No keyboard required.",
        "highlights": ["Gemini Live API real-time voice", "Bi-directional WebSocket audio", "Voice + visual diligence output"],
        "stack": ["Gemini Live API", "WebSocket", "FastAPI", "Dash", "Google Cloud Run"],
        "github": None, "live": None,
        "icon": "fa-microphone-lines", "tags": "voice finance",
    },
    {
        "name": "Enough", "hackathon": "OpenAI Realtime Experience", "status": "Deployed",
        "tagline": "A private AI companion for overwhelming days",
        "description": "A privacy-conscious conversational companion for moments of grief, panic and overload, with a calm real-time voice experience.",
        "highlights": ["Realtime voice interaction", "Privacy-conscious by design", "Low-friction crisis interface"],
        "stack": ["GPT-5.6", "OpenAI Realtime API", "Python", "Railway"],
        "github": "https://github.com/divergent99/Enough", "live": "https://web-production-bc492.up.railway.app/",
        "icon": "fa-heart", "tags": "voice",
    },
    {
        "name": "CoreMap", "hackathon": "Personalized GenAI Learning", "status": "Deployed",
        "tagline": "Signal-first roadmap for learning GenAI",
        "description": "Builds personalized learning roadmaps, filters live AI news by signal versus hype, and ships an interactive architecture simulator.",
        "highlights": ["Personalized learning roadmap", "Signal-vs-hype news filtering", "Interactive architecture graphs"],
        "stack": ["Next.js", "TypeScript", "Claude Sonnet", "Tavily", "DynamoDB"],
        "github": "https://github.com/divergent99/coremap", "live": "https://coremap.vercel.app/",
        "icon": "fa-map", "tags": "learning agents",
    },
    {
        "name": "Roast My Portfolio", "hackathon": "AI Investment Experience", "status": "Deployed",
        "tagline": "Brutally honest AI feedback on your holdings",
        "description": "Upload a portfolio screenshot, get direct and entertaining analysis that turns a dense set of holdings into clear feedback.",
        "highlights": ["Screenshot-based portfolio input", "AI-generated investment critique", "Shareable results"],
        "stack": ["React", "JavaScript", "Vision AI", "Vercel"],
        "github": "https://github.com/divergent99/roast-my-portfolio", "live": "https://roast-my-portfolio-two.vercel.app/",
        "icon": "fa-fire-flame-curved", "tags": "finance play",
    },
    {
        "name": "Kalam", "hackathon": "Applied GenAI Project", "status": "Deployed",
        "tagline": "AI preparation companion for IAS aspirants",
        "description": "A focused preparation platform that helps IAS aspirants navigate the civil-services journey with an AI-powered study experience.",
        "highlights": ["Designed for IAS aspirants", "AI-assisted preparation", "Production Railway deploy"],
        "stack": ["Python", "AI", "Railway"],
        "github": "https://github.com/divergent99/Kalam", "live": "https://kalam-prod-test.up.railway.app/",
        "icon": "fa-pen-fancy", "tags": "learning",
    },
    {
        "name": "GenAI Guide", "hackathon": "GenAI Learning Resource", "status": "Deployed",
        "tagline": "A practical field guide to generative AI",
        "description": "A web-first guide that organizes core generative-AI concepts into a practical, structured learning path.",
        "highlights": ["Structured GenAI learning path", "Practical concept breakdowns", "Production Railway deploy"],
        "stack": ["HTML", "CSS", "JavaScript", "Railway"],
        "github": "https://github.com/divergent99/GenAI-Guide", "live": "https://genai-guide-production.up.railway.app/",
        "icon": "fa-book-open", "tags": "learning",
    },
]

FILTERS = [
    ("all", "All"), ("agents", "Agents"), ("finance", "Finance"), ("rag", "RAG"),
    ("devtools", "Dev Tools"), ("voice", "Voice"), ("play", "Play"), ("learning", "Learning"),
]

# icon key -> (label, brand hex used on hover). SVGs live in assets/icons/<key>.svg
ICONS = {
    "langgraph": "#4FB3A9", "langchain": "#7FC8FF", "llamaindex": "#E66BC1", "crewai": "#FF5A50",
    "mcp": "#E7E2D6", "claudecode": "#D97757", "codex": "#E7E2D6", "claude": "#D97757",
    "azure": "#0089D6", "bedrock": "#01A88D", "gemini": "#8E75B2", "groq": "#F55036",
    "huggingface": "#FFD21E", "openai": "#E7E2D6", "ollama": "#E7E2D6", "gcp": "#4285F4",
    "chroma": "#FFDE2D", "postgresql": "#6B9BE8", "duckdb": "#FFF000", "bigquery": "#669DF6",
    "pandas": "#E70488", "numpy": "#4DABCF", "sklearn": "#F7931E", "tensorflow": "#FF6F00",
    "python": "#FFD43B", "fastapi": "#05A28F", "docker": "#2496ED", "githubactions": "#2088FF",
    "railway": "#E7E2D6", "vercel": "#E7E2D6", "selenium": "#43B02A", "plotly": "#7A76FF",
    "streamlit": "#FF4B4B", "gradio": "#F97316", "react": "#61DAFB", "nextjs": "#E7E2D6",
    "vite": "#9135FF", "tailwind": "#06B6D4", "threejs": "#E7E2D6", "typescript": "#3178C6",
    "aws": "#FF9900", "tavily": "#8FB5FF", "github": "#E7E2D6", "linkedin": "#0A66C2",
    "medium": "#E7E2D6", "gmail": "#EA4335", "hackerrank": "#00EA64",
}

SKILL_CATS = [
    {"label": "Agents & Orchestration", "kanji": "策", "skills": [
        ("LangGraph", "langgraph"), ("LangChain", "langchain"), ("LlamaIndex", "llamaindex"),
        ("CrewAI", "crewai"), ("MCP", "mcp"), ("Claude Code", "claudecode"), ("Codex", "codex")]},
    {"label": "Models & Cloud", "kanji": "雲", "skills": [
        ("Claude API", "claude"), ("Azure OpenAI", "azure"), ("AWS Bedrock", "bedrock"),
        ("Gemini", "gemini"), ("Groq", "groq"), ("Hugging Face", "huggingface"),
        ("Whisper", "openai"), ("Ollama", "ollama")]},
    {"label": "RAG & Retrieval", "kanji": "蔵", "skills": [
        ("ChromaDB", "chroma"), ("pgvector", "postgresql"), ("DuckDB", "duckdb"),
        ("BigQuery", "bigquery"), ("LlamaIndex", "llamaindex"), ("Tavily", "tavily")]},
    {"label": "Data & ML", "kanji": "学", "skills": [
        ("Pandas", "pandas"), ("NumPy", "numpy"), ("scikit-learn", "sklearn"),
        ("TensorFlow", "tensorflow"), ("Hugging Face", "huggingface")]},
    {"label": "Backend & Infra", "kanji": "鍛", "skills": [
        ("Python", "python"), ("FastAPI", "fastapi"), ("Docker", "docker"), ("GitHub Actions", "githubactions"),
        ("Railway", "railway"), ("Vercel", "vercel"), ("Google Cloud", "gcp"), ("Selenium", "selenium")]},
    {"label": "Frontend", "kanji": "画", "skills": [
        ("Plotly Dash", "plotly"), ("Streamlit", "streamlit"), ("Gradio", "gradio"), ("React", "react"),
        ("Next.js", "nextjs"), ("TypeScript", "typescript"), ("Vite", "vite"), ("Tailwind", "tailwind")]},
]

ALSO_FLUENT = ["Docling", "MinerU", "Pytesseract", "Librosa", "RAGAS", "DeepEval", "XGBoost",
               "SSE streaming", "Text-to-SQL", "Fine-tuning", "RFM / CLV", "Churn & uplift"]

EXPERIENCE = [
    {
        "role": "Data Scientist", "company": "GEDU Services", "company_url": "https://geduservices.com/",
        "dates": "Jul 2026 – Present", "place": "Noida", "active": True,
        "desc": "Building production GenAI across a global education services group.",
        "bullets": [
            "Built and deployed an agentic RAG chatbot for Global Banking School: LangGraph pipeline, recursive crawling, PDF/table extraction and ChromaDB retrieval over 450+ pages",
            "Engineered citation-first, self-checking answers streamed in real time over FastAPI SSE",
            "Built a review-intelligence pipeline across 8+ platforms and 12 portfolio schools, combining VADER and Claude Haiku sentiment with a React/D3 leadership dashboard",
            "Authored the GenAI executive briefing and use-case roadmap for leadership: coverage-gap matrix, competitor benchmarking, data governance and PII",
            "Prototyped a LangGraph Microsoft Teams agent answering Jira sprint queries (status, blockers, standup digests)",
        ],
        "tech": ["LangGraph", "FastAPI", "ChromaDB", "Claude API", "Azure Bot Service", "Jira API"],
    },
    {
        "role": "AI Engineer (Associate)", "company": "Alvarez & Marsal", "company_url": "https://www.alvarezandmarsal.com",
        "dates": "Jan 2025 – May 2026", "place": "Gurugram · GCC AI Team", "active": False,
        "desc": "Production GenAI for Private Equity and M&A advisory deal teams.",
        "bullets": [
            "Automated end-to-end CDD deck generation (Docling → Azure OpenAI extraction → python-pptx), cutting analyst prep time by 60% per engagement",
            "Built a production RAG service (FastAPI, PyMuPDF, pgvector, Azure OpenAI) with hierarchy-preserving chunking, validated with RAGAS and DeepEval",
            "Developed RAPID, a text-to-SQL analytics engine (LangGraph, DuckDB) with semantic caching, follow-up detection and SSE streaming, aligned to Power BI / DAX",
            "Shipped LangGraph conversational agents for real-time portfolio metrics, powering 20+ executive briefings per quarter",
            "Engineered OCR + ASR ingestion (Whisper, Pytesseract, Docling), improving data capture accuracy by 35%",
            "Designed a three-phase vendor normalization pipeline with embedding clustering, cutting procurement cycle time from 4 weeks to 2",
        ],
        "tech": ["LangGraph", "LangChain", "Azure OpenAI", "FastAPI", "Docker", "DuckDB", "pgvector", "RAGAS", "DeepEval"],
    },
    {
        "role": "Data Scientist", "company": "Newgen Software", "company_url": "https://www.newgensoft.com",
        "dates": "Oct 2022 – Dec 2024", "place": "Noida", "active": False,
        "desc": "Enterprise GenAI, recommendations and classical ML for e-commerce and BFSI clients.",
        "bullets": [
            "Built LumYn and Harper, enterprise GenAI apps with RAG and multi-agent LangChain workflows, reducing query time by 65%",
            "Developed an embedding-based recommendation engine (GLoVe + product catalog), lifting relevance and CTR by 18%",
            "Built a contact-center analytics pipeline: Whisper ASR + Librosa signal processing + LLM summarization",
            "Delivered a classical ML suite (RFM, CLV, forecasting, churn, uplift, STP scorecards), improving retention and scoring by 22%",
        ],
        "tech": ["LangChain", "LlamaIndex", "Azure OpenAI", "AWS Bedrock", "Whisper", "TensorFlow", "BigQuery", "GCP"],
    },
]

CODE = [
    ("誠", "makoto", "Grounded, not guessed",
     "Citation-first answers, golden datasets, RAGAS and DeepEval. If the agent can't show its source, it doesn't get to talk."),
    ("勇", "yū", "Ship under pressure",
     "10+ hackathons, several built in a single day. Deadlines are just weather. You walk through them."),
    ("道", "dō", "Production is the path",
     "Demos are cheap. FastAPI, Docker, CI/CD and real users are where the craft actually lives."),
]

UNIVAI_MODULES = ["AI-1 · AI & ML basics", "AI-2 · CNNs", "AI-3 · Language models", "AI-4 · RL & GANs",
                  "DS-1 · Data science", "DS-2 · Trees & ensembles"]

# LinkedIn posts to embed, newest first (share URNs from LinkedIn's "Embed this post")
POSTS = [  # (share id, height from LinkedIn's embed code)
    ("7449118803113930753", 1412),
    ("7443719970334715904", 1237),
    ("7285357114158411777", 1078),
    ("7268924245546549248", 984),
]

CASES = [
    {
        "org": "GEDU Services · Global Banking School", "year": "2026", "status": "In production",
        "title": "GBS Assistant",
        "problem": "Students and staff were digging through 450+ pages of site content and PDFs to find course, fee and admissions answers.",
        "build": "LangGraph pipeline with recursive site crawling, PDF and table extraction, and ChromaDB retrieval on domain-tuned embeddings. Answers are citation-first and self-checked before they stream out over FastAPI SSE.",
        "metric": "453", "metric_label": "pages indexed, every answer cited",
        "facts": [("768", "dim embeddings, nomic-embed v1.5"), ("2", "source types: site + PDFs"),
                  ("1", "self-check pass per answer"), ("SSE", "streamed token by token")],
        "term_title": "gbs · illustrative query",
        "terminal": [
            ("q", "What are the entry requirements for the business degree?"),
            ("info", "retrieve: top-k chunks from ChromaDB"),
            ("sql", "[1] admissions / undergraduate entry"),
            ("sql", "[2] course page / requirements table"),
            ("info", "self-check: grounded in sources ✓"),
            ("ok", "streaming answer with 2 citations…"),
        ],
        "graph": "gbs",
        "decisions": [
            "Citation-first generation, so every answer can be checked against its source page",
            "Self-check before streaming: ungrounded drafts go back for another retrieval pass",
            "Domain-tuned embeddings, so course and fee terminology retrieves cleanly",
        ],
        "stack": ["LangGraph", "ChromaDB", "FastAPI", "Claude API"],
    },
    {
        "org": "Alvarez & Marsal · PE / M&A advisory", "year": "2025", "status": "Shipped to deal teams",
        "title": "CDD deck automation",
        "problem": "Analysts hand-built commercial due diligence decks from data-room documents on every engagement.",
        "build": "Docling parses the documents, Azure OpenAI extracts the facts, and python-pptx renders a finished deck in the firm's format.",
        "metric": "60%", "metric_label": "less analyst prep time per engagement",
        "facts": [("3", "stages: parse, extract, render"), ("50%+", "analyst effort cut across A&M builds"),
                  ("35%", "better data capture in OCR + ASR ingestion"), ("PPTX", "native, editable slides")],
        "term_title": "cdd · illustrative run",
        "terminal": [
            ("q", "build_deck --engagement target_co"),
            ("info", "docling: parsing data room documents"),
            ("sql", "market_size      → extracted"),
            ("sql", "competitor_set   → extracted"),
            ("sql", "customer_mix     → extracted"),
            ("ok", "python-pptx → CDD_deck.pptx ready for review"),
        ],
        "graph": "cdd",
        "decisions": [
            "Parse with Docling first, so the LLM sees structured sections and tables, not raw PDF text",
            "Extract to a structured fact sheet before rendering, one source of truth for every slide",
            "Render native PPTX, so analysts edit slides instead of rebuilding them",
        ],
        "stack": ["Docling", "Azure OpenAI", "python-pptx", "FastAPI"],
    },
    {
        "org": "Alvarez & Marsal · Portfolio analytics", "year": "2025", "status": "Shipped to deal teams",
        "title": "RAPID text-to-SQL",
        "problem": "Deal teams needed portfolio numbers on demand without writing SQL, and the answers had to match the Power BI dashboards exactly.",
        "build": "LangGraph agent over DuckDB with Azure OpenAI, semantic caching, follow-up question detection and SSE streaming. Calculations are aligned to the existing Power BI / DAX definitions.",
        "metric": "DAX", "metric_label": "aligned, so the numbers match the dashboards",
        "facts": [("5", "pipeline stages"), ("1", "semantic cache in front of the LLM"),
                  ("SSE", "streamed answers"), ("0", "SQL written by the analyst")],
        "term_title": "rapid · illustrative query",
        "terminal": [
            ("q", "Revenue trend for Portfolio Co. B, last 4 quarters?"),
            ("info", "follow-up: no · cache: miss"),
            ("sql", "SELECT quarter, SUM(revenue) AS revenue"),
            ("sql", "FROM fact_financials WHERE company = 'B'"),
            ("sql", "GROUP BY quarter ORDER BY quarter DESC LIMIT 4;"),
            ("ok", "DuckDB → DAX-aligned answer streaming…"),
        ],
        "graph": "rapid",
        "decisions": [
            "Reuse the Power BI / DAX metric definitions, so answers never disagree with the dashboards",
            "Semantic cache in front of the LLM, so repeat questions skip generation entirely",
            "Follow-up detection keeps context, so \"and last year?\" just works",
        ],
        "stack": ["LangGraph", "DuckDB", "Azure OpenAI", "FastAPI"],
    },
]

# ══════════════════════════════════════════════════════════════════
# COMPONENT BUILDERS
# ══════════════════════════════════════════════════════════════════

STACK_ICON_RULES = [
    ("langgraph", "langgraph"), ("langchain", "langchain"), ("fastapi", "fastapi"), ("dash", "plotly"),
    ("chroma", "chroma"), ("next.js", "nextjs"), ("react", "react"), ("typescript", "typescript"),
    ("claude", "claude"), ("tavily", "tavily"), ("railway", "railway"), ("vercel", "vercel"),
    ("groq", "groq"), ("gemini", "gemini"), ("nova", "bedrock"), ("bedrock", "bedrock"),
    ("python", "python"), ("vite", "vite"), ("openai", "openai"), ("gpt", "openai"),
    ("gmail", "gmail"), ("cloud run", "gcp"), ("mcp", "mcp"), ("sentencetransformers", "huggingface"),
    ("docker", "docker"), ("duckdb", "duckdb"), ("pgvector", "postgresql"), ("azure", "azure"),
    ("whisper", "openai"), ("tensorflow", "tensorflow"), ("bigquery", "bigquery"), ("gcp", "gcp"),
    ("llamaindex", "llamaindex"),
]


def icon_for(name):
    n = name.lower()
    for key, ico in STACK_ICON_RULES:
        if key in n:
            return ico
    return None


def brand_icon(key, cls="bi"):
    return html.Span(className=cls, style={
        "WebkitMaskImage": f"url(/assets/icons/{key}.svg)",
        "maskImage": f"url(/assets/icons/{key}.svg)",
        "--brand": ICONS.get(key, "#E7E2D6"),
    }, **{"aria-hidden": "true"})


def stack_tag(text):
    ico = icon_for(text)
    kids = [brand_icon(ico, "bi bi-sm"), html.Span(text)] if ico else [html.Span(text)]
    return html.Span(kids, className="stack-tag")


def section_head(num, kanji, label, title, sub):
    return html.Div([
        html.Div(kanji, className="section-kanji", **{"aria-hidden": "true"}),
        html.Div([html.Span(num, className="num"), html.Span(label)], className="section-label"),
        html.H2(title, className="section-title"),
        html.P(sub, className="section-sub"),
        html.Div(className="brush-line"),
    ], className="section-head reveal")


def project_card(p, i):
    status_cls = {"Deployed": "live", "Submitted": "sub", "Built": "built"}[p["status"]]
    links = []
    if p["github"]:
        links.append(html.A([html.I(className="fa-brands fa-github"), " Code"], href=p["github"],
                            target="_blank", rel="noopener", className="card-link"))
    if p["live"]:
        links.append(html.A([html.I(className="fa-solid fa-arrow-up-right-from-square"), " Live"],
                            href=p["live"], target="_blank", rel="noopener", className="card-link primary"))
    return html.Article([
        html.Div(className="card-glow"),
        html.Div([
            html.Div([
                html.Div(html.I(className=f"fa-solid {p['icon']}"), className="card-icon"),
                html.Div([
                    html.H3(p["name"], className="card-name"),
                    html.Div([html.I(className="fa-solid fa-trophy"), p["hackathon"]], className="hackathon-tag"),
                ]),
            ], className="card-title"),
            html.Span(p["status"], className=f"status-badge {status_cls}"),
        ], className="card-header"),
        html.P(p["tagline"], className="card-tagline"),
        html.P(p["description"], className="card-desc"),
        html.Ul([html.Li(h) for h in p["highlights"]], className="card-highlights"),
        html.Div([stack_tag(s) for s in p["stack"]], className="card-stack"),
        html.Div(links, className="card-links"),
    ], className="project-card reveal", **{
        "data-tags": p["tags"], "data-live": "1" if p["live"] else "0", "data-index": str(i),
    })


def case_card(c, i):
    side = [
        html.Div(c["metric"], className="case-metric"),
        html.Div(c["metric_label"], className="case-metric-label"),
    ]
    if c.get("facts"):
        side.append(html.Div([
            html.Div([html.Div(n, className="fact-num"), html.Div(l, className="fact-label")], className="fact")
            for n, l in c["facts"]
        ], className="case-facts"))
    if c.get("terminal"):
        side.append(html.Div([
            html.Div([html.Span(className="tdot"), html.Span(className="tdot"), html.Span(className="tdot"),
                      html.Span(c["term_title"], className="tterm-title")], className="tterm-bar"),
            html.Div([html.Div(t, className=f"tline t-{k}", **{"data-text": t}) for k, t in c["terminal"]],
                     className="tterm-body"),
        ], className="tterm"))
    if c.get("bars"):
        side.append(html.Div([
            html.Div([
                html.Div([html.Span(label), html.Span(f"{v}%", className="bar-v")], className="bar-head"),
                html.Div(html.Div(className="bar-fill" + (" after" if j else ""), style={"--w": f"{v}%"}), className="bar-track"),
            ], className="bar")
            for j, (label, v) in enumerate(c["bars"])
        ], className="case-bars"))
    return html.Article([
        html.Div([
            html.Div([html.Span(f"0{i+1}", className="case-num"), html.Span(c["org"])], className="case-org"),
            html.H3(c["title"], className="case-title"),
            html.Div([html.Span(className="dot"), c["status"], html.Span(" · " + c["year"], className="dim")], className="case-status"),
            html.Div([
                html.Div([html.Div("Problem", className="case-k"), html.P(c["problem"])], className="case-block"),
                html.Div([html.Div("Build", className="case-k"), html.P(c["build"])], className="case-block"),
            ], className="case-body"),
            html.Div([
                html.Div("Key decisions", className="case-k"),
                html.Ul([html.Li(d) for d in c["decisions"]], className="case-decisions"),
            ], className="case-block decisions-block"),
            html.Div([stack_tag(t) for t in c["stack"]], className="card-stack"),
        ], className="case-main"),
        html.Div(side, className="case-side"),
        html.Div([
            html.Div([html.Span("Architecture", className="case-k"), html.Span("live data flow", className="arch-live")], className="arch-head"),
            html.Div(className="case-graph", **{"data-graph": c["graph"]}),
        ], className="case-arch"),
    ], className="case-card reveal")


def skill_section(cat):
    return html.Div([
        html.Div([html.Span(cat["kanji"], className="skill-kanji"), html.Span(cat["label"])],
                 className="skill-cat-label"),
        html.Div([
            html.Div([brand_icon(ico), html.Span(name)], className="skill-chip", title=name)
            for name, ico in cat["skills"]
        ], className="skill-row"),
    ], className="skill-cat reveal")


def timeline_item(exp):
    return html.Div([
        html.Div(className="tl-dot" + (" active" if exp["active"] else "")),
        html.Div([
            html.Div([
                html.Div([
                    html.A(exp["company"], href=exp["company_url"], target="_blank", rel="noopener", className="tl-company"),
                    html.Div(exp["role"], className="tl-role"),
                ]),
                html.Div([html.Div(exp["dates"], className="tl-date"), html.Div(exp["place"], className="tl-place")],
                         className="tl-meta"),
            ], className="tl-head"),
            html.P(exp["desc"], className="tl-desc"),
            html.Ul([html.Li(b) for b in exp["bullets"]], className="tl-bullets"),
            html.Div([html.Span(t, className="tl-tech") for t in exp["tech"]], className="tl-tech-row"),
        ], className="tl-card"),
    ], className="timeline-item reveal")


def stat(target, suffix, label, prefix=""):
    return html.Div([
        html.Div(f"{prefix}{target}{suffix}", className="stat-num",
                 **{"data-count": str(target), "data-suffix": suffix, "data-prefix": prefix}),
        html.Div(label, className="stat-label"),
    ], className="stat")


def contact_link(icon_key, label, sub, href, extra=None):
    return html.A([
        brand_icon(icon_key, "bi bi-lg"),
        html.Div([html.Div(label, className="contact-link-label"), html.Div(sub, className="contact-link-sub")]),
        html.I(className="fa-solid fa-arrow-right contact-arrow"),
    ], href=href, target="_blank", rel="noopener", className="contact-link-item reveal", **(extra or {}))


# ══════════════════════════════════════════════════════════════════
# LAYOUT
# ══════════════════════════════════════════════════════════════════

NAV = [("way", "Way"), ("cases", "Cases"), ("projects", "Work"), ("skills", "Arsenal"), ("experience", "Path"), ("posts", "Notes"), ("contact", "Contact")]

app.layout = html.Div(id="ronin-root", children=[

    # ── Ambient layers (driven by assets/main.js) ──────────────────
    html.Canvas(id="rain"),
    html.Div(id="flash"),
    html.Div(id="lantern-cursor"),
    html.Div(id="progress"),
    html.Div(id="toast", role="status"),

    # ── NAV ────────────────────────────────────────────────────────
    html.Nav([
        html.A([
            html.Span("A", className="hanko"),
            html.Span([html.Span("abhineet", className="accent"), html.Span(".sharma", className="dim")]),
        ], href="#hero", className="nav-logo"),
        html.Div([html.A(label, href=f"#{sid}", **{"data-nav": sid}) for sid, label in NAV], className="nav-links"),
        html.Div([
            html.Button(html.I(className="fa-solid fa-cloud-rain"), id="rain-toggle", className="icon-btn",
                        title="Rain: drizzle / storm / off  (R)", **{"aria-label": "Toggle rain"}),
            html.Button(html.I(className="fa-solid fa-volume-xmark"), id="sound-toggle", className="icon-btn",
                        title="Rain sound  (S)", **{"aria-label": "Toggle rain sound"}),
            html.Button([html.Span(), html.Span(), html.Span()], id="burger", className="burger",
                        **{"aria-label": "Open menu", "aria-expanded": "false"}),
        ], className="nav-controls"),
    ], id="navbar"),

    html.Div([
        html.Div([html.A([html.Span(f"0{i+1}", className="num"), label], href=f"#{sid}")
                  for i, (sid, label) in enumerate(NAV)], className="mobile-links"),
        html.Div("雨にも負けず", className="mobile-menu-kanji"),
    ], id="mobile-menu"),

    # ── HERO ───────────────────────────────────────────────────────
    html.Section([
        html.Div([
            html.Picture([
                html.Source(srcSet="/assets/img/ronin-mobile.webp", media="(max-width: 760px)", type="image/webp"),
                html.Source(srcSet="/assets/img/ronin.webp", type="image/webp"),
                html.Img(src="/assets/img/ronin.jpg", alt="A ronin sketching by lantern light on rain-soaked shrine steps",
                         id="hero-img"),
            ]),
            html.Div(id="lantern-glow"),
        ], className="hero-bg", id="hero-bg"),
        html.Div(className="hero-shade"),
        html.Div(className="hero-fog"),

        html.Div("浪人", className="hero-vertical", **{"aria-hidden": "true"}),

        html.Div([
            html.Div([html.Span(className="dot"), "Open to freelance & consulting"], className="status-pill reveal"),
            html.Div("Data Scientist & AI Engineer · Noida", className="hero-eyebrow reveal"),
            html.H1([html.Span("Abhineet", className="first"), html.Span("Sharma", className="last")],
                    className="hero-name reveal"),
            html.Div([html.Span(id="typewriter-text"), html.Span(className="typewriter-cursor")],
                     className="hero-role reveal"),
            html.P([
                f"{YEARS} years building GenAI and ML systems end to end: RAG pipelines, multi-agent "
                "orchestration and production deploys. ",
                html.Span("I write agents by lantern light and ship them in the rain.", className="hero-quip"),
            ], className="hero-desc reveal"),
            html.Div([
                html.A([html.I(className="fa-solid fa-torii-gate"), " See the work"], href="#projects", className="btn-primary"),
                html.A([brand_icon("github", "bi bi-sm"), " GitHub"], href="https://github.com/divergent99",
                       target="_blank", rel="noopener", className="btn-ghost"),
                html.A([html.I(className="fa-regular fa-envelope"), " Email"], href="mailto:abhineetsharma77@gmail.com",
                       className="btn-ghost"),
            ], className="hero-ctas reveal"),
            html.Div([
                stat(4, "+", "Years in production AI"),
                stat(10, "+", "Hackathons shipped"),
                stat(60, "%", "Analyst prep time cut"),
                stat(65, "%", "Query time reduced"),
            ], className="hero-stats reveal"),
        ], className="container hero-content"),

        html.A([html.Span("scroll"), html.Span(className="scroll-line")], href="#way", className="scroll-cue"),
    ], id="hero"),

    # ── THE WAY ────────────────────────────────────────────────────
    html.Section([
        html.Div([
            section_head("01", "道", "The Way", "How I build",
                         "Three rules, borrowed loosely from bushido and strictly from production incidents."),
            html.Div([
                html.Div([
                    html.Div(k, className="code-kanji"),
                    html.Div(r, className="code-romaji"),
                    html.H3(t, className="code-title"),
                    html.P(d, className="code-desc"),
                ], className="code-card reveal")
                for k, r, t, d in CODE
            ], className="code-grid"),
        ], className="container"),
    ], id="way", className="section"),

    # ── CASE STUDIES ───────────────────────────────────────────────
    html.Section([
        html.Div([
            section_head("02", "匠", "The Craft", "Production case studies",
                         "Hackathons are sparring. This is the real fight: systems running for real users and deal teams."),
            html.Div([case_card(c, i) for i, c in enumerate(CASES)], className="cases"),
        ], className="container"),
    ], id="cases", className="section"),

    # ── PROJECTS ───────────────────────────────────────────────────
    html.Section([
        html.Div([
            section_head("03", "作", "The Work", "Selected projects",
                         "Deployed products and hackathon systems, built under real deadlines."),
            html.Div([
                html.Div([
                    html.Button(label, className="filter-btn" + (" active" if key == "all" else ""),
                                **{"data-filter": key})
                    for key, label in FILTERS
                ], className="filters", role="tablist"),
                html.Label([
                    html.Span(className="switch"),
                    html.Span("Live only"),
                ], className="live-toggle", id="live-toggle", **{"data-on": "0"}),
            ], className="filter-bar reveal"),
            html.Div([project_card(p, i) for i, p in enumerate(PROJECTS)], className="projects-grid", id="projects-grid"),
            html.Div(id="projects-empty", className="projects-empty", children="Nothing here yet. The rain washed it away."),
            html.Div(html.Button([html.Span("Unsheathe all", className="more-label"), html.I(className="fa-solid fa-chevron-down")],
                                 id="show-more", className="btn-ghost"), className="show-more-wrap"),
        ], className="container"),
    ], id="projects", className="section"),

    # ── SKILLS ─────────────────────────────────────────────────────
    html.Section([
        html.Div([
            section_head("04", "武器", "The Arsenal", "Tech stack",
                         "From LLM orchestration to production deployment. Hover to light them up."),
            html.Div([skill_section(c) for c in SKILL_CATS], className="skill-categories"),
            html.Div([
                html.Span("Also fluent in", className="also-label"),
                html.Div([html.Span(s, className="also-chip") for s in ALSO_FLUENT], className="also-row"),
            ], className="also reveal"),
        ], className="container"),
    ], id="skills", className="section"),

    # ── EXPERIENCE ─────────────────────────────────────────────────
    html.Section([
        html.Div([
            section_head("05", "旅", "The Path", "Experience",
                         f"{YEARS} years delivering AI in production, from BFSI to PE deal rooms to education."),
            html.Div([timeline_item(e) for e in EXPERIENCE], className="timeline"),
            html.Div([
                html.Div([
                    html.Div([html.I(className="fa-solid fa-graduation-cap"), html.Span("Degree", className="edu-kind")], className="edu-top"),
                    html.H3("B.Tech, Information Technology", className="edu-title"),
                    html.Div("Dr. A.P.J. Abdul Kalam Technical University", className="edu-org"),
                    html.Div([
                        html.Div([html.Span("CGPA", className="edu-k"), html.Span(["8.81", html.Span(" / 10", className="dim")], className="edu-score")],
                                 className="cgpa-head"),
                        html.Div(html.Div(className="cgpa-fill", style={"--w": "88.1%"}), className="cgpa-track"),
                    ], className="cgpa"),
                    html.Div([html.I(className="fa-solid fa-medal"), "First Division with Distinction"], className="edu-honour"),
                    html.Div([html.Span("Distinction", className="edu-pill"), html.Span("2018 to 2022", className="edu-date")], className="edu-meta"),
                ], className="edu-card reveal"),
                html.Div([
                    html.Div([html.I(className="fa-solid fa-award"), html.Span("Fellowship", className="edu-kind"),
                              html.A(["Credentials ", html.I(className="fa-solid fa-arrow-up-right-from-square")],
                                     href="https://www.linkedin.com/in/abhineet-sharma-/details/certifications/",
                                     target="_blank", rel="noopener", className="edu-link")], className="edu-top"),
                    html.H3("Master ML & AI", className="edu-title"),
                    html.Div("Univ.AI · DSLP Fellowship", className="edu-org"),
                    html.Div([html.Span(m, className="also-chip") for m in UNIVAI_MODULES], className="edu-modules"),
                    html.Div([html.Span("6 modules", className="edu-pill"), html.Span("2021 to 2022", className="edu-date")], className="edu-meta"),
                ], className="edu-card reveal"),
            ], className="edu-grid"),
        ], className="container"),
    ], id="experience", className="section"),

    # ── LINKEDIN POSTS ─────────────────────────────────────────────
    html.Section([
        html.Div([
            section_head("06", "書", "The Notes", "Latest writing",
                         "Short posts on LinkedIn, long-form on Medium. What I'm building and what I learned."),
            html.Div([
                html.Div([
                    html.Button(html.I(className="fa-solid fa-arrow-left"), className="icon-btn post-nav", id="posts-prev",
                                **{"aria-label": "Previous post"}),
                    html.Button(html.I(className="fa-solid fa-arrow-right"), className="icon-btn post-nav", id="posts-next",
                                **{"aria-label": "Next post"}),
                ], className="posts-controls"),
                html.A([brand_icon("linkedin", "bi bi-sm"), " Follow on LinkedIn"],
                       href="https://www.linkedin.com/in/abhineet-sharma-/recent-activity/all/",
                       target="_blank", rel="noopener", className="btn-ghost posts-follow"),
            ], className="posts-bar reveal"),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div(className="post-skel-line w40"), html.Div(className="post-skel-line w90"),
                        html.Div(className="post-skel-line w75"), html.Div(className="post-skel-block"),
                    ], className="post-frame", **{"data-src": f"https://www.linkedin.com/embed/feed/update/urn:li:share:{pid}",
                                                  "data-h": str(h)}),
                    html.Div([
                        html.Button([html.Span("Read more", className="rm-label"), html.I(className="fa-solid fa-chevron-down")],
                                    className="post-more"),
                        html.A(["Open on LinkedIn ", html.I(className="fa-solid fa-arrow-up-right-from-square")],
                               href=f"https://www.linkedin.com/feed/update/urn:li:share:{pid}/",
                               target="_blank", rel="noopener", className="post-open"),
                    ], className="post-foot"),
                ], className="post-card reveal")
                for pid, h in POSTS
            ], className="posts-track", id="posts-track"),
            html.Div([
                html.Div([brand_icon("medium", "bi"), html.Span("Long-form on Medium")], className="articles-label"),
                html.A(["All articles ", html.I(className="fa-solid fa-arrow-right")], href="https://abhineetsharma77.medium.com/",
                       target="_blank", rel="noopener", className="articles-all"),
            ], className="articles-head reveal"),
            html.Div(id="articles", className="articles-grid reveal"),
        ], className="container"),
    ], id="posts", className="section"),

    # ── CONTACT ────────────────────────────────────────────────────
    html.Section([
        html.Div([
            section_head("07", "灯", "Light the lantern", "Let's build something",
                         "Open to freelance projects, consulting and collaborations."),
            html.Div([
                html.Div([
                    contact_link("github", "GitHub", "divergent99", "https://github.com/divergent99"),
                    contact_link("linkedin", "LinkedIn", "abhineet-sharma-", "https://linkedin.com/in/abhineet-sharma-/"),
                    contact_link("gmail", "Email", "abhineetsharma77@gmail.com", "mailto:abhineetsharma77@gmail.com"),
                    contact_link("medium", "Medium", "abhineetsharma77", "https://abhineetsharma77.medium.com/"),
                    contact_link("hackerrank", "HackerRank", "5★ Python, SQL, C++ · Shadow_Walker007",
                                 "https://www.hackerrank.com/profile/Shadow_Walker007"),
                ], className="contact-links"),
                html.Div([
                    html.Div(className="cta-lantern", children=[html.Div(className="cta-lantern-body"), html.Div(className="cta-lantern-light")]),
                    html.H3("The lantern's on.", className="cta-title"),
                    html.P("GenAI pipelines, RAG systems, multi-agent architectures and enterprise AI. "
                           "Tell me the problem, I'll bring the umbrella.", className="cta-sub"),
                    html.Div([
                        html.A("Get in touch", href="mailto:abhineetsharma77@gmail.com", className="btn-primary"),
                        html.Button([html.I(className="fa-regular fa-copy"), " Copy email"], className="btn-ghost",
                                    id="copy-email", **{"data-copy": "abhineetsharma77@gmail.com"}),
                    ], className="cta-actions"),
                ], className="contact-cta-card reveal"),
            ], className="contact-grid"),
        ], className="container"),
    ], id="contact", className="section"),

    html.Footer([
        html.Div([
            html.Span("A", className="hanko small"),
            html.Span("Abhineet Sharma © 2026"),
        ], className="foot-left"),
        html.Div([
            "Plotly Dash components, server-rendered, + vanilla JS · ",
            html.Kbd("R"), " rain ", html.Kbd("S"), " sound",
        ], className="foot-right"),
    ], className="site-footer"),
])


# ══════════════════════════════════════════════════════════════════
# SERVER-SIDE RENDER
# Dash components are rendered to static HTML once at startup, so crawlers,
# link previews and slow phones get the full page without the React bundle.
# ══════════════════════════════════════════════════════════════════
import hashlib
import json
import os
import re
from html import escape

from flask import Response, request

VOID = {"img", "source", "br", "hr", "input", "meta", "link"}
SKIP_PROPS = {"children", "n_clicks", "n_clicks_timestamp", "disable_n_clicks", "loading_state"}
ATTR = {"className": "class", "srcSet": "srcset", "htmlFor": "for"}


def _css_name(k):
    if k.startswith("--"):
        return k
    k = re.sub(r"^Webkit", "-webkit-", k)
    return re.sub(r"(?<!^)(?<!-)([A-Z])", r"-\1", k).lower()


def render(node):
    if node is None:
        return ""
    if isinstance(node, (str, int, float)):
        return escape(str(node))
    if isinstance(node, (list, tuple)):
        return "".join(render(n) for n in node)
    js = node.to_plotly_json()
    tag, props = js["type"].lower(), js["props"]
    attrs = []
    for k, v in props.items():
        if k in SKIP_PROPS or v is None:
            continue
        if k == "style":
            v = ";".join(f"{_css_name(sk)}:{sv}" for sk, sv in v.items())
        attrs.append(f'{ATTR.get(k, k)}="{escape(str(v), quote=True)}"')
    if tag == "button":
        attrs.append('type="button"')
    open_tag = f"<{tag}{' ' if attrs else ''}{' '.join(attrs)}>"
    return open_tag if tag in VOID else f"{open_tag}{render(props.get('children'))}</{tag}>"


ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")


def _v(name):
    with open(os.path.join(ASSETS, name), "rb") as f:
        return hashlib.md5(f.read()).hexdigest()[:8]


DESCRIPTION = ("Abhineet Sharma, Data Scientist and AI Engineer with 4+ years building GenAI systems: "
               "LangGraph agents, RAG pipelines and production ML.")
PERSON = {
    "@context": "https://schema.org", "@type": "Person", "name": "Abhineet Sharma",
    "jobTitle": "Data Scientist & AI Engineer", "worksFor": {"@type": "Organization", "name": "GEDU Services"},
    "address": {"@type": "PostalAddress", "addressLocality": "Noida", "addressCountry": "IN"},
    "email": "mailto:abhineetsharma77@gmail.com",
    "sameAs": ["https://github.com/divergent99", "https://linkedin.com/in/abhineet-sharma-/",
               "https://abhineetsharma77.medium.com/"],
    "knowsAbout": ["Generative AI", "LangGraph", "RAG", "Multi-agent systems", "Machine Learning", "FastAPI"],
}
from graphs import graph_html, GRAPHS
import medium
medium.warm()

BODY = render(app.layout)
for _key in GRAPHS:
    BODY = BODY.replace(f'<div class="case-graph" data-graph="{_key}"></div>',
                        f'<div class="case-graph" data-graph="{_key}">{graph_html(_key)}</div>')
BODY, _n = re.subn(r'(<div[^>]*id="articles"[^>]*>)</div>', r'\1{articles}</div>', BODY)
assert _n == 1, "articles placeholder not found"
FA = "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"
TEMPLATE = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<script>document.documentElement.classList.add("js")</script>
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Abhineet Sharma | Data Scientist &amp; AI Engineer</title>
<meta name="description" content="{escape(DESCRIPTION)}">
<meta name="theme-color" content="#070b14">
<link rel="canonical" href="{{origin}}/">
<meta property="og:type" content="website">
<meta property="og:url" content="{{origin}}/">
<meta property="og:title" content="Abhineet Sharma | Data Scientist &amp; AI Engineer">
<meta property="og:description" content="4+ years shipping GenAI, RAG and multi-agent systems. Built in the rain.">
<meta property="og:image" content="{{origin}}/assets/img/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="675">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{{origin}}/assets/img/og.jpg">
<link rel="icon" href="/assets/favicon.ico">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="image" type="image/webp" href="/assets/img/ronin.webp" media="(min-width: 761px)">
<link rel="preload" as="image" type="image/webp" href="/assets/img/ronin-mobile.webp" media="(max-width: 760px)">
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="{FA}" media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="{FA}"></noscript>
<link rel="stylesheet" href="/assets/style.css?v={_v('style.css')}">
<script type="application/ld+json">{json.dumps(PERSON)}</script>
</head>
<body>
{BODY}
<script src="/assets/main.js?v={_v('main.js')}" defer></script>
</body>
</html>"""


def _origin():
    proto = request.headers.get("X-Forwarded-Proto", request.scheme).split(",")[0].strip()
    if request.host.endswith(".railway.app") or request.host.endswith(".dev"):
        proto = "https"
    return f"{proto}://{request.host}"


@server.before_request
def serve_static_page():
    if request.path in ("/", "/index.html"):
        page = TEMPLATE.replace("{origin}", _origin()).replace("{articles}", medium.render(medium.articles()))
        resp = Response(page, mimetype="text/html")
        resp.headers["Cache-Control"] = "public, max-age=300"
        return resp
    if request.path == "/status/medium":
        return Response(json.dumps(medium.status(), indent=2), mimetype="application/json",
                        headers={"Cache-Control": "no-store"})
    if request.path == "/robots.txt":
        return Response(f"User-agent: *\nAllow: /\nSitemap: {_origin()}/sitemap.xml\n", mimetype="text/plain")
    if request.path == "/sitemap.xml":
        return Response(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                        f"<url><loc>{_origin()}/</loc></url></urlset>", mimetype="application/xml")


@server.after_request
def cache_assets(resp):
    if request.path.startswith("/assets/"):
        versioned = bool(request.args.get("v"))
        resp.headers["Cache-Control"] = "public, max-age=31536000, immutable" if versioned else "public, max-age=604800"
    return resp


if __name__ == "__main__":
    server.run(debug=False, port=8060)
