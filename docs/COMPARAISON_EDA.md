# EDA archivée vs EDA Lean — que reprendre ?

Sources archivées (Drive, le GitHub n’existe plus) :

- `EDA_maternite_2013-2023.ipynb` (exploration + théorie)
- `EDA_clean_2013_2023.ipynb` (nettoyage + colinéarité + amorces de modèle)
- Dictionnaire `dico_var.csv` + slides DemoDay avril 2025

Lean actuel : `notebooks/01_eda_court.ipynb` (taux de cible, NA, rappel anti-leakage).

---

## Verdict

**Ne pas importer l’EDA archivée telle quelle.** C’est un laboratoire Colab (45 cellules, SMOTE, GridSearch, tests χ² en batterie). Le Lean resterait Lean.

**Reprendre seulement 3 choses**, déjà ajoutées dans le notebook Lean :

1. Lien **feature → HPPsev** (taux par facteur de risque, numériques par classe)
2. **Redondances** AMP / PMA (et le souvenir bmi vs poids, cortico vs dose)
3. **Dictionnaire** des 22 variables utilisées (`data/dico_features_lean.csv`)

Le reste est soit déjà dans `src/prepare_data.py` / `train.py`, soit un piège à l’oral.

---

## Ce que l’archive faisait (et le Lean non)

| Analyse | Archive | Lean avant | Reprendre ? |
|---------|---------|------------|-------------|
| Dictionnaire + discussion statisticien | Oui (Massi) | Non | **Oui** (dico filtré, pas l’e-mail brut) |
| Cible / déséquilibre | `hpp_trans` ~1 % | `HPPsev` 0,82 % | Déjà là ; **cible Lean plus large** (gestes invasifs) |
| NA | Comptage + drop de 1–2 lignes | Barres NA | Suffisant ; **imputer dans le pipeline**, ne pas dropper |
| Univarié numériques | Histogrammes | Non | **Oui, léger** (describe + boxplots vs cible) |
| Bivarié vs cible | χ² / Cramer / point-bisériale | Non | **Oui, taux d’HPP par FdR clinique** (plus parlant qu’un χ²) |
| Colinéarité | Pearson, Kendall, χ² toutes paires | Non | **Oui, 1 tableau AMP×PMA** ; pas la matrice 30×30 |
| Types binaires / ordinal / nominal | Tableau `desc` | Implicitement num/cat | Pas obligatoire (déjà dans `config.py`) |
| SMOTE + GridSearch RF dans l’EDA | Oui (fin de `EDA_clean`) | Non | **Non** — ça n’est plus de l’EDA |
| Markdown « quelle méthode de corrélation » | Long | Non | **Non** — à l’oral tu cites Kendall/χ², tu ne colles pas le cours |

---

## Ce que le Lean a **en plus** (à dire au jury)

L’archive listait ~34 colonnes « avant accouchement ». Le Lean en a **22**, mais ce n’est pas un simple dépouillement.

**Ajouts Lean, plus crédibles à l’admission :** `terme`, `g_type`, `creta`, `dsm_g`, `hosp_m_g`, `nsej18`, `nbilan`, `bilan`.

**Drops justifiés par l’archive elle-même :**

- `poids_mere` (colinéaire à `bmi`)
- `Dosecortico` (NA + colinéaire à `cortico` ; le statisticien validait 12 mg par défaut — trop bricolé)
- `Aide_procreation` (doublon AMP)
- `hta_gest` (absorbé par `hta_tot`)
- `eclamps`, `gene` (quasi constantes, peu d’info)

**Drops Lean plus stricts (anti-leakage) — l’archive les avait encore :**

- `hdd` = hémorragie de la délivrance → **c’est l’événement**, pas un prédicteur d’admission
- `gene` = anesthésie générale → pendant l’accouchement
- `dbp` / `hiv` dans le dictionnaire = **pathologies néonatales** (dysplasie, HIV cérébrale), pas le VIH maternel

Ne pas « récupérer » ces variables.

---

## Nettoyage : archive vs Lean

| Règle | Archive | Lean | Garder Lean ? |
|-------|---------|------|----------------|
| AMP vide | `fillna("Aucune")` | idem | Oui |
| NA `age_m` / `dbp` | dropna (1 ligne / 60k) | imputation médiane **dans** le pipeline | **Oui Lean** (reproductible, pas de fuite) |
| `dsm_g` aberrant | — | clip &lt;0 ou ≥270 → NA | Oui Lean |
| Cible | `hpp_trans` seul | union transfusion **ou** gestes | **Oui Lean** (sévérité opérationnelle) |

Le slide DemoDay disait : *« suppression des manquants en amont, pas d’imputation dans le preprocess »*. Le Lean a **inversé** ce choix, et c’est le bon réflexe sklearn (fit train only). À l’oral : *« j’ai abandonné le dropna global ; l’imputation est dans le Pipeline. »*

---

## À ne surtout pas reporter

- Notebooks Colab + `drive.mount`
- Batterie SMOTE / SMOTEENN (le Lean assume `class_weight` + seuil)
- Tests statistiques sur toutes les paires (oral illisible, p-values sur n=65k toutes « significatives »)
- Feature `hdd`, `gene`, `dbp`, `hiv` « avant accouchement »
- Grilles RF dans l’EDA

---

## Phrase d’oral (30 s)

> « L’EDA complète a servi à cadrer le leakage avec le statisticien et à jeter les doublons (poids/IMC, dose/cortico, HTA). Le notebook Lean ne garde que ce dont j’ai besoin pour raconter le déséquilibre, les NA, et le taux d’HPP selon les FdR d’admission. Le modèle, lui, est dans `train.py`. »
