# HPP Prediction Lean — Projet final Bloc 6 (Jedha)

Version **cadrée et suffisante** pour la certification CDSD : même data clinique Bourgogne, sans overengineering.

> Variante allégée du [Projet 9 — HPP Prediction](../Projet%209%20-%20Final%20Project%20-%20HPP%20Prediction).  
> Objectif : POC déployable + arbitrage métier assumé, pas un zoo de modèles.

## Problème métier

Prédire le risque d’**hémorragie du post-partum sévère** dès l’**admission**, avant l’accouchement, pour organiser la prise en charge (sang, astreinte, surveillance).

| Élément | Choix |
|--------|--------|
| Cible `HPPsev` | transfusion (`hpp_trans`) **ou** acte invasif (`embo`, `Tampo_int`, `hyst`, `liga`) |
| Moment | variables connues **avant / à l’admission** uniquement |
| KPI | **recall** prioritaire (+ PR-AUC) ; accuracy hors sujet (~99 % de négatifs) |
| Cadre | aide au triage, **pas** décision automatique — données anonymisées / RGPD |

## Ce qui est volontairement simple

| On fait | On ne fait pas |
|---------|----------------|
| 1 baseline Dummy + **LogReg `class_weight="balanced"`** | SMOTE / SMOTEENN / UnderSampler en batterie |
| 1 challenger RF optionnel | XGBoost + grids lourds |
| Seuil τ calibré sur validation (recall / volume d’alertes) | Seuil 0.5 par défaut sans discussion |
| Pipeline sklearn anti-leakage + joblib | Notebooks modèles séparés |
| Streamlit + Docker Compose | MLflow Spaces + FastAPI en doublon |

Leçon Jedha (Conversion / module 05) : un modèle simple bien seuillé > un boosting mal cadré.

## Structure

```text
Projet 9b - HPP Prediction Lean/
├── README.md
├── DATA_LOCATION.md
├── requirements.txt
├── src/
│   ├── config.py          # features, chemins, cible
│   ├── prepare_data.py    # brut → admission_hpp.csv
│   └── train.py           # baseline + LogReg + seuil + export
├── notebooks/
│   └── 01_eda_court.ipynb
├── data/processed/        # généré (gitignore)
├── artifacts/             # model + feature_order + meta (généré)
└── app/                   # POC Streamlit prêt Docker
    ├── app.py
    ├── Dockerfile
    ├── docker-compose.yml
    ├── artifacts/         # copie pour la démo
    └── data/demo_patients.csv
```

## Quickstart

```bash
cd "Projet 9b - HPP Prediction Lean"
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 1) Préparer (nécessite le CSV brut — voir DATA_LOCATION.md)
python -m src.prepare_data

# 2) Entraîner + exporter artefacts + CSV démo
python -m src.train

# 3) Démo locale
streamlit run app/app.py
```

### Docker

```bash
cd app
docker compose up --build
```

→ http://localhost:8501 → **Charger le dataset de démo** → **Prédire**

## Résultats (hold-out test, sklearn 1.6.1)

Prévalence `HPPsev` ≈ **0,82 %** (535 / 65 535). Seuil LogReg τ ≈ **0,45** (calibré sur validation : recall ≥ 65 % et taux d’alerte ≤ 35 %).

| Modèle | Recall | Precision | PR-AUC | Taux d’alerte |
|--------|--------|-----------|--------|---------------|
| Dummy (prior) | 0 % | — | 0,008 | 0 % |
| **LogReg `class_weight`** (retenu) | **57 %** | **1,4 %** | **0,093** | **32 %** |
| RF challenger | 65 % | 1,5 % | 0,035 | 34 % |

Interprétation orale : on bat clairement la baseline ; la RF n’apporte pas de gain de PR-AUC ; la faible précision est **attendue** sur un événement < 1 % et acceptée tant que le volume d’alertes reste gérable avec le clinicien. Détail : `app/artifacts/meta.json`.

## Oral Bloc 6 — angles clés

1. Traduction métier → data (admission, anti-leakage temporel).  
2. Métrique = coût d’erreur (recall).  
3. Choix de stack volontairement lean (délai + interprétabilité LogReg).  
4. POC industrialisé (joblib + Streamlit + Docker).  
5. Limites : précision faible, validation clinique prospective, monitoring du volume d’alertes.

## Confidentialité

Données PMSI anonymisées, usage pédagogique. Pas d’identifiants personnels dans le repo portfolio.
