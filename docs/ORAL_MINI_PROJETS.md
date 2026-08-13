# Oral parcours — dépôt CDSD (branche portfolio)

Source relue : [CDSD_Certification_Projets](https://github.com/thibautmodrin/CDSD_Certification_Projets).

**Il n’y a pas de branche nommée `certification`.** Le livrable complet est `cursor/cdsd-certification-portfolio` (PR #1). `main` est plus maigre (pas d’API Getaround, pas des decks, pas du projet HPP). Pour l’oral, montre **cette branche** (ou merge-la dans `main` avant le jury).

Les 10 min DemoDay restent [`ORAL_BLOC6.md`](ORAL_BLOC6.md) (**HPP Lean**). Ici : les 8 mini-projets du dépôt CDSD + filet Q/R.

---

## 1. Verdict (après lecture du repo)

| Question | Réponse |
|----------|---------|
| Les cas Jedha 1–5 sont-ils **assez complets** pour un oral de parcours ? | **Oui**, si tu t’appropries les chiffres ci-dessous et que tu ne mélanges pas les deux HPP. |
| Suffisent-ils à **valider le titre** à eux seuls ? | Ils **documentent** les 6 blocs. La validation reste Jedha / jury. Mais on ne peut plus dire « Getaround n’existe pas ». |
| Les 10 min DemoDay ? | Toujours **HPP Lean**. Ne pas enchaîner Kayak → AT&T. |

Phrase si on demande le parcours :

> « Les cas des blocs 1 à 5 sont dans `CDSD_Certification_Projets` (branche portfolio) : Kayak S3/RDS, Steam Spark, Conversion F1 0,777, Uber clustering, AT&T NLP, Getaround FastAPI + Streamlit. Le projet de soutenance est HPP Lean : triage à l’admission, LogReg, recall 57 % sur le test. »

---

## 2. Cartographie (la tienne, dans le README du dépôt)

| Bloc RNCP | Projet du dépôt | Statut | À mémoriser |
|-----------|-----------------|--------|-------------|
| **1** Infra | **Kayak** | Complet pour l’oral (notebooks 1→7 + spider) | Pipeline Nominatim → OpenWeather → S3 → Scrapy → RDS → Plotly. Top CCM **Le Havre ~0,93** (un run météo, pas une vérité éternelle). |
| **2** EDA | **Steam** (deck) + **Tinder** (notebook) | Steam = Spark Databricks (outputs locaux faibles). Tinder = EDA Plotly aboutie | Steam : JSON S3 + PySpark. Tinder : dit vs fait sur l’attractivité. |
| **3** Structuré | **Conversion** + **Walmart** + **Uber** | Conversion et Uber solides. Walmart notebook réel | Conversion **F1 0,777** LogReg, seuil 0,96. Walmart Ridge **R² test ~0,95** (CV ~0,89). Uber **KMeans k=6** + DBSCAN. |
| **4** Non structuré | **AT&T** | Complet | Sequential **F1 0,92** / acc. 97,9 %. BERT val **F1 0,18** — le simple gagne. |
| **5** Industrialiser | **Getaround** | Complet pour l’oral (API + dash + data) | Ridge → `reg.pkl` → FastAPI `/predict` + Streamlit threshold. Pas de Docker. |
| **6** Projet | **HPP** (ce Lean **ou** l’archive XGB/MLflow du dépôt CDSD) | Lean = oral DemoDay | **Ne pas mélanger les chiffres** (voir §4). |

Portfolio hors Jedha (CathQ, ERP, Vitizen) : filet emploi, pas les cas officiels. CathQ ≠ Bloc 5.

---

## 3. Comment jouer l’oral

1. **DemoDay 10 min** = HPP Lean uniquement.  
2. Tes decks `Presentation_Bloc*.pptx` (~5 min / bloc) servent si le jury **déroule les 6 blocs**. Ne les enchaîne pas dans les 10 min HPP.  
3. Branche à ouvrir : `cursor/cdsd-certification-portfolio`.  
4. **Deux HPP** : Lean (recall test 57 %, 0,82 %, pas de SMOTE) vs archive CDSD/HF (SMOTE, ~2 %, recall 69 % LogReg). Tu défends **Lean**. Les slides `Presentation_Bloc6_HPP.pptx` du dépôt CDSD parlent encore de l’archive.

---

## 4. Piège n°1 : deux versions HPP

| | **Lean** (oral recommandé) | **Archive** (Projet 9 du dépôt CDSD) |
|--|----------------------------|--------------------------------------|
| Prévalence | **0,82 %** (535 / 65 535) | ~2 % dans le README Projet 9 |
| Modèle | LogReg `class_weight`, pas de SMOTE | LogReg+SMOTE, RF, XGB |
| Recall test | **57 %** (objectif 65 % non tenu) | 69 % / 65 % / 66 % |
| Démo | Streamlit Lean + Compose | HF Space + MLflow + joblib **Git LFS** (pointeur 0,1 ko sans `git lfs`) |

Si tu cites 69 % et 57 % dans la même phrase, le jury croit que tu ne maîtrises pas. Une phrase : *« J’ai volontairement simplifié : plus de SMOTE, seuil métier, POC Docker. Les notebooks XGB/MLflow restent dans le dépôt CDSD. »*

---

## 5. Pitchs 30 s + Q/R (cas du dépôt)

### Kayak — Bloc 1

**Pitch.** 35 villes FR. GPS Nominatim, météo OpenWeather, score CCM, lake S3, scrape Booking (Scrapy, cartes `data-testid=property-card`), warehouse RDS MySQL, carte Plotly. Enjeu brief : 70 % veulent plus d’infos destination.

**Chiffres du README / deck.** CCM top **Le Havre ~0,93** (un autre run Drive donnait Collioure : **le ranking change avec la météo du jour**). Spider fragile si le DOM Booking bouge. `.env` (pas de secrets dans Git).

**Q/R.** Lake = fichiers S3 ; warehouse = tables RDS. ACL `public-read` = limite, signed URLs en mieux. Pas d’Airflow : notebooks manuels.

**Reste mince.** Notebook S3 tout petit (~3 ko). Pas de `hotels.csv` commité (reproductibilité scrape).

### Steam — Bloc 2 (deck officiel)

**Pitch.** EDA Big Data : JSON Steam sur S3, **PySpark / Databricks**, schéma imbriqué, 7 questions métier (éditeurs, ratings…). Passage du pandas local au cluster.

**Limite à dire.** Le `.ipynb` local (~28 ko) a **peu d’outputs**. La preuve live = workspace Databricks (lien dans le notebook). Si le lien est mort le jour J : raconter le pipeline, pas feindre une démo.

**Tinder** (même bloc EDA, notebook 3,5 Mo) : unité = un *date* ; écart déclaré vs réel sur l’attractivité ; `match` = double yes.

### Conversion — Bloc 3

**Pitch.** Newsletter `converted`. F1 (accuracy 99 % trompeuse). **LogReg F1 0,777** > GB 0,773 > XGB 0,769. Seuil **0,96**. Prec 0,85 / recall 0,72 sur la classe 1.

**Piège.** Features incluent `total_pages_visited` (souvent **après** la session). Le dire : *utile en analyse, discutable pour cibler à l’arrivée*. C’est le fil HPP Lean (modèle simple bien seuillé).

### Walmart — Bloc 3 (régression)

Ridge + GridSearch. **R² CV ~0,89, R² test ~0,95** (Best Score ~0,936). Si le test > CV : petit jeu, split chanceux — ne pas vendre 0,95 comme « la » perf.

### Uber — Bloc 3 (non supervisé)

NYC, cartes Plotly. **KMeans k=6** (elbow) vs **DBSCAN** (densité, outliers). Pas de cible : on cherche des zones / heures de demande.

### AT&T — Bloc 4

SMS ham/spam. Embedding+Dense **acc. 97,9 %, F1 0,92**. BERT transfer **F1 val 0,18** : trop lourd / mal calé pour ce corpus. Vectorizer / tokenizer **fit sur le train**.

### Getaround — Bloc 5

**Pitch.** Deux livrables Jedha : (1) **API prix** Ridge + Pipeline sklearn, joblib, FastAPI `/predict` + `/health` + `/model/feature_order` ; (2) **dashboard** Streamlit : slider 0–120 min, part des locations coupées vs retards évités (Connect vs All). Data Jedha dans `dashboard/data/`. Notebooks d’analyse dans `others/`.

**Q/R.** *Docker ?* Non sur Getaround (HPP/CathQ oui). *Test ?* Script smoke `tests/test_api_local.py` (API déjà up), pas une suite pytest. *Modèle ?* Ridge, MAE imprimée à l’entraînement — à relancer `python app/model/train.py` pour le chiffre exact plutôt que l’inventer.

Démo orale : `uvicorn app.main:app` + `streamlit run dashboard/streamlit_app.py`.

---

## 6. Suffisant pour valider ?

**Oral Bloc 6 / DemoDay :** oui avec HPP Lean, plus ce filet.

**Parcours 6 blocs :** le dépôt portfolio **couvre** Kayak, EDA (Tinder+Steam), ML structuré (Conversion/Walmart/Uber), DL (AT&T), deploy (Getaround), projet (HPP). Trous honnêtes, pas rédhibitoires à l’oral :

- Steam peu reproductible hors Databricks  
- Kayak scrape non figé dans Git  
- Getaround sans Docker / CI  
- Conversion : leakage pages vues  
- HPP Projet 9 : joblib en **Git LFS** ; chiffres ≠ Lean  
- `oral/node_modules` versionné (bruit, pas un sujet jury)

Merge la PR portfolio dans `main` avant d’envoyer le lien au jury.

---

## 7. Révision 3 min (hors HPP Lean)

1. Kayak : S3 + RDS ; CCM **du jour** ; Booking fragile.  
2. Steam : Spark Databricks ; Tinder : dit vs fait.  
3. Conversion : F1 **0,777** LogReg ; pages vues = leakage.  
4. Walmart : Ridge, R² test élevé, petit dataset.  
5. Uber : k=6 vs DBSCAN.  
6. AT&T : F1 0,92 > BERT 0,18.  
7. Getaround : Ridge API + threshold Streamlit.  
8. HPP : **Lean 57 % / 0,82 %**, pas les 69 % de l’archive.
