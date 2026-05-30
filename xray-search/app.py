import streamlit as st
import urllib.parse
import io
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT

# ─── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="X-Ray Search Pro",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
}

/* Hide default streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.stApp {
    background: #0a0a0f;
    color: #e8e8f0;
}

/* Hero header */
.hero-title {
    font-size: 3.2rem;
    font-weight: 700;
    background: linear-gradient(135deg, #4af7c4 0%, #7b61ff 50%, #ff6b9d 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -1px;
    margin-bottom: 0.3rem;
}
.hero-subtitle {
    font-size: 1.1rem;
    color: #8888aa;
    margin-bottom: 2rem;
    font-weight: 300;
}

/* Network pills */
.network-pills {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin: 12px 0;
}
.pill {
    display: inline-block;
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 0.82rem;
    font-weight: 500;
    border: 1px solid;
    cursor: pointer;
    transition: all 0.2s;
}

/* Result box */
.result-box {
    background: #13131f;
    border: 1px solid #2a2a3d;
    border-left: 4px solid #4af7c4;
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.9rem;
    word-break: break-all;
    line-height: 1.7;
    color: #c8f7e8;
}

.variant-box {
    background: #13131f;
    border: 1px solid #2a2a3d;
    border-radius: 10px;
    padding: 1.2rem;
    margin: 0.6rem 0;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    word-break: break-all;
    color: #d4d4f0;
}

.variant-label {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.78rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 6px;
}

/* Section header */
.section-header {
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: #7b61ff;
    margin: 1.5rem 0 0.8rem;
}

/* Stats row */
.stats-row {
    display: flex;
    gap: 16px;
    margin: 1rem 0;
    flex-wrap: wrap;
}
.stat-chip {
    background: #1e1e30;
    border: 1px solid #2a2a3d;
    border-radius: 8px;
    padding: 6px 14px;
    font-size: 0.8rem;
    color: #9999bb;
}
.stat-chip span {
    color: #4af7c4;
    font-weight: 600;
}

/* Operator badge */
.op-badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 4px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    font-weight: 600;
    margin: 2px;
}
.op-quote { background: #1a3d2a; color: #4af7c4; border: 1px solid #2d6644; }
.op-or    { background: #2a1a3d; color: #a88fff; border: 1px solid #5d3d8a; }
.op-plus  { background: #1a2a3d; color: #6bb5ff; border: 1px solid #2d4d6a; }
.op-minus { background: #3d1a1a; color: #ff8888; border: 1px solid #6a2d2d; }
.op-site  { background: #3d2a1a; color: #ffbb66; border: 1px solid #6a4d2d; }

/* Google button */
.google-btn {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: linear-gradient(135deg, #4af7c4, #7b61ff);
    color: #000;
    padding: 10px 24px;
    border-radius: 8px;
    font-weight: 700;
    font-size: 0.95rem;
    text-decoration: none;
    transition: opacity 0.2s;
}
.google-btn:hover { opacity: 0.85; }

/* Divider */
.fancy-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #2a2a3d, transparent);
    margin: 2rem 0;
}

/* Input styling override */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
    background: #13131f !important;
    border: 1px solid #2a2a3d !important;
    color: #e8e8f0 !important;
    border-radius: 8px !important;
}

.stMultiSelect > div > div {
    background: #13131f !important;
    border: 1px solid #2a2a3d !important;
}

/* Label */
.stTextInput label, .stTextArea label, .stSelectbox label, .stMultiSelect label, .stRadio label {
    color: #9999bb !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    text-transform: uppercase !important;
    letter-spacing: 1.2px !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: #13131f;
    border-radius: 10px;
    padding: 4px;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #8888aa;
    border-radius: 8px;
    font-weight: 500;
}
.stTabs [aria-selected="true"] {
    background: #1e1e30 !important;
    color: #4af7c4 !important;
}

/* Button */
.stButton > button {
    background: linear-gradient(135deg, #4af7c4 0%, #7b61ff 100%) !important;
    color: #000 !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.6rem 2rem !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.5px !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}

/* Download button */
.stDownloadButton > button {
    background: #1e1e30 !important;
    color: #4af7c4 !important;
    border: 1px solid #4af7c4 !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}
</style>
""", unsafe_allow_html=True)


# ─── Network configs ────────────────────────────────────────────────────────────
NETWORKS = {
    "LinkedIn": {
        "icon": "💼",
        "color": "#0077b5",
        "site": "linkedin.com/in",
        "profile_fields": ["in", "pub"],
        "extra": 'site:linkedin.com/in OR site:linkedin.com/pub',
    },
    "GitHub": {
        "icon": "🐙",
        "color": "#6e40c9",
        "site": "github.com",
        "extra": 'site:github.com -site:github.com/orgs',
    },
    "Stack Overflow": {
        "icon": "📚",
        "color": "#f48024",
        "site": "stackoverflow.com/users",
        "extra": 'site:stackoverflow.com/users',
    },
    "Twitter/X": {
        "icon": "🐦",
        "color": "#1da1f2",
        "site": "x.com",
        "extra": 'site:x.com OR site:twitter.com -site:twitter.com/hashtag',
    },
    "Wellfound": {
        "icon": "🚀",
        "color": "#1a1a1a",
        "site": "wellfound.com",
        "extra": 'site:wellfound.com/u',
    },
    "Dribbble": {
        "icon": "🎨",
        "color": "#ea4c89",
        "site": "dribbble.com",
        "extra": 'site:dribbble.com',
    },
    "Behance": {
        "icon": "✏️",
        "color": "#1769ff",
        "site": "behance.net",
        "extra": 'site:behance.net',
    },
    "Google (général)": {
        "icon": "🌐",
        "color": "#4285f4",
        "site": "",
        "extra": '',
    },
}

EDUCATION_MAP = {
    "Tous les candidats": "",
    "Licence / Bachelor": '"licence" OR "bachelor" OR "bac+3"',
    "Master": '"master" OR "mastère" OR "bac+5" OR "msc" OR "mba"',
    "Doctorat": '"doctorat" OR "phd" OR "docteur"',
}

INTENT_MAP = {
    "Recherche générale": "",
    "Achat / Service": '+acheter OR +prix OR +tarif OR +service',
    "Application / Logiciel": '+application OR +appli OR +logiciel OR +télécharger',
    "Professionnel / Recrutement": '+professionnel OR +expert OR +consultant OR +freelance',
    "Actualité / Veille": '+2024 OR +2025 OR +actualité OR +news',
}

DEFAULT_EXCLUSIONS = ["-gratuit", "-avis", "-forum", "-PDF", "-emploi", "-occasion", "-wiki", "-discount"]


# ─── Core logic ────────────────────────────────────────────────────────────────
def build_query(params: dict) -> dict:
    """Build the optimised Google search query from params."""
    parts_main = []
    parts_quoted = []

    # Param 1: Keywords — comma = separate expressions, no comma = single expression
    # "analyste lcbft" → "analyste lcbft"
    # "analyste lcbft, conformité" → "analyste lcbft" OR "conformité"
    kw_raw = params.get("keywords", "")
    if kw_raw:
        expressions = [e.strip() for e in kw_raw.split(",") if e.strip()]
        quoted = [f'"{e}"' for e in expressions]
        parts_quoted = quoted
        parts_main.append(" OR ".join(quoted))

    # Param 2: Job title / exact phrase
    job_title = params.get("job_title", "").strip()
    if job_title:
        parts_main.insert(0, f'"{job_title}"')

    # Param 3: Location / additional include
    location = params.get("location", "").strip()
    if location:
        parts_main.append(f'"{location}"')

    # Param 4: Education
    edu = EDUCATION_MAP.get(params.get("education", "Tous les candidats"), "")
    if edu:
        parts_main.append(f"({edu})")

    # Param 5: Current employer
    employer = params.get("employer", "").strip()
    if employer:
        parts_main.append(f'"{employer}"')

    # Intent modifiers
    intent = INTENT_MAP.get(params.get("intent", "Recherche générale"), "")
    if intent:
        parts_main.append(intent)

    # Network site restriction
    network = params.get("network", "Google (général)")
    net_cfg = NETWORKS.get(network, NETWORKS["Google (général)"])
    site_op = net_cfg["extra"]
    if site_op:
        parts_main.append(f"({site_op})")

    # Exclusions
    custom_excl = params.get("exclusions", "")
    excl_list = list(DEFAULT_EXCLUSIONS)
    if custom_excl:
        for e in custom_excl.replace(",", " ").split():
            token = e.strip().lstrip("-")
            if token:
                excl_list.append(f"-{token}")

    excl_str = " ".join(excl_list)
    base = " ".join(parts_main)
    base_no_excl = base
    full_query = f"{base} {excl_str}".strip()

    return {
        "query": full_query,
        "base": base_no_excl,
        "exclusions": excl_str,
        "quoted_keywords": parts_quoted,
        "network": network,
        "net_cfg": net_cfg,
        "google_url": f"https://www.google.com/search?q={urllib.parse.quote(full_query)}",
    }


def generate_pdf(result: dict, params: dict) -> bytes:
    """Generate a styled PDF report for the search query."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm,
    )

    styles = getSampleStyleSheet()
    dark = colors.HexColor("#0a0a0f")
    accent = colors.HexColor("#4af7c4")
    purple = colors.HexColor("#7b61ff")
    light = colors.HexColor("#e8e8f0")
    muted = colors.HexColor("#8888aa")
    card_bg = colors.HexColor("#13131f")

    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Title"],
        fontSize=26,
        textColor=accent,
        fontName="Helvetica-Bold",
        spaceAfter=4,
        alignment=TA_CENTER,
    )
    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        fontSize=10,
        textColor=muted,
        alignment=TA_CENTER,
        spaceAfter=20,
    )
    section_style = ParagraphStyle(
        "Section",
        parent=styles["Normal"],
        fontSize=8,
        textColor=purple,
        fontName="Helvetica-Bold",
        spaceBefore=16,
        spaceAfter=6,
        textTransform="uppercase",
    )
    query_style = ParagraphStyle(
        "Query",
        parent=styles["Code"],
        fontSize=9,
        textColor=accent,
        backColor=card_bg,
        borderPadding=12,
        fontName="Courier-Bold",
        leading=14,
    )
    variant_label_style = ParagraphStyle(
        "VLabel",
        parent=styles["Normal"],
        fontSize=8,
        textColor=purple,
        fontName="Helvetica-Bold",
        spaceBefore=10,
        spaceAfter=2,
    )
    variant_style = ParagraphStyle(
        "Variant",
        parent=styles["Code"],
        fontSize=8,
        textColor=light,
        backColor=card_bg,
        fontName="Courier",
        leading=13,
        borderPadding=8,
    )
    label_style = ParagraphStyle(
        "Label",
        parent=styles["Normal"],
        fontSize=8,
        textColor=muted,
        fontName="Helvetica-Bold",
    )
    value_style = ParagraphStyle(
        "Value",
        parent=styles["Normal"],
        fontSize=9,
        textColor=light,
    )

    story = []

    # Header
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("🔍 X-Ray Search Pro", title_style))
    story.append(Paragraph(f"Rapport généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=purple, spaceAfter=16))

    # Params table
    story.append(Paragraph("PARAMÈTRES DE RECHERCHE", section_style))
    param_data = [
        ["Réseau", params.get("network", "—")],
        ["Mots-clés", params.get("keywords", "—") or "—"],
        ["Poste / Titre", params.get("job_title", "—") or "—"],
        ["Localisation", params.get("location", "—") or "—"],
        ["Niveau d'études", params.get("education", "—") or "—"],
        ["Employeur", params.get("employer", "—") or "—"],
        ["Intention", params.get("intent", "—")],
    ]
    tbl = Table(param_data, colWidths=[4*cm, 13*cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), card_bg),
        ("BACKGROUND", (1, 0), (1, -1), colors.HexColor("#0f0f1a")),
        ("TEXTCOLOR", (0, 0), (0, -1), muted),
        ("TEXTCOLOR", (1, 0), (1, -1), light),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [card_bg, colors.HexColor("#0f0f1a")]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#2a2a3d")),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("ROUNDEDCORNERS", [4, 4, 4, 4]),
    ]))
    story.append(tbl)

    # Main query
    story.append(Paragraph("REQUÊTE GOOGLE OPTIMISÉE", section_style))
    story.append(Paragraph(result["query"], query_style))
    story.append(Spacer(1, 0.4*cm))

    # URL
    story.append(Paragraph("URL DE RECHERCHE", section_style))
    story.append(Paragraph(result["google_url"], ParagraphStyle(
        "URL", parent=styles["Normal"], fontSize=7, textColor=colors.HexColor("#6bb5ff"),
        fontName="Courier", leading=11,
    )))

    # Variants
    story.append(Paragraph("VARIANTES PAR OBJECTIF", section_style))
    for label, query in result["variants"].items():
        story.append(Paragraph(label, variant_label_style))
        story.append(Paragraph(query, variant_style))

    # Operators guide
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#2a2a3d"), spaceBefore=20, spaceAfter=12))
    story.append(Paragraph("GUIDE DES OPÉRATEURS UTILISÉS", section_style))

    ops_data = [
        ['Opérateur', 'Usage', 'Exemple'],
        ['"mot"', 'Correspondance exacte', '"développeur python"'],
        ['OR', 'Alternative (majuscules)', '"java" OR "python"'],
        ['+mot', 'Mot obligatoire', '+expert +senior'],
        ['-mot', 'Exclure un mot', '-forum -gratuit'],
        ['site:', 'Restreindre au domaine', 'site:linkedin.com'],
    ]
    ops_tbl = Table(ops_data, colWidths=[3.5*cm, 7*cm, 6.5*cm])
    ops_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), purple),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [card_bg, colors.HexColor("#0f0f1a")]),
        ("TEXTCOLOR", (0, 1), (-1, -1), light),
        ("FONTNAME", (0, 1), (0, -1), "Courier-Bold"),
        ("TEXTCOLOR", (0, 1), (0, -1), accent),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#2a2a3d")),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(ops_tbl)

    # Footer
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph(
        "X-Ray Search Pro — Outil de recherche Google avancée",
        ParagraphStyle("Footer", parent=styles["Normal"], fontSize=7, textColor=muted, alignment=TA_CENTER)
    ))

    doc.build(story)
    return buffer.getvalue()


# ─── UI ────────────────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title">🔍 X-Ray Search Pro</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Transformez vos mots-clés en requêtes Google ultra-précises · Recherche X-Ray multi-plateformes</div>', unsafe_allow_html=True)

# Operator legend
st.markdown("""
<div style="margin-bottom:1.5rem">
  <span class="op-badge op-quote">"mot"</span> exacte &nbsp;
  <span class="op-badge op-or">OR</span> alternative &nbsp;
  <span class="op-badge op-plus">+mot</span> inclure &nbsp;
  <span class="op-badge op-minus">-mot</span> exclure &nbsp;
  <span class="op-badge op-site">site:</span> domaine
</div>
""", unsafe_allow_html=True)

# ── Tabs ──
tab1, tab2 = st.tabs(["🎯 Générateur de requête", "📖 Guide des opérateurs"])

with tab1:
    col_left, col_right = st.columns([1.1, 1], gap="large")

    with col_left:
        st.markdown('<div class="section-header">⚙️ Paramètres de recherche</div>', unsafe_allow_html=True)

        # Network selector
        network = st.selectbox(
            "Réseau / Plateforme",
            list(NETWORKS.keys()),
            index=0,
        )
        net_cfg = NETWORKS[network]
        st.markdown(f"""
        <div style="font-size:0.8rem;color:#8888aa;margin-top:-8px;margin-bottom:12px">
          {net_cfg['icon']} Recherche sur <code style="color:#4af7c4">{net_cfg['site'] or 'tous les sites'}</code>
        </div>
        """, unsafe_allow_html=True)

        # Param 1 — Keywords
        keywords = st.text_input(
            "① Mots-clés ou expressions (séparés par virgule)",
            placeholder="ex: analyste lcbft, conformité, risque",
            help="Chaque expression séparée par une virgule est mise entre guillemets et jointe par OR. Ex: analyste lcbft, conformité → \"analyste lcbft\" OR \"conformité\"",
        )

        # Param 2 — Job title
        job_title = st.text_input(
            "② Poste / Titre exact",
            placeholder="ex: Data Engineer",
            help="Sera cherché comme expression exacte entre guillemets",
        )

        # Param 3 — Location / include
        location = st.text_input(
            "③ Localisation ou mots à inclure",
            placeholder="ex: Paris, Lyon, France",
        )

        col_a, col_b = st.columns(2)
        with col_a:
            # Param 4 — Education
            education = st.selectbox(
                "④ Niveau d'études",
                list(EDUCATION_MAP.keys()),
            )
        with col_b:
            # Param 5 — Employer
            employer = st.text_input(
                "⑤ Employeur actuel",
                placeholder="ex: Google, LVMH",
            )

        # Intent
        intent = st.radio(
            "Intention de recherche",
            list(INTENT_MAP.keys()),
            horizontal=True,
        )

        # Custom exclusions
        with st.expander("➕ Exclusions personnalisées"):
            custom_excl = st.text_input(
                "Mots supplémentaires à exclure",
                placeholder="ex: junior, stage, offre",
            )
            st.caption(f"Exclusions par défaut : `{' '.join(DEFAULT_EXCLUSIONS)}`")

        generate = st.button("✨ Générer la requête", use_container_width=True)

    with col_right:
        st.markdown('<div class="section-header">📤 Résultat</div>', unsafe_allow_html=True)

        if generate or any([keywords, job_title, location, employer]):
            params = {
                "keywords": keywords,
                "job_title": job_title,
                "location": location,
                "education": education,
                "employer": employer,
                "intent": intent,
                "exclusions": custom_excl if "custom_excl" in dir() else "",
                "network": network,
            }

            if not any([keywords, job_title, location, employer]):
                st.warning("⚠️ Saisissez au moins un paramètre pour générer une requête.")
            else:
                result = build_query(params)

                # Stats
                op_count = result["query"].count(" OR ") + result["query"].count("-") + result["query"].count("+") + result["query"].count('"')
                st.markdown(f"""
                <div class="stats-row">
                  <div class="stat-chip">Mots entre guillemets : <span>{len(result['quoted_keywords'])}</span></div>
                  <div class="stat-chip">Opérateurs : <span>{op_count}</span></div>
                  <div class="stat-chip">Réseau : <span>{net_cfg['icon']} {network}</span></div>
                </div>
                """, unsafe_allow_html=True)

                # Main query
                st.markdown('<div class="section-header">Requête optimisée</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="result-box">{result["query"]}</div>', unsafe_allow_html=True)
                st.code(result["query"], language=None)

                # Google link
                st.markdown(f"""
                <a href="{result['google_url']}" target="_blank" class="google-btn">
                  🔍 Ouvrir dans Google
                </a>
                """, unsafe_allow_html=True)

                st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

                # PDF download
                pdf_bytes = generate_pdf(result, params)
                st.download_button(
                    label="📄 Télécharger le rapport PDF",
                    data=pdf_bytes,
                    file_name=f"xray_search_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )
        else:
            st.markdown("""
            <div style="text-align:center;padding:3rem 2rem;color:#4a4a6a;border:1px dashed #2a2a3d;border-radius:12px;margin-top:1rem">
              <div style="font-size:2.5rem;margin-bottom:1rem">🎯</div>
              <div style="font-size:1rem;font-weight:500;color:#6666aa">Remplissez les paramètres à gauche</div>
              <div style="font-size:0.85rem;margin-top:0.5rem">Votre requête Google optimisée apparaîtra ici</div>
            </div>
            """, unsafe_allow_html=True)


with tab2:
    st.markdown('<div class="section-header">📘 Guide des opérateurs Google avancés</div>', unsafe_allow_html=True)

    ops = [
        ("🔤", '"expression exacte"', 'Recherche la phrase telle quelle', '"data engineer Paris"'),
        ("🔀", "OR", "Alternative — l'un ou l'autre (MAJUSCULES!)", '"python" OR "django"'),
        ("➕", "+mot", "Mot obligatoirement présent", '+expert +python'),
        ("➖", "-mot", "Exclure les pages avec ce mot", '-forum -gratuit'),
        ("🌐", "site:domaine.com", "Limiter à un site ou domaine", 'site:linkedin.com/in'),
        ("🔗", "inurl:mot", "Mot dans l'URL de la page", 'inurl:profile inurl:github'),
        ("📄", "intitle:mot", "Mot dans le titre de la page", 'intitle:"curriculum vitae"'),
        ("📁", "filetype:ext", "Chercher un type de fichier", 'filetype:pdf "curriculum vitae"'),
        ("🔍", "related:site.com", "Sites similaires à un site donné", 'related:linkedin.com'),
        ("⭐", "* (wildcard)", "Remplace n'importe quel mot", '"développeur * Paris"'),
        ("📅", "after: / before:", "Filtrer par date de publication", 'after:2024-01-01'),
    ]

    for icon, op, desc, example in ops:
        col1, col2, col3 = st.columns([1.2, 2, 2])
        with col1:
            st.markdown(f'<span class="op-badge op-quote" style="font-size:0.85rem">{op}</span>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<span style="color:#d4d4f0;font-size:0.9rem">{desc}</span>', unsafe_allow_html=True)
        with col3:
            st.code(example, language=None)
        st.markdown('<div style="height:1px;background:#1a1a2a;margin:4px 0"></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">💡 Exemples de requêtes X-Ray</div>', unsafe_allow_html=True)

    examples = [
        ("LinkedIn · Dev Python Paris", 'site:linkedin.com/in "python" OR "django" "Paris" -recruteur -offre'),
        ("GitHub · Profils ML", 'site:github.com "machine learning" OR "deep learning" -forks -issues'),
        ("Stack Overflow · Experts Java", 'site:stackoverflow.com/users "java" "spring boot" -questions'),
        ("Recherche achat · SaaS", '"logiciel RH" OR "SIRH" +acheter OR +tarif OR +démo -forum -avis'),
    ]
    for title, query in examples:
        url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
        st.markdown(f"""
        <div style="margin:0.5rem 0">
          <div style="font-size:0.78rem;color:#7b61ff;font-weight:600;margin-bottom:3px">{title}</div>
          <div class="variant-box" style="margin:0">
            {query}
            <a href="{url}" target="_blank" style="color:#7b61ff;font-size:0.72rem;text-decoration:none;margin-left:12px">↗ Tester</a>
          </div>
        </div>
        """, unsafe_allow_html=True)
