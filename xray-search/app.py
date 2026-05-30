
cat > /home/claude/xray-search/app.py << 'PYEOF'
import streamlit as st
import urllib.parse
import io
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_CENTER

st.set_page_config(page_title="Sniper Search Pro", page_icon="🎯", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');
html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; }
#MainMenu {visibility:hidden;} footer {visibility:hidden;} header {visibility:hidden;}
.stApp { background:#0a0a0f; color:#e8e8f0; }
.hero-title { font-size:2.8rem; font-weight:700; background:linear-gradient(135deg,#4af7c4 0%,#7b61ff 50%,#ff6b9d 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; letter-spacing:-1px; margin-bottom:.2rem; }
.hero-subtitle { font-size:1rem; color:#8888aa; margin-bottom:1.5rem; font-weight:300; }
.result-box { background:#13131f; border:1px solid #2a2a3d; border-left:4px solid #4af7c4; border-radius:12px; padding:1.5rem; margin:1rem 0; font-family:'JetBrains Mono',monospace; font-size:.88rem; word-break:break-all; line-height:1.7; color:#c8f7e8; }
.example-box { background:#0f0f1a; border:1px solid #1e1e2e; border-radius:8px; padding:.8rem 1rem; margin:.4rem 0; font-family:'JetBrains Mono',monospace; font-size:.78rem; word-break:break-all; color:#aaaacc; line-height:1.6; }
.section-header { font-size:.72rem; font-weight:600; text-transform:uppercase; letter-spacing:2px; color:#7b61ff; margin:1.2rem 0 .6rem; }
.tab-label { font-size:.78rem; font-weight:600; text-transform:uppercase; letter-spacing:1.5px; color:#4af7c4; margin-bottom:.8rem; }
.stats-row { display:flex; gap:12px; margin:.8rem 0; flex-wrap:wrap; }
.stat-chip { background:#1e1e30; border:1px solid #2a2a3d; border-radius:8px; padding:5px 12px; font-size:.78rem; color:#9999bb; }
.stat-chip span { color:#4af7c4; font-weight:600; }
.op-badge { display:inline-block; padding:2px 8px; border-radius:4px; font-family:'JetBrains Mono',monospace; font-size:.73rem; font-weight:600; margin:2px; }
.op-quote { background:#1a3d2a; color:#4af7c4; border:1px solid #2d6644; }
.op-or    { background:#2a1a3d; color:#a88fff; border:1px solid #5d3d8a; }
.op-plus  { background:#1a2a3d; color:#6bb5ff; border:1px solid #2d4d6a; }
.op-minus { background:#3d1a1a; color:#ff8888; border:1px solid #6a2d2d; }
.op-site  { background:#3d2a1a; color:#ffbb66; border:1px solid #6a4d2d; }
.google-btn { display:inline-flex; align-items:center; gap:8px; background:linear-gradient(135deg,#4af7c4,#7b61ff); color:#000; padding:9px 22px; border-radius:8px; font-weight:700; font-size:.9rem; text-decoration:none; }
.fancy-divider { height:1px; background:linear-gradient(90deg,transparent,#2a2a3d,transparent); margin:1.5rem 0; }
.tip-box { background:#0f1a2a; border:1px solid #1a3d5a; border-radius:8px; padding:.7rem 1rem; margin:.5rem 0; font-size:.82rem; color:#8888aa; }
.tip-box strong { color:#6bb5ff; }
.excl-box { background:#1a0f0f; border:1px solid #3d1a1a; border-radius:8px; padding:.7rem 1rem; margin:.5rem 0; font-size:.8rem; color:#cc9999; }
.stTextInput > div > div > input, .stTextArea > div > div > textarea, .stSelectbox > div > div { background:#13131f !important; border:1px solid #2a2a3d !important; color:#e8e8f0 !important; border-radius:8px !important; }
.stTextInput label, .stTextArea label, .stSelectbox label, .stMultiSelect label, .stRadio label { color:#9999bb !important; font-size:.8rem !important; font-weight:500 !important; text-transform:uppercase !important; letter-spacing:1.2px !important; }
.stTabs [data-baseweb="tab-list"] { background:#13131f; border-radius:10px; padding:4px; gap:4px; flex-wrap:wrap; }
.stTabs [data-baseweb="tab"] { background:transparent; color:#8888aa; border-radius:8px; font-weight:500; }
.stTabs [aria-selected="true"] { background:#1e1e30 !important; color:#4af7c4 !important; }
.stButton > button { background:linear-gradient(135deg,#4af7c4 0%,#7b61ff 100%) !important; color:#000 !important; font-weight:700 !important; border:none !important; border-radius:8px !important; padding:.6rem 2rem !important; font-size:.92rem !important; }
.stDownloadButton > button { background:#1e1e30 !important; color:#4af7c4 !important; border:1px solid #4af7c4 !important; border-radius:8px !important; font-weight:600 !important; }
</style>
""", unsafe_allow_html=True)

# ─── Data ──────────────────────────────────────────────────────────────────────

NETWORKS = {
    "LinkedIn":        {"icon": "💼", "site": "linkedin.com/in",        "extra": "site:linkedin.com/in OR site:linkedin.com/pub"},
    "GitHub":          {"icon": "🐙", "site": "github.com",             "extra": "site:github.com"},
    "Stack Overflow":  {"icon": "📚", "site": "stackoverflow.com/users","extra": "site:stackoverflow.com/users"},
    "Twitter/X":       {"icon": "🐦", "site": "x.com",                  "extra": "site:x.com OR site:twitter.com"},
    "Wellfound":       {"icon": "🚀", "site": "wellfound.com",          "extra": "site:wellfound.com/u"},
    "Dribbble":        {"icon": "🎨", "site": "dribbble.com",           "extra": "site:dribbble.com"},
    "Behance":         {"icon": "✏️", "site": "behance.net",            "extra": "site:behance.net"},
    "Google (général)":{"icon": "🌐", "site": "",                       "extra": ""},
}

EDUCATION_MAP = {
    "Tous niveaux":   "",
    "Licence / Bac+3":'"licence" OR "bachelor" OR "bac+3"',
    "Master / Bac+5": '"master" OR "mastère" OR "bac+5" OR "msc" OR "mba"',
    "Doctorat":       '"doctorat" OR "phd" OR "docteur"',
}

TABS = {
    "🎓 Étudiant & Emploi": {
        "placeholder_kw":   "ex: stagiaire finance, alternance analyste",
        "placeholder_title":"ex: analyste junior, compliance officer",
        "placeholder_loc":  "ex: Paris, Île-de-France",
        "placeholder_emp":  "ex: ESLSCA, Revolut, BNP",
        "placeholder_excl": "ex: senior, CDI, payant",
        "examples": [
            ("Stage finance Paris",    '"stagiaire finance" OR "alternance" "Paris" -forum -PDF'),
            ("Alternance conformité",  '"alternance conformité" OR "alternance compliance" "Paris" -forum -PDF'),
            ("Job dating étudiant",    '"job dating" OR "forum emploi" "finance" "Paris" -gratuit'),
        ],
        "tips": "💡 Virgule = expressions distinctes. <code>stagiaire finance, alternance</code> → <code>\"stagiaire finance\" OR \"alternance\"</code>",
    },
    "💰 Financement & Bourses": {
        "placeholder_kw":   "ex: bourse étudiant, aide financière Master",
        "placeholder_title":"ex: bourse excellence, prêt étudiant",
        "placeholder_loc":  "ex: France, CROUS, Île-de-France",
        "placeholder_emp":  "ex: CROUS, Fondation, Banque",
        "placeholder_excl": "ex: arnaque, scam, remboursé",
        "examples": [
            ("Bourses Master",         '"bourse étudiant" OR "bourse Master" "France" -arnaque -scam'),
            ("Prêt étudiant",          '"prêt étudiant" OR "crédit étudiant" "banque" "France" -arnaque'),
            ("Aides financières",      '"aide financière étudiant" OR "subvention formation" "France" -forum'),
        ],
        "tips": "💡 Précisez <code>CROUS</code> ou votre région dans la localisation pour cibler les aides territoriales.",
    },
    "🚀 Entrepreneuriat": {
        "placeholder_kw":   "ex: création entreprise, incubateur Paris",
        "placeholder_title":"ex: co-fondateur, entrepreneur",
        "placeholder_loc":  "ex: Station F, French Tech, Paris",
        "placeholder_emp":  "ex: Bpifrance, Station F, French Tech",
        "placeholder_excl": "ex: arnaque, formation payante",
        "examples": [
            ("Startup fintech Paris",  '"startup fintech" OR "création entreprise" "Paris" -forum -arnaque'),
            ("Incubateurs Paris",      '"incubateur Paris" OR "pépinière entreprise" OR "Station F" -gratuit'),
            ("Financement startup",    '"aide startup" OR "subvention startup" OR "Bpifrance" "France" -arnaque'),
        ],
        "tips": "💡 Mettez <code>Station F</code> ou <code>French Tech</code> dans la localisation pour cibler l'écosystème startup.",
    },
    "🚗 Véhicules & Logement": {
        "placeholder_kw":   "ex: voiture occasion, colocation Paris",
        "placeholder_title":"ex: studio, appartement, location",
        "placeholder_loc":  "ex: Paris, Versailles, Île-de-France",
        "placeholder_emp":  "ex: SeLoger, Leboncoin, CROUS",
        "placeholder_excl": "ex: arnaque, scam, indisponible",
        "examples": [
            ("Voiture occasion Paris", '"voiture occasion" OR "crédit auto" "Paris" -arnaque -scam'),
            ("Logement étudiant Paris",'"appartement étudiant" OR "studio" OR "CROUS logement" "Paris" -arnaque'),
            ("Colocation Paris",       '"colocation Paris" OR "coloc" "disponible" -arnaque -scam'),
        ],
        "tips": "💡 Ajoutez <code>arnaque, scam</code> dans les exclusions pour filtrer les annonces frauduleuses.",
    },
    "🛍️ Discount & Économies": {
        "placeholder_kw":   "ex: code promo, réduction étudiant",
        "placeholder_title":"ex: promo, réduction, avantage étudiant",
        "placeholder_loc":  "ex: France, en ligne",
        "placeholder_emp":  "ex: Amazon, Fnac, Edenred, Revolut",
        "placeholder_excl": "ex: expiré, scam, arnaque",
        "examples": [
            ("Codes promo étudiants",  '"code promo" OR "réduction étudiant" "France" -expiré -scam'),
            ("Soldes / Black Friday",  '"soldes" OR "Black Friday" "France" -expiré -arnaque'),
            ("Avantages carte étudiant",'"avantage étudiant" OR "carte étudiant" "France" -expiré'),
        ],
        "tips": "💡 Mettez <code>expiré</code> dans les exclusions pour ne voir que les offres actives.",
    },
    "👤 Personnes & Conformité": {
        "placeholder_kw":   "ex: Jack Pierre, sanctions OFAC",
        "placeholder_title":"ex: PEP, politically exposed person",
        "placeholder_loc":  "ex: France, Haïti, USA, UE",
        "placeholder_emp":  "ex: Banque, Gouvernement, OFAC, FATF",
        "placeholder_excl": "ex: homonyme, acteur, sportif",
        "examples": [
            ("Recherche PEP",          '"Jack Pierre" "PEP" OR "politically exposed person" "gouvernement" -forum'),
            ("Sanctions OFAC/UE",      '"Jack Pierre" "OFAC" OR "SDN list" OR "sanctions list" -forum'),
            ("AML / Blanchiment",      '"Jack Pierre" "money laundering" OR "blanchiment" OR "AML" -forum'),
            ("Watchlist complète",     '"Jack Pierre" "OFAC" OR "UN" OR "EU" OR "FATF" "sanctions" OR "liste noire" -PDF'),
        ],
        "tips": "💡 AML/KYC : mettez le <strong>nom complet</strong> dans les mots-clés. Combinez avec les opérateurs sanctions dans le titre.",
    },
}

# ─── Core logic ────────────────────────────────────────────────────────────────
def build_query(params: dict) -> dict:
    parts_main = []
    parts_quoted = []

    # Keywords: comma = separate expressions, each quoted
    kw_raw = params.get("keywords", "")
    if kw_raw:
        expressions = [e.strip() for e in kw_raw.split(",") if e.strip()]
        quoted = [f'"{e}"' for e in expressions]
        parts_quoted = quoted
        parts_main.append(" OR ".join(quoted))

    # Job title as exact phrase
    job_title = params.get("job_title", "").strip()
    if job_title:
        parts_main.insert(0, f'"{job_title}"')

    # Location
    location = params.get("location", "").strip()
    if location:
        parts_main.append(f'"{location}"')

    # Education
    edu = EDUCATION_MAP.get(params.get("education", "Tous niveaux"), "")
    if edu:
        parts_main.append(f"({edu})")

    # Employer
    employer = params.get("employer", "").strip()
    if employer:
        parts_main.append(f'"{employer}"')

    # Network site restriction
    network = params.get("network", "Google (général)")
    net_cfg = NETWORKS.get(network, NETWORKS["Google (général)"])
    if net_cfg["extra"]:
        parts_main.append(f"({net_cfg['extra']})")

    # Exclusions — only what the user typed
    excl_parts = []
    custom_excl = params.get("exclusions", "")
    if custom_excl:
        for e in custom_excl.split(","):
            token = e.strip().lstrip("-")
            if token:
                excl_parts.append(f"-{token}")

    base = " ".join(parts_main)
    excl_str = " ".join(excl_parts)
    full_query = f"{base} {excl_str}".strip()

    return {
        "query": full_query,
        "quoted_keywords": parts_quoted,
        "network": network,
        "net_cfg": net_cfg,
        "google_url": f"https://www.google.com/search?q={urllib.parse.quote(full_query)}",
    }


def generate_pdf(result: dict, params: dict, tab_name: str) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
        rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)

    styles = getSampleStyleSheet()
    accent  = colors.HexColor("#4af7c4")
    purple  = colors.HexColor("#7b61ff")
    light   = colors.HexColor("#e8e8f0")
    muted   = colors.HexColor("#8888aa")
    card_bg = colors.HexColor("#13131f")

    title_style   = ParagraphStyle("T",   parent=styles["Title"],  fontSize=22, textColor=accent, fontName="Helvetica-Bold", spaceAfter=4, alignment=TA_CENTER)
    sub_style     = ParagraphStyle("S",   parent=styles["Normal"], fontSize=9,  textColor=muted,  alignment=TA_CENTER, spaceAfter=16)
    section_style = ParagraphStyle("Sec", parent=styles["Normal"], fontSize=8,  textColor=purple, fontName="Helvetica-Bold", spaceBefore=14, spaceAfter=5)
    query_style   = ParagraphStyle("Q",   parent=styles["Code"],   fontSize=9,  textColor=accent, backColor=card_bg, borderPadding=12, fontName="Courier-Bold", leading=14)

    story = []
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("🎯 Sniper Search Pro", title_style))
    story.append(Paragraph(f"Rapport · {tab_name} · {datetime.now().strftime('%d/%m/%Y %H:%M')}", sub_style))
    story.append(HRFlowable(width="100%", thickness=1, color=purple, spaceAfter=14))

    story.append(Paragraph("PARAMÈTRES", section_style))
    pdata = [
        ["Onglet",          tab_name],
        ["Réseau",          params.get("network", "—")],
        ["Mots-clés",       params.get("keywords",  "—") or "—"],
        ["Titre / Poste",   params.get("job_title", "—") or "—"],
        ["Localisation",    params.get("location",  "—") or "—"],
        ["Niveau d'études", params.get("education", "—") or "—"],
        ["Employeur",       params.get("employer",  "—") or "—"],
        ["Mots à exclure",  params.get("exclusions","—") or "—"],
    ]
    tbl = Table(pdata, colWidths=[4*cm, 13*cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND",  (0,0),(0,-1), card_bg),
        ("BACKGROUND",  (1,0),(1,-1), colors.HexColor("#0f0f1a")),
        ("TEXTCOLOR",   (0,0),(0,-1), muted),
        ("TEXTCOLOR",   (1,0),(1,-1), light),
        ("FONTNAME",    (0,0),(0,-1), "Helvetica-Bold"),
        ("FONTSIZE",    (0,0),(-1,-1), 8),
        ("GRID",        (0,0),(-1,-1), 0.5, colors.HexColor("#2a2a3d")),
        ("TOPPADDING",  (0,0),(-1,-1), 5),
        ("BOTTOMPADDING",(0,0),(-1,-1), 5),
        ("LEFTPADDING", (0,0),(-1,-1), 8),
        ("RIGHTPADDING",(0,0),(-1,-1), 8),
    ]))
    story.append(tbl)

    story.append(Paragraph("REQUÊTE GOOGLE OPTIMISÉE", section_style))
    story.append(Paragraph(result["query"], query_style))
    story.append(Spacer(1, 0.4*cm))

    story.append(Paragraph("URL DE RECHERCHE", section_style))
    story.append(Paragraph(result["google_url"], ParagraphStyle(
        "URL", parent=styles["Normal"], fontSize=7, textColor=colors.HexColor("#6bb5ff"), fontName="Courier", leading=11)))

    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#2a2a3d"), spaceBefore=18, spaceAfter=10))
    story.append(Paragraph("GUIDE DES OPÉRATEURS", section_style))
    ops_data = [
        ['Opérateur', 'Usage', 'Exemple'],
        ['"mot"',   'Correspondance exacte',       '"analyste lcbft"'],
        ['OR',      'Alternative (MAJUSCULES)',     '"python" OR "django"'],
        ['-mot',    'Exclure un mot',               '-forum -gratuit'],
        ['site:',   'Restreindre au domaine',       'site:linkedin.com/in'],
        ['intitle:','Mot dans le titre de la page', 'intitle:"curriculum vitae"'],
        ['filetype:','Type de fichier',             'filetype:pdf'],
    ]
    otbl = Table(ops_data, colWidths=[3.5*cm, 7*cm, 6.5*cm])
    otbl.setStyle(TableStyle([
        ("BACKGROUND",  (0,0),(-1,0), purple),
        ("TEXTCOLOR",   (0,0),(-1,0), colors.white),
        ("FONTNAME",    (0,0),(-1,0), "Helvetica-Bold"),
        ("FONTSIZE",    (0,0),(-1,-1), 8),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [card_bg, colors.HexColor("#0f0f1a")]),
        ("TEXTCOLOR",   (0,1),(-1,-1), light),
        ("FONTNAME",    (0,1),(0,-1),  "Courier-Bold"),
        ("TEXTCOLOR",   (0,1),(0,-1),  accent),
        ("GRID",        (0,0),(-1,-1), 0.5, colors.HexColor("#2a2a3d")),
        ("TOPPADDING",  (0,0),(-1,-1), 5),
        ("BOTTOMPADDING",(0,0),(-1,-1), 5),
        ("LEFTPADDING", (0,0),(-1,-1), 8),
        ("RIGHTPADDING",(0,0),(-1,-1), 8),
    ]))
    story.append(otbl)
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("Sniper Search Pro — Recherche Google avancée",
        ParagraphStyle("Footer", parent=styles["Normal"], fontSize=7, textColor=muted, alignment=TA_CENTER)))
    doc.build(story)
    return buffer.getvalue()


# ─── UI ────────────────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title">🎯 Sniper Search Pro</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Transformez vos mots-clés en requêtes Google ultra-précises · 6 modes de recherche spécialisés</div>', unsafe_allow_html=True)

st.markdown("""
<div style="margin-bottom:1.2rem">
  <span class="op-badge op-quote">"mot"</span> exacte &nbsp;
  <span class="op-badge op-or">OR</span> alternative &nbsp;
  <span class="op-badge op-minus">-mot</span> exclure &nbsp;
  <span class="op-badge op-site">site:</span> domaine
</div>
""", unsafe_allow_html=True)

main_tabs = st.tabs(list(TABS.keys()) + ["📖 Guide"])

for idx, (tab_name, tab_cfg) in enumerate(TABS.items()):
    with main_tabs[idx]:
        col_left, col_right = st.columns([1.1, 1], gap="large")

        with col_left:
            st.markdown(f'<div class="tab-label">{tab_name}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="tip-box">{tab_cfg["tips"]}</div>', unsafe_allow_html=True)

            network = st.selectbox("Réseau / Plateforme", list(NETWORKS.keys()), key=f"net_{idx}")
            net_cfg = NETWORKS[network]
            st.markdown(
                f'<div style="font-size:.78rem;color:#8888aa;margin-top:-8px;margin-bottom:10px">'
                f'{net_cfg["icon"]} Recherche sur <code style="color:#4af7c4">'
                f'{net_cfg["site"] or "tous les sites"}</code></div>',
                unsafe_allow_html=True)

            keywords = st.text_input(
                "① Mots-clés ou expressions (séparés par virgule)",
                placeholder=tab_cfg["placeholder_kw"],
                help='Chaque expression séparée par une virgule → entre guillemets + OR. Ex: "analyste lcbft, conformité" → "analyste lcbft" OR "conformité"',
                key=f"kw_{idx}")

            job_title = st.text_input("② Titre / Poste exact",
                placeholder=tab_cfg["placeholder_title"], key=f"jt_{idx}")

            location = st.text_input("③ Localisation ou termes à inclure",
                placeholder=tab_cfg["placeholder_loc"], key=f"loc_{idx}")

            col_a, col_b = st.columns(2)
            with col_a:
                education = st.selectbox("④ Niveau d'études", list(EDUCATION_MAP.keys()), key=f"edu_{idx}")
            with col_b:
                employer = st.text_input("⑤ Employeur / Organisation",
                    placeholder=tab_cfg["placeholder_emp"], key=f"emp_{idx}")

            # Exclusions — visible directly, not hidden in expander
            st.markdown('<div class="section-header" style="color:#ff8888">⊖ Mots à exclure</div>', unsafe_allow_html=True)
            custom_excl = st.text_input(
                "Mots ou expressions à exclure des résultats (séparés par virgule)",
                placeholder=tab_cfg["placeholder_excl"],
                help="Chaque mot sera précédé de - dans la requête. Ex: arnaque, forum → -arnaque -forum",
                key=f"excl_{idx}")
            if custom_excl:
                excl_preview = " ".join(f"-{e.strip().lstrip('-')}" for e in custom_excl.split(",") if e.strip())
                st.markdown(f'<div class="excl-box">Exclusions : <code>{excl_preview}</code></div>', unsafe_allow_html=True)

            generate = st.button("✨ Générer la requête", key=f"gen_{idx}", use_container_width=True)

        with col_right:
            st.markdown('<div class="section-header">📤 Résultat</div>', unsafe_allow_html=True)

            has_input = any([keywords, job_title, location, employer])

            if generate or has_input:
                params = {
                    "keywords":   keywords,
                    "job_title":  job_title,
                    "location":   location,
                    "education":  education,
                    "employer":   employer,
                    "exclusions": custom_excl,
                    "network":    network,
                }
                if not has_input:
                    st.warning("⚠️ Saisissez au moins un paramètre.")
                else:
                    result = build_query(params)

                    nb_excl = len([e for e in custom_excl.split(",") if e.strip()]) if custom_excl else 0
                    st.markdown(f"""
                    <div class="stats-row">
                      <div class="stat-chip">Expressions : <span>{len(result['quoted_keywords'])}</span></div>
                      <div class="stat-chip">Exclusions : <span>{nb_excl}</span></div>
                      <div class="stat-chip">Réseau : <span>{net_cfg['icon']} {network}</span></div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown('<div class="section-header">Requête optimisée</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="result-box">{result["query"]}</div>', unsafe_allow_html=True)
                    st.code(result["query"], language=None)

                    st.markdown(f"""
                    <a href="{result['google_url']}" target="_blank" class="google-btn">
                      🔍 Ouvrir dans Google
                    </a>
                    """, unsafe_allow_html=True)

                    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

                    pdf_bytes = generate_pdf(result, params, tab_name)
                    st.download_button(
                        label="📄 Télécharger le rapport PDF",
                        data=pdf_bytes,
                        file_name=f"sniper_{tab_name.split()[0]}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                        mime="application/pdf",
                        key=f"pdf_{idx}",
                        use_container_width=True,
                    )
            else:
                st.markdown('<div class="section-header">💡 Exemples pour cet onglet</div>', unsafe_allow_html=True)
                for ex_title, ex_query in tab_cfg["examples"]:
                    ex_url = f"https://www.google.com/search?q={urllib.parse.quote(ex_query)}"
                    st.markdown(f"""
                    <div style="margin:.5rem 0">
                      <div style="font-size:.75rem;color:#7b61ff;font-weight:600;margin-bottom:3px">{ex_title}</div>
                      <div class="example-box">
                        {ex_query}
                        <a href="{ex_url}" target="_blank" style="color:#7b61ff;font-size:.72rem;text-decoration:none;margin-left:12px">↗ Tester</a>
                      </div>
                    </div>
                    """, unsafe_allow_html=True)

# ── Guide tab ──
with main_tabs[len(TABS)]:
    st.markdown('<div class="section-header">📘 Guide des opérateurs Google avancés</div>', unsafe_allow_html=True)
    ops = [
        ('"expression exacte"', "Recherche la phrase telle quelle",           '"analyste lcbft"'),
        ("OR",                  "Alternative — l'un ou l'autre (MAJUSCULES!)", '"python" OR "django"'),
        ("-mot",                "Exclure les pages contenant ce mot",          '-forum -gratuit -arnaque'),
        ("site:domaine.com",    "Limiter la recherche à un site",              'site:linkedin.com/in'),
        ("inurl:mot",           "Mot présent dans l'URL de la page",           'inurl:profile inurl:cv'),
        ("intitle:mot",         "Mot présent dans le titre de la page",        'intitle:"curriculum vitae"'),
        ("filetype:ext",        "Chercher un type de fichier",                 'filetype:pdf "rapport annuel"'),
        ('"mot1 * mot2"',       "Wildcard — remplace n'importe quel mot",      '"directeur * finance"'),
        ("after:AAAA-MM-JJ",   "Pages publiées après une date donnée",        'after:2025-01-01'),
    ]
    for op, desc, example in ops:
        c1, c2, c3 = st.columns([1.4, 2, 2])
        with c1: st.markdown(f'<span class="op-badge op-quote" style="font-size:.82rem">{op}</span>', unsafe_allow_html=True)
        with c2: st.markdown(f'<span style="color:#d4d4f0;font-size:.88rem">{desc}</span>', unsafe_allow_html=True)
        with c3: st.code(example, language=None)
        st.markdown('<div style="height:1px;background:#1a1a2a;margin:4px 0"></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">🎯 Exemples par cas d\'usage</div>', unsafe_allow_html=True)
    all_examples = [
        ("🎓 LinkedIn · Analyste conformité Paris", 'site:linkedin.com/in "analyste lcbft" OR "compliance officer" "Paris" -recruteur'),
        ("💰 Bourses Master Finance",               '"bourse étudiant" OR "bourse Master" "finance" "France" -arnaque'),
        ("🚀 Startup Fintech Paris",                '"startup fintech" OR "création entreprise" "Paris" -forum -arnaque'),
        ("👤 Conformité AML · Recherche personne",  '"Jack Pierre" "OFAC" OR "PEP" OR "sanctions" "liste noire" -forum'),
        ("🛍️ Codes promo étudiants valides",        '"code promo" OR "réduction étudiant" "France" -expiré -scam'),
        ("🚗 Colocation étudiant Paris",            '"colocation Paris" OR "coloc" "disponible" -arnaque -scam'),
    ]
    for title, query in all_examples:
        url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
        st.markdown(f"""
        <div style="margin:.5rem 0">
          <div style="font-size:.75rem;color:#7b61ff;font-weight:600;margin-bottom:3px">{title}</div>
          <div class="example-box">
            {query}
            <a href="{url}" target="_blank" style="color:#7b61ff;font-size:.72rem;text-decoration:none;margin-left:12px">↗ Tester</a>
          </div>
        </div>
        """, unsafe_allow_html=True)
