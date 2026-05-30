# 🎯 Sniper Search Pro

> **Transformez vos mots-clés en requêtes Google ultra-optimisées** — 6 modes de recherche spécialisés avec export PDF.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)
![Python](https://img.shields.io/badge/Python-3.9+-blue)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Fonctionnalités

- 🎯 **6 onglets thématiques** : chaque onglet a ses inclusions et exclusions optimisées par défaut
- 🔤 **Guillemets automatiques** : chaque expression entre virgules → `"expression"` + `OR`
- 🌐 **8 réseaux** : LinkedIn, GitHub, Stack Overflow, Twitter/X, Wellfound, Dribbble, Behance, Google
- 📄 **Export PDF** professionnel avec guide des opérateurs
- 🔗 **Lien direct Google** pour chaque requête générée
- 💡 **Exemples intégrés** dans chaque onglet

---

## 🗂️ Les 6 onglets

| Onglet | Usage | Inclusions auto |
|--------|-------|-----------------|
| 🎓 **Étudiant & Emploi** | Stages, alternances, job dating | `+Master2 +étudiant +Paris +2026` |
| 💰 **Financement & Bourses** | Bourses, prêts étudiants, aides | `+France +2026 +Master` |
| 🚀 **Entrepreneuriat** | Startups, incubateurs, co-fondateurs | `+startup +Paris +2026` |
| 🚗 **Véhicules & Logement** | Voitures, colocations, studios | `+étudiant +Paris +2026` |
| 🛍️ **Discount & Économies** | Codes promo, soldes, avantages | `+valide +2026 +étudiant` |
| 👤 **Personnes & Conformité** | AML, KYC, PEP, sanctions OFAC/UE | *(opérateurs manuels)* |

---

## 📐 Logique des mots-clés

La **virgule** est le seul séparateur entre expressions. Les espaces dans une expression font partie de cette expression :

| Saisie | Requête générée |
|--------|----------------|
| `analyste lcbft` | `"analyste lcbft"` |
| `analyste lcbft, conformité` | `"analyste lcbft" OR "conformité"` |
| `Jack Pierre, sanctions OFAC` | `"Jack Pierre" OR "sanctions OFAC"` |

### Opérateurs utilisés

| Opérateur | Effet |
|-----------|-------|
| `"mot"` | Correspondance exacte |
| `OR` | Alternative (MAJUSCULES obligatoires) |
| `+mot` | Mot obligatoirement inclus |
| `-mot` | Mot à exclure |
| `site:` | Restriction au domaine |

---

## 🚀 Déploiement

### Streamlit Cloud (recommandé)

1. **Forkez** ce dépôt sur GitHub
2. Allez sur **[share.streamlit.io](https://share.streamlit.io)**
3. Sélectionnez votre fork → fichier `app.py` → **Deploy**

### En local

```bash
git clone https://github.com/VOTRE_USERNAME/sniper-search-pro.git
cd sniper-search-pro/xray-search
pip install -r requirements.txt
streamlit run app.py
```

---

## 🗂️ Structure du projet

```
xray-search/
├── app.py                  ← Application Streamlit principale
├── requirements.txt        ← streamlit + reportlab
├── .streamlit/
│   └── config.toml         ← Thème sombre
└── README.md
```

---

## 👤 Onglet Conformité / AML — exemples

```
# Recherche PEP
"nom prénom" +PEP OR "politically exposed person" +gouvernement +ministre -forum

# Sanctions OFAC/UE
"nom prénom" +OFAC OR "SDN list" OR "sanctions list" +USA OR +EU -forum

# Blanchiment / AML
"nom prénom" +"money laundering" OR "blanchiment" +banque +fraude -forum

# Watchlist complète
"nom prénom" +OFAC OR +UN OR +EU OR +FATF +sanctions OR "liste noire" -PDF
```

---

## 📄 Licence

MIT — libre d'utilisation, modification et redistribution.

---

*Inspiré de [Recruit'em / RecruitIn](https://recruitin.net) — étendu pour les cas d'usage étudiants et conformité*
