# Rendre le dossier Lean complet

Le **code** est déjà dans Git. Il manque deux choses pour une démo qui marche : le CSV brut (chez toi, pas sur GitHub) et les **`.joblib`** (à générer puis committer).

Ne **pas** pusher `Bourgogne20132023.csv` (données cliniques, ~28 Mo).

## Chez toi, dans l’ordre

### 1. Récupérer le CSV brut

Fichier Drive : [Bourgogne20132023.csv](https://drive.google.com/file/d/1ftl9VysHENLKHLAXkeGhwXz2b-tkNP7t/view) (~28 Mo).

```bash
cd HPP-Prediction-Lean
mkdir -p data/raw
# copier le CSV téléchargé :
cp ~/Téléchargements/Bourgogne20132023.csv data/raw/Bourgogne20132023.csv
```

### 2. Entraîner (écrit les artefacts)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

python -m src.prepare_data
python -m src.train
```

Contrôle : tu dois voir ~**65 535** lignes et ~**535** positifs, et les fichiers :

- `app/artifacts/model_logreg.joblib`
- `app/artifacts/feature_order.joblib`
- `app/artifacts/meta.json` (déjà présent ; il sera mis à jour)

### 3. Vérifier la démo

```bash
streamlit run app/app.py
# → Charger le dataset de démo → Prédire

cd app && docker compose up --build
# → http://localhost:8501
```

### 4. Committer **uniquement** les `.joblib` (pas le CSV)

```bash
git add app/artifacts/model_logreg.joblib app/artifacts/feature_order.joblib app/artifacts/meta.json
git status   # data/raw/*.csv et data/processed/*.csv doivent rester hors Git
git commit -m "chore: artefacts LogReg pour la démo Streamlit/Docker"
git push
```

Après ça, un clone + `docker compose up` suffit **sans** le CSV.

## Déjà dans Git (rien à refaire)

Code (`src/`, `app/app.py`, Docker), CSV de démo, `meta.json` (chiffres d’oral), notebook EDA, fiches `docs/`.
