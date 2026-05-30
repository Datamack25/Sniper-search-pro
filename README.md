[README.md](https://github.com/user-attachments/files/28422527/README.md)
# 🔍 X-Ray Search Pro

> **Transformez vos mots-clés bruts en requêtes Google ultra-optimisées** — Recherche X-Ray multi-plateformes avec export PDF.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)
![Python](https://img.shields.io/badge/Python-3.9+-blue)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Fonctionnalités

- 🎯 **5 paramètres de recherche** : mots-clés, poste, localisation, niveau d'études, employeur
- 🔤 **Guillemets automatiques** sur chaque mot-clé pour une correspondance exacte
- 🌐 **10+ réseaux supportés** : LinkedIn, GitHub, Stack Overflow, Twitter/X, Wellfound, Dribbble, Behance…
- 🎨 **4 variantes** générées automatiquement selon l'intention (général, achat, app, pro)
- ➖ **Exclusions intelligentes** par défaut + personnalisables
- 📄 **Export PDF** professionnel avec guide des opérateurs
- 🔗 **Liens directs Google** pour chaque requête générée

## 🚀 Déploiement rapide

### Streamlit Cloud

1. Fork ce dépôt
2. Connectez-vous sur [share.streamlit.io](https://share.streamlit.io)
3. Sélectionnez votre fork → `app.py` → Deploy

### Local

```bash
git clone https://github.com/VOTRE_USERNAME/xray-search-pro.git
cd xray-search-pro
pip install -r requirements.txt
streamlit run app.py
```

## 📐 Comment ça marche

| Paramètre | Effet | Exemple |
|-----------|-------|---------|
| **Mots-clés** | `"mot"` avec guillemets, joints par `OR` | `"python" OR "django"` |
| **Poste** | Expression exacte en tête de requête | `"Data Engineer"` |
| **Localisation** | Ajouté entre guillemets | `"Paris"` |
| **Éducation** | Termes de diplôme en alternatif | `"master" OR "bac+5"` |
| **Employeur** | Nom d'entreprise exact | `"Google"` |

### Opérateurs générés

```
"mot"    → correspondance exacte
OR       → alternative (majuscules obligatoires)
+mot     → mot obligatoirement inclus
-mot     → exclusion
site:    → restriction au domaine
```

### Exemple de sortie

**Entrée :** `python, django` · Poste: `Data Engineer` · Lieu: `Paris`

**Requête générée :**
```
"Data Engineer" "python" OR "django" "Paris" (site:linkedin.com/in OR site:linkedin.com/pub) -gratuit -avis -forum -PDF -emploi -occasion -wiki -discount
```

## 🗂️ Structure du projet

```
xray-search-pro/
├── app.py                  # Application principale Streamlit
├── requirements.txt        # Dépendances Python
├── .streamlit/
│   └── config.toml         # Configuration thème sombre
└── README.md
```

## 📄 Licence

MIT — libre d'utilisation, modification et redistribution.

---

*Inspiré de [Recruit'em / RecruitIn](https://recruitin.net) — outil de X-Ray search pour recruteurs*
