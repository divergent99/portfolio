"""Architecture graphs for the case studies.

Each graph is a small DAG laid out on a (col, row) grid. It renders to two
SVGs: horizontal for wide screens and vertical (cols become rows) for phones.
Data packets travel along every edge with SVG <animateMotion>, so the motion
needs no JavaScript; main.js only adds hover highlighting.
"""
from html import escape

KIND_COLOR = {
    "source": "#9bb4d6",   # rain
    "process": "#c9c4b8",  # paper
    "store": "#9fd26f",    # moss
    "llm": "#f6a54a",      # lantern
    "output": "#d4402f",   # crimson
}
KIND_LABEL = {"source": "Source", "process": "Process", "store": "Store", "llm": "LLM / agent", "output": "Output"}

GRAPHS = {
    "gbs": {
        "nodes": {
            "web":     (0, 0, "Website", "450+ pages", "source"),
            "pdf":     (0, 2, "PDFs & tables", "prospectus, fees", "source"),
            "crawl":   (1, 0, "Recursive crawler", "link-aware", "process"),
            "extract": (1, 2, "PDF / table extract", "layout-preserving", "process"),
            "embed":   (2, 1, "Embeddings", "domain-tuned", "process"),
            "chroma":  (3, 1, "ChromaDB", "vector store", "store"),
            "user":    (4, 0, "Student question", "chat widget", "source"),
            "agent":   (4, 1, "LangGraph agent", "retrieve + route", "llm"),
            "claude":  (5, 1, "Claude", "cited answer", "llm"),
            "check":   (6, 1, "Self-check", "grounded?", "process"),
            "sse":     (6, 0, "SSE stream", "answer + sources", "output"),
        },
        "edges": [
            ("web", "crawl"), ("pdf", "extract"), ("crawl", "embed"), ("extract", "embed"),
            ("embed", "chroma"), ("chroma", "agent"), ("user", "agent"), ("agent", "claude"),
            ("claude", "check"), ("check", "sse", "pass"), ("check", "agent", "retry", "below"),
        ],
    },
    "cdd": {
        "nodes": {
            "room":     (0, 1, "Data room", "PDFs, decks, xlsx", "source"),
            "docling":  (1, 1, "Docling", "parse + structure", "process"),
            "gpt":      (2, 1, "Azure OpenAI", "fact extraction", "llm"),
            "facts":    (3, 1, "Fact sheet", "structured JSON", "store"),
            "template": (3, 0, "Deck template", "firm format", "source"),
            "pptx":     (4, 1, "python-pptx", "slide renderer", "process"),
            "deck":     (5, 1, "CDD deck", "ready for review", "output"),
        },
        "edges": [
            ("room", "docling"), ("docling", "gpt"), ("gpt", "facts"), ("facts", "pptx"),
            ("template", "pptx"), ("pptx", "deck"),
        ],
    },
    "rapid": {
        "nodes": {
            "q":      (0, 1, "Question", "plain English", "source"),
            "follow": (1, 1, "Follow-up detector", "keeps context", "process"),
            "cache":  (2, 1, "Semantic cache", "similar asked?", "store"),
            "dax":    (3, 2, "Power BI / DAX", "metric definitions", "source"),
            "sql":    (3, 1, "LangGraph SQL", "Azure OpenAI", "llm"),
            "duck":   (4, 1, "DuckDB", "portfolio data", "store"),
            "ans":    (5, 1, "SSE answer", "matches dashboards", "output"),
        },
        "edges": [
            ("q", "follow"), ("follow", "cache"), ("cache", "sql", "miss"), ("dax", "sql"),
            ("sql", "duck"), ("duck", "ans"), ("cache", "ans", "hit", "above"),
        ],
    },
}

W, H = 136, 50          # node size
DX, DY = 168, 82        # grid spacing, horizontal layout
VDX, VDY = 150, 92      # grid spacing, vertical layout
PAD = 18


def _layout(spec, vertical):
    pos = {}
    for k, (c, r, *_rest) in spec["nodes"].items():
        if vertical:
            pos[k] = (PAD + r * VDX, PAD + c * VDY)
        else:
            pos[k] = (PAD + c * DX, PAD + r * DY)
    xs = [p[0] for p in pos.values()]
    ys = [p[1] for p in pos.values()]
    return pos, max(xs) + W + PAD, max(ys) + H + PAD


def _edge_path(a, b, vertical, route):
    (ax, ay), (bx, by) = a, b
    if vertical:
        x1, y1 = ax + W / 2, ay + H
        x2, y2 = bx + W / 2, by
        if abs(by - ay) < 1 and not route:   # same rank: straight side hop
            sx, tx = (ax, bx + W) if bx < ax else (ax + W, bx)
            return f"M{sx},{ay + H / 2} L{tx},{by + H / 2}", ((sx + tx) / 2, ay + H / 2 - 9)
        if route in ("below", "above") or by <= ay:
            # back-edge / bypass: swing out to the side
            side = -1 if route == "above" else 1
            x1 = ax + (W if side > 0 else 0)
            y1 = ay + H / 2
            x2 = bx + (W if side > 0 else 0)
            y2 = by + H / 2
            off = 56 * side
            return f"M{x1},{y1} C{x1 + off},{y1} {x2 + off},{y2} {x2},{y2}", ((x1 + x2) / 2 + off * 0.75, (y1 + y2) / 2)
        if abs(ax - bx) < 1 and by > ay:
            return f"M{x1},{y1} L{x2},{y2}", ((x1 + x2) / 2 + 8, (y1 + y2) / 2)
        my = (y1 + y2) / 2
        return f"M{x1},{y1} C{x1},{my} {x2},{my} {x2},{y2}", ((x1 + x2) / 2, my)

    if route in ("below", "above"):
        side = 1 if route == "below" else -1
        x1, y1 = ax + W / 2, ay + (H if side > 0 else 0)
        x2, y2 = bx + W / 2, by + (H if side > 0 else 0)
        off = 62 * side
        return f"M{x1},{y1} C{x1},{y1 + off} {x2},{y2 + off} {x2},{y2}", ((x1 + x2) / 2, (y1 + y2) / 2 + off * 0.75)
    if abs(ax - bx) < 1:   # same column: straight vertical hop
        if by < ay:
            x1, y1, x2, y2 = ax + W / 2, ay, bx + W / 2, by + H
        else:
            x1, y1, x2, y2 = ax + W / 2, ay + H, bx + W / 2, by
        return f"M{x1},{y1} L{x2},{y2}", (x1 + 10, (y1 + y2) / 2)
    x1, y1 = ax + W, ay + H / 2
    x2, y2 = bx, by + H / 2
    mx = (x1 + x2) / 2
    return f"M{x1},{y1} C{mx},{y1} {mx},{y2} {x2},{y2}", (mx, (y1 + y2) / 2 - 11)


def _svg(key, spec, vertical):
    pos, vw, vh = _layout(spec, vertical)
    o = "v" if vertical else "h"
    out = [f'<svg class="arch arch-{o}" viewBox="0 0 {vw:.0f} {vh:.0f}" role="img" '
           f'aria-label="{escape(key)} architecture diagram" xmlns="http://www.w3.org/2000/svg">',
           f'<defs><marker id="ah-{key}-{o}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" '
           f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="rgba(233,228,216,.45)"/></marker></defs>']
    labels = []
    for i, e in enumerate(spec["edges"]):
        a, b = e[0], e[1]
        label = e[2] if len(e) > 2 else None
        route = e[3] if len(e) > 3 else None
        d, (lx, ly) = _edge_path(pos[a], pos[b], vertical, route)
        pid = f"p-{key}-{o}-{i}"
        color = KIND_COLOR[spec["nodes"][b][4]]
        dashed = " dashed" if route else ""
        out.append(f'<g class="edge{dashed}" data-from="{a}" data-to="{b}">'
                   f'<path id="{pid}" d="{d}" pathLength="1" marker-end="url(#ah-{key}-{o})"/>'
                   f'<circle r="3.2" fill="{color}" class="packet">'
                   f'<animateMotion dur="{2.2 + (i % 3) * 0.4:.1f}s" begin="{i * 0.35:.2f}s" repeatCount="indefinite">'
                   f'<mpath href="#{pid}"/></animateMotion></circle></g>')
        if label:
            labels.append(f'<text class="edge-label" x="{lx:.0f}" y="{ly:.0f}" text-anchor="middle">{escape(label)}</text>')
    # Wide vertical graphs (3 lanes) get bigger titles and no sublabels so they stay legible on phones
    compact = vertical and max(r for _c, r, *_x in spec["nodes"].values()) >= 2
    for k, (_c, _r, title, sub, kind) in spec["nodes"].items():
        x, y = pos[k]
        col = KIND_COLOR[kind]
        if compact:
            out.append(f'<g class="node kind-{kind}" data-node="{k}" transform="translate({x},{y})" tabindex="0">'
                       f'<rect width="{W}" height="{H}" rx="9" style="stroke:{col}"/>'
                       f'<rect class="node-tab" width="4" height="{H - 16}" x="0" y="8" rx="2" style="fill:{col}"/>'
                       f'<text class="node-title big" x="{W / 2 + 2:.0f}" y="{H / 2 + 5:.0f}" text-anchor="middle">{escape(title)}</text>'
                       f'<title>{escape(sub)}</title></g>')
            continue
        out.append(f'<g class="node kind-{kind}" data-node="{k}" transform="translate({x},{y})" tabindex="0">'
                   f'<rect width="{W}" height="{H}" rx="9" style="stroke:{col}"/>'
                   f'<rect class="node-tab" width="4" height="{H - 16}" x="0" y="8" rx="2" style="fill:{col}"/>'
                   f'<text class="node-title" x="14" y="21">{escape(title)}</text>'
                   f'<text class="node-sub" x="14" y="37">{escape(sub)}</text></g>')
    out.extend(labels)
    out.append("</svg>")
    return "".join(out)


def legend(key):
    kinds = []
    for _c, _r, _t, _s, kind in GRAPHS[key]["nodes"].values():
        if kind not in kinds:
            kinds.append(kind)
    return '<div class="arch-legend">' + "".join(
        f'<span><i style="background:{KIND_COLOR[k]}"></i>{KIND_LABEL[k]}</span>' for k in KIND_COLOR if k in kinds
    ) + '<span class="arch-hint">hover a node to trace it</span></div>'


def graph_html(key):
    spec = GRAPHS[key]
    return _svg(key, spec, False) + _svg(key, spec, True) + legend(key)
