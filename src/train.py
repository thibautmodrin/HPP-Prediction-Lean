"""
Entraînement lean : Dummy + LogReg(class_weight) + RF optionnel, seuil métier.

Usage:
  python -m src.train
  python -m src.train --skip-rf
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import sklearn
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    average_precision_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_recall_curve,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.config import (
    ARTIFACTS_DIR,
    CAT_FEATURES,
    DEMO_CSV,
    FEATURES,
    NUM_FEATURES,
    PROCESSED_DIR,
    RANDOM_STATE,
    TARGET,
    TEST_SIZE,
    VAL_SIZE,
)
from src.prepare_data import main as prepare_main


def make_preprocessor() -> ColumnTransformer:
    return ColumnTransformer(
        transformers=[
            (
                "num",
                Pipeline(
                    [
                        ("imp", SimpleImputer(strategy="median")),
                        ("sc", StandardScaler()),
                    ]
                ),
                NUM_FEATURES,
            ),
            (
                "cat",
                Pipeline(
                    [
                        ("imp", SimpleImputer(strategy="most_frequent")),
                        ("oh", OneHotEncoder(handle_unknown="ignore")),
                    ]
                ),
                CAT_FEATURES,
            ),
        ]
    )


def metrics_at_threshold(y_true, proba, thr: float) -> dict:
    pred = (proba >= thr).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_true, pred, labels=[0, 1]).ravel()
    return {
        "threshold": float(thr),
        "precision": float(precision_score(y_true, pred, zero_division=0)),
        "recall": float(recall_score(y_true, pred, zero_division=0)),
        "f1": float(f1_score(y_true, pred, zero_division=0)),
        "tp": int(tp),
        "fp": int(fp),
        "fn": int(fn),
        "tn": int(tn),
        "alert_rate": float(pred.mean()),
    }


def choose_threshold_for_recall(
    y_true, proba, min_recall: float = 0.65, max_alert_rate: float = 0.35
) -> tuple[float, dict]:
    """
    Seuil métier HPP : viser un recall minimal tout en limitant le volume d'alertes.
    Si impossible, maximise le recall sous contrainte d'alert_rate.
    """
    precisions, recalls, thresholds = precision_recall_curve(y_true, proba)
    # thresholds a len = len(precisions) - 1
    best = None
    for thr, r, p in zip(thresholds, recalls[:-1], precisions[:-1]):
        pred = (proba >= thr).astype(int)
        alert = float(pred.mean())
        if r < min_recall or alert > max_alert_rate:
            continue
        score = (r, -alert, p)  # recall haut, peu d'alertes, precision
        row = metrics_at_threshold(y_true, proba, float(thr))
        if best is None or score > best[0]:
            best = (score, float(thr), row)

    if best is not None:
        return best[1], best[2]

    # Fallback : maximiser recall sous plafond d'alertes
    fallback = None
    for thr in thresholds:
        row = metrics_at_threshold(y_true, proba, float(thr))
        if row["alert_rate"] > max_alert_rate:
            continue
        key = (row["recall"], row["precision"])
        if fallback is None or key > fallback[0]:
            fallback = (key, float(thr), row)
    if fallback is not None:
        return fallback[1], fallback[2]

    # Dernier recours : seuil 0.5
    return 0.5, metrics_at_threshold(y_true, proba, 0.5)


def evaluate_proba(name: str, y_true, proba, thr: float) -> dict:
    out = {
        "model": name,
        "pr_auc": float(average_precision_score(y_true, proba)),
        "roc_auc": float(roc_auc_score(y_true, proba)),
        **metrics_at_threshold(y_true, proba, thr),
    }
    return out


def ensure_processed() -> Path:
    path = PROCESSED_DIR / "admission_hpp.csv"
    if not path.exists():
        print("Jeu processed absent → lancement de prepare_data…")
        prepare_main()
    return path


def export_demo(df: pd.DataFrame, n: int = 10) -> None:
    DEMO_CSV.parent.mkdir(parents=True, exist_ok=True)
    pos = df[df[TARGET] == 1]
    neg = df[df[TARGET] == 0]
    n_pos = min(4, len(pos))
    n_neg = min(n - n_pos, len(neg))
    sample = pd.concat(
        [
            pos.sample(n_pos, random_state=RANDOM_STATE) if n_pos else pos,
            neg.sample(n_neg, random_state=RANDOM_STATE) if n_neg else neg,
        ]
    ).sample(frac=1, random_state=RANDOM_STATE)
    sample[FEATURES].to_csv(DEMO_CSV, index=False)
    print(f"Démo CSV : {DEMO_CSV} ({len(sample)} lignes)")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-rf", action="store_true", help="Ne pas entraîner la RF challenger")
    parser.add_argument("--min-recall", type=float, default=0.65)
    parser.add_argument("--max-alert-rate", type=float, default=0.35)
    args = parser.parse_args()

    data_path = ensure_processed()
    df = pd.read_csv(data_path)
    X = df[FEATURES]
    y = df[TARGET]

    X_trainval, X_test, y_trainval, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, stratify=y, random_state=RANDOM_STATE
    )
    X_train, X_val, y_train, y_val = train_test_split(
        X_trainval,
        y_trainval,
        test_size=VAL_SIZE,
        stratify=y_trainval,
        random_state=RANDOM_STATE,
    )

    print(
        f"Split — train {len(X_train)} | val {len(X_val)} | test {len(X_test)} "
        f"| taux+ train={y_train.mean():.3%} val={y_val.mean():.3%} test={y_test.mean():.3%}"
    )

    results = []

    # --- Baseline ---
    dummy = Pipeline(
        [
            ("pre", make_preprocessor()),
            ("clf", DummyClassifier(strategy="prior", random_state=RANDOM_STATE)),
        ]
    )
    dummy.fit(X_train, y_train)
    # Dummy prior → proba constante = taux positifs ; seuil 0.5 → tout négatif
    proba_dummy = dummy.predict_proba(X_test)[:, 1]
    results.append(evaluate_proba("dummy_prior", y_test, proba_dummy, 0.5))

    # --- LogReg (modèle principal) ---
    logreg = Pipeline(
        [
            ("pre", make_preprocessor()),
            (
                "clf",
                LogisticRegression(
                    max_iter=2000,
                    class_weight="balanced",
                    random_state=RANDOM_STATE,
                ),
            ),
        ]
    )
    logreg.fit(X_train, y_train)
    proba_val = logreg.predict_proba(X_val)[:, 1]
    thr, thr_row = choose_threshold_for_recall(
        y_val, proba_val, min_recall=args.min_recall, max_alert_rate=args.max_alert_rate
    )
    print(f"Seuil calibré sur VAL : {thr:.4f} → {thr_row}")

    proba_test = logreg.predict_proba(X_test)[:, 1]
    logreg_test = evaluate_proba("logreg_balanced", y_test, proba_test, thr)
    results.append(logreg_test)
    print("\n=== LogReg @ seuil métier (TEST) ===")
    print(classification_report(y_test, (proba_test >= thr).astype(int), digits=3))

    # --- RF challenger (optionnel) ---
    if not args.skip_rf:
        rf = Pipeline(
            [
                ("pre", make_preprocessor()),
                (
                    "clf",
                    RandomForestClassifier(
                        n_estimators=200,
                        max_depth=8,
                        min_samples_leaf=5,
                        class_weight="balanced_subsample",
                        random_state=RANDOM_STATE,
                        n_jobs=-1,
                    ),
                ),
            ]
        )
        rf.fit(X_train, y_train)
        rf_thr, _ = choose_threshold_for_recall(
            y_val,
            rf.predict_proba(X_val)[:, 1],
            min_recall=args.min_recall,
            max_alert_rate=args.max_alert_rate,
        )
        results.append(
            evaluate_proba("rf_balanced", y_test, rf.predict_proba(X_test)[:, 1], rf_thr)
        )

    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

    # Refit final sur train+val avec le même pipeline (seuil figé)
    final = Pipeline(
        [
            ("pre", make_preprocessor()),
            (
                "clf",
                LogisticRegression(
                    max_iter=2000,
                    class_weight="balanced",
                    random_state=RANDOM_STATE,
                ),
            ),
        ]
    )
    final.fit(X_trainval, y_trainval)

    model_path = ARTIFACTS_DIR / "model_logreg.joblib"
    order_path = ARTIFACTS_DIR / "feature_order.joblib"
    meta_path = ARTIFACTS_DIR / "meta.json"

    joblib.dump(final, model_path)
    joblib.dump(FEATURES, order_path)

    meta = {
        "target": TARGET,
        "features": FEATURES,
        "num_features": NUM_FEATURES,
        "cat_features": CAT_FEATURES,
        "threshold": thr,
        "threshold_policy": {
            "min_recall": args.min_recall,
            "max_alert_rate": args.max_alert_rate,
            "calibrated_on": "validation",
        },
        "sklearn_version": sklearn.__version__,
        "random_state": RANDOM_STATE,
        "n_trainval": int(len(X_trainval)),
        "n_test": int(len(X_test)),
        "positive_rate_full": float(y.mean()),
        "test_metrics_logreg": logreg_test,
        "comparison": results,
        "notes": (
            "Aide au triage à l'admission. Recall prioritaire vs precision. "
            "Pas de décision médicale automatique."
        ),
    }
    meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")

    # Copie légère pour l'app Docker
    app_art = Path(__file__).resolve().parents[1] / "app" / "artifacts"
    app_art.mkdir(parents=True, exist_ok=True)
    joblib.dump(final, app_art / "model_logreg.joblib")
    joblib.dump(FEATURES, app_art / "feature_order.joblib")
    (app_art / "meta.json").write_text(meta_path.read_text(encoding="utf-8"), encoding="utf-8")

    export_demo(df)

    print("\n=== Comparaison (TEST) ===")
    print(pd.DataFrame(results).round(3).to_string(index=False))
    print(f"\nArtefacts : {model_path}")
    print(f"Meta      : {meta_path}")


if __name__ == "__main__":
    main()
