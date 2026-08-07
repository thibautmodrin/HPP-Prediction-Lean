"""
Prépare le jeu admission → HPPsev.

Usage:
  python -m src.prepare_data
  python -m src.prepare_data --raw /chemin/Bourgogne20132023.csv
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from src.config import (
    DEFAULT_RAW_CSV,
    FEATURES,
    PROCESSED_DIR,
    TARGET,
    TARGET_SOURCE_COLS,
)


def build_target(df: pd.DataFrame) -> pd.Series:
    """HPP sévère = transfusion ± actes invasifs (définition RPB / README source)."""
    parts = []
    for col in TARGET_SOURCE_COLS:
        if col not in df.columns:
            continue
        parts.append(df[col].fillna(0).astype(float) == 1)
    if not parts:
        raise ValueError(f"Aucune colonne cible trouvée parmi {TARGET_SOURCE_COLS}")
    y = parts[0]
    for p in parts[1:]:
        y = y | p
    return y.astype(int)


def prepare(raw_path: Path) -> pd.DataFrame:
    if not raw_path.exists():
        raise FileNotFoundError(
            f"CSV brut introuvable : {raw_path}\n"
            "Indiquez le chemin avec --raw (voir DATA_LOCATION.md)."
        )

    df = pd.read_csv(raw_path, low_memory=False)
    missing = [c for c in FEATURES if c not in df.columns]
    if missing:
        raise ValueError(f"Colonnes manquantes dans le brut : {missing}")

    out = df[FEATURES].copy()
    out[TARGET] = build_target(df)

    # AMP quasi vide → « Aucune » (pas de PMA documentée)
    if "AMP" in out.columns:
        out["AMP"] = out["AMP"].fillna("Aucune").astype(str)

    # dsm_g aberrant (durée séjour grossesse) : clip métier soft
    if "dsm_g" in out.columns:
        out.loc[(out["dsm_g"] < 0) | (out["dsm_g"] >= 270), "dsm_g"] = pd.NA

    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Prépare data/processed/admission_hpp.csv")
    parser.add_argument("--raw", type=Path, default=DEFAULT_RAW_CSV)
    args = parser.parse_args()

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    df = prepare(args.raw)
    out_path = PROCESSED_DIR / "admission_hpp.csv"
    df.to_csv(out_path, index=False)

    n = len(df)
    pos = int(df[TARGET].sum())
    print(f"Écrit : {out_path}")
    print(f"Lignes : {n:,} | positifs {TARGET} : {pos:,} ({100 * pos / n:.2f} %)")
    print(f"NA moyen features : {df[FEATURES].isna().mean().mean():.1%}")


if __name__ == "__main__":
    main()
