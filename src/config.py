"""Configuration centrale — HPP Lean (Bloc 6 Jedha)."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Source brute (hors repo portfolio, RGPD / poids)
DEFAULT_RAW_CSV = Path(
    "/home/burgovida21/Bureau/Jedha_Full_Stack_HPP_Prediction/00_Data/Bourgogne20132023.csv"
)

RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"
ARTIFACTS_DIR = ROOT / "artifacts"
APP_DIR = ROOT / "app"
DEMO_CSV = APP_DIR / "data" / "demo_patients.csv"

TARGET = "HPPsev"

# Features disponibles avant / à l'admission (anti-leakage temporel)
# Alignées sur le POC historique + cadrage clinique Jedha.
NUM_FEATURES = [
    "bmi",
    "terme",
    "dsm_g",
    "taille_mere",
    "age_m",
    "parite",
    "nbilan",
    "hosp_m_g",
    "nsej18",
]

CAT_FEATURES = [
    "AMP",
    "g_type",
    "diabete",
    "preecl",
    "hta_tot",
    "tabac",
    "cortico",
    "ut_cica",
    "creta",
    "hellp",
    "cholestase",
    "pma",
    "bilan",
]

FEATURES = NUM_FEATURES + CAT_FEATURES

# Colonnes servant à construire la cible (exclues des features)
TARGET_SOURCE_COLS = ["hpp_trans", "embo", "Tampo_int", "hyst", "liga"]

RANDOM_STATE = 42
TEST_SIZE = 0.2
VAL_SIZE = 0.2  # fraction du train pour calibrer le seuil
