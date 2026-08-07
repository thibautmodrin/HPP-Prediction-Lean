"""POC Streamlit — scoring HPP sévère à l'admission (aide au triage)."""

from __future__ import annotations

import json
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
ART = ROOT / "artifacts"
DEMO = ROOT / "data" / "demo_patients.csv"


@st.cache_resource
def load_bundle():
    model = joblib.load(ART / "model_logreg.joblib")
    features = joblib.load(ART / "feature_order.joblib")
    meta = json.loads((ART / "meta.json").read_text(encoding="utf-8"))
    return model, features, meta


st.set_page_config(page_title="HPP Lean — triage admission", layout="wide")
st.title("Prédiction du risque d'HPP sévère")
st.caption(
    "Aide au triage à l'admission — pas une décision médicale automatique. "
    "Priorité métier : rappel (ne pas rater un cas critique)."
)

try:
    model, features, meta = load_bundle()
except Exception as e:
    st.error(f"Artefacts introuvables ou incompatibles : {e}")
    st.info("Lancez `python -m src.train` depuis la racine du projet, puis relancez l'app.")
    st.stop()

thr = float(meta.get("threshold", 0.5))
test_m = meta.get("test_metrics_logreg", {})

c1, c2, c3, c4 = st.columns(4)
c1.metric("Seuil τ", f"{thr:.3f}")
c2.metric("Recall (test)", f"{test_m.get('recall', float('nan')):.0%}" if test_m else "—")
c3.metric("Precision (test)", f"{test_m.get('precision', float('nan')):.0%}" if test_m else "—")
c4.metric("Taux d'alerte (test)", f"{test_m.get('alert_rate', float('nan')):.0%}" if test_m else "—")

with st.expander("Colonnes attendues"):
    st.code(", ".join(features))

st.subheader("Données d'entrée")
col_a, col_b = st.columns([1, 2])
with col_a:
    load_demo = st.button("Charger le dataset de démo", use_container_width=True)
with col_b:
    uploaded = st.file_uploader("Ou importer un CSV (mêmes colonnes)", type="csv")

if "data" not in st.session_state:
    st.session_state.data = None
    st.session_state.label = None

if load_demo:
    if not DEMO.exists():
        st.error(f"Démo introuvable : {DEMO}")
        st.stop()
    st.session_state.data = pd.read_csv(DEMO)
    st.session_state.label = DEMO.name

if uploaded is not None:
    st.session_state.data = pd.read_csv(uploaded)
    st.session_state.label = uploaded.name

data = st.session_state.data
if data is None:
    st.stop()

st.success(f"Chargé : **{st.session_state.label}** — {data.shape[0]} × {data.shape[1]}")
st.code(data.head(10).to_string(index=False))

missing = [c for c in features if c not in data.columns]
if missing:
    st.error(f"Colonnes manquantes : {missing}")
    st.stop()

if st.button("Prédire", type="primary"):
    X = data[features].copy()
    proba = model.predict_proba(X)[:, 1]
    pred = (proba >= thr).astype(int)
    out = X.copy()
    out["proba_hpp_sev"] = (proba * 100).round(2)
    out["alerte"] = pred
    out = out.sort_values("proba_hpp_sev", ascending=False)

    st.subheader("Résultats")
    st.code(out.to_string(index=False))
    n_alert = int(pred.sum())
    st.info(
        f"Alertes (proba ≥ {thr:.3f}) : **{n_alert}** / {len(pred)} "
        f"({100 * n_alert / len(pred):.0f} %)"
    )
    st.caption(meta.get("notes", ""))
