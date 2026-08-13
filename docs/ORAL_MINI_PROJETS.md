# Oral parcours — mini-projets Jedha + portfolio

Ce document prépare les **questions hors HPP**. L’oral Bloc 6 (10 min) reste [`ORAL_BLOC6.md`](ORAL_BLOC6.md). Ici : verdict de complétude, cartographie des 6 blocs CDSD, pitchs 30 s, Q/R, pièges.

Sources auditées (août 2026) : GitHub public `thibautmodrin/*` et Drive Jedha. **Aucun dépôt officiel Getaround étudiant n’a été trouvé.** Les clés API Kayak présentes dans un `.env` Drive ne sont **pas** reproduites ici : à **révoquer / régénérer**, jamais à committer.

---

## 1. Verdict en 20 secondes

| Question | Réponse |
|----------|---------|
| Le **DemoDay / oral Bloc 6** se joue-t-il sur les mini-projets ? | **Non.** Tu présentes **HPP Lean**. Les autres projets sont des **filets** si le jury sort du sujet. |
| Les repos GitHub suffisent-ils à **valider le titre CDSD** (6 blocs) ? | **Non.** Le titre se capitalise par les **études de cas Jedha** (blocs 1–5) + le **projet libre** (bloc 6). Le portfolio n’est pas le jury. |
| Peux-tu **défendre** un parcours fullstack à l’oral ? | **Oui sur 2, 3, 4, 6** (preuves Drive / GitHub). **Fragile sur 1** (Kayak incomplet). **Trou sur 5** (Getaround introuvable) — à compenser **honnêtement** par CathQ + HPP Docker, sans prétendre que Getaround est livré. |

Phrase à dire si on te demande « tu as tout validé ? » :

> « Le projet de soutenance est HPP (Bloc 6). Les blocs 1 à 5 sont les cas Jedha : Speed Dating, Conversion, AT&T sont dans mon Drive ; Kayak est partiel (météo + carte, scraping Booking et warehouse SQL non aboutis) ; Getaround n’est pas dans mon Drive. L’industrialisation que je peux **montrer** aujourd’hui, c’est Streamlit/Docker sur HPP et FastAPI/CI/drift sur CathQ. »

---

## 2. Deux certifications à ne pas mélanger

| Cursus | Titre | Ton artefact « final » |
|--------|--------|-------------------------|
| **Fullstack Data** | CDSD, RNCP **35288**, 6 blocs | **HPP Lean** (ce repo) |
| **Lead** | Architecte IA (autre RNCP) | **CathQ** se présente lui-même comme *Lead Bloc 4 / Project Overview* |

CathQ **n’est pas** le cas officiel Fullstack (Getaround). C’est un **plus** MLOps / employabilité, et un argument si le jury veut de l’industrialisation. Ne dis pas « CathQ = Bloc 5 CDSD » : dis « compétence équivalente d’industrialisation, sur un projet Lead / portfolio ».

La fiche CDSD 35288 est **inactive depuis le 10/02/2026** ; les inscrits avant cette date peuvent encore la passer. Les 6 blocs restent requis pour le titre ; un bloc seul donne un certificat de compétences (5 ans).

---

## 3. Cartographie CDSD ↔ preuves

Études de cas Jedha Fullstack usuelles : **Kayak → Speed Dating → Conversion → AT&T → Getaround → projet libre**.

| Bloc CDSD | Cas Jedha attendu | Ta preuve | Complet pour l’oral ? |
|-----------|-------------------|-----------|------------------------|
| **1** Infra / collecte / lake | **Kayak** (API, scrape, S3, RDS, cartes) | Drive : Nominatim, OpenWeather, ranking CCM, Plotly, spider Booking **embryonnaire**, notebook S3 **léger**, **pas de RDS** | **Partiel** |
| **2** EDA | **Speed Dating** | `Project_Tinder.ipynb` (~2,4 Mo, Plotly, questions métier) | **Oui** si tu sors 3 insights |
| **3** ML structuré | **Conversion** | Colab `test.ipynb` (pipeline sklearn, `converted`) + **HPP** | **Oui** (HPP est même plus fort) |
| **4** Non structuré / DL | **AT&T spam** | `at$t_perso.ipynb` (~574 ko) + bonus **Vitizen RAG** | **Oui** pour AT&T ; RAG = bonus mince |
| **5** Industrialiser / API | **Getaround** (dash + API prix, Docker) | **Stub cours seulement** ; relais : HPP Streamlit/Docker + **CathQ** FastAPI/CI | **Trou Getaround** ; relais défendable |
| **6** Conduite de projet | Projet libre | **HPP Lean** | **Oui** si tu tiens [`ORAL_BLOC6.md`](ORAL_BLOC6.md) |

Portfolio GitHub (hors cas Jedha) : [HPP-Prediction-Lean](https://github.com/thibautmodrin/HPP-Prediction-Lean), [CathQ](https://github.com/thibautmodrin/CathQ), [ERP-Stock-Prediction](https://github.com/thibautmodrin/ERP-Stock-Prediction), [Vitizen-RAG](https://github.com/thibautmodrin/Vitizen-RAG).

---

## 4. Comment utiliser ça le jour J

1. **10 min** = uniquement HPP (problème, anti-leakage, métriques, 57 % ≠ 65 %, 1 HPP / 70 alertes, Docker, limites).
2. **Q/R** : si « et les autres blocs ? » → tableau ci-dessus, 4 phrases, **pas** de démo Kayak.
3. **Ne pas** enchaîner CathQ / ERP / Vitizen sauf question explicite.
4. **Ne jamais** sur-vendre : données CathQ synthétiques, ERP sans sklearn, Vitizen 399 mots, Kayak Booking cassé, Getaround absent.

---

## 5. Cas Jedha (Drive) — pitchs et honnêteté

### 5.1 Kayak (Bloc 1) — partiel

**Pitch 30 s.** Reco de destinations FR : GPS Nominatim, météo OpenWeather, score **CCM**, carte Plotly. Top ville le jour du run : **Collioure (CCM 0,935)**, puis Aigues-Mortes / Saintes-Maries. Objectif Jedha ensuite : data lake S3 + warehouse RDS + hôtels Booking.

**Ce qui est là.** Notebooks `1_Api_GPS`, `2_Api_meteo`, `4_Map`, CSV `cities_lat_long_ccm.csv` / `City_Meteo_Rank.csv`. Notebook S3 présent mais très court.

**Ce qui manque.** Spider Booking : une URL Paris + XPath qui logge, pas un extract 35 villes. Warehouse SQL / RDS : pas trouvé. Scraping Booking.com est **fragile** (DOM change, ToS) : le dire.

**Q/R.**
- *Lake vs warehouse ?* Lake = brut (CSV S3) ; warehouse = tables SQL nettoyées, requêtables.
- *Pourquoi pas tout scraper ?* APIs d’abord (contrat stable) ; scrape en dernier recours.
- *Score CCM ?* Agrégat météo maison (chaud / sec) pour classer 35 villes — pas un modèle ML.

**Piège.** Un `.env` Drive contient des clés météo. **Les régénérer.** Ne jamais les coller dans GitHub ni les lire à l’oral.

### 5.2 Speed Dating / Tinder (Bloc 2) — suffisant

**Pitch 30 s.** EDA Columbia speed dating : ce que les gens **déclarent** vouloir vs ce qui **prévoit** un `match` / un `dec`. Visualisations Plotly. Trois questions Jedha classiques.

**3 insights à retenir** (d’après tes notebooks `Descriptive_Statistics_Tinder` / `Project_Tinder`) :
1. Attributs **déclarés** (`attr1_1` …) : les hommes sur-pondèrent souvent l’attractivité ; les femmes répartissent davantage.
2. **Écart dit / fait** : `attr1_1` (avant) vs `attr7_2` (après) et vs notes réelles `attr` selon `dec` — l’attractivité pèse plus dans la décision que dans le discours.
3. Intérêts partagés (`int_corr`) vs même race (`samerace` / `imprace`) : corrélation d’intérêts liée au match ; la race n’est pas le levier unique.

**Q/R.** *Cible ?* `match` = double yes. Unité = un **rendez-vous** (iid × partner), pas une personne — sinon on double-compte. *Biais ?* Waves, étudiants Columbia, auto-déclaration, NA.

### 5.3 Conversion (Bloc 3) — suffisant si tu tiens le leakage

**Pitch 30 s.** Prédire `converted` (newsletter) : `country`, `age`, `new_user`, `source`, et **éventuellement** `total_pages_visited`. Déséquilibre. Pipeline sklearn (impute + scale + OHE + LogReg / arbres). Leçon du module 05 : **modèle simple + bon cadrage > boosting mal cadré** — c’est exactement le fil HPP Lean.

**Piège n°1 du jury.** `total_pages_visited` est souvent du **leakage** : on le connaît **après** la session. Un modèle « magique » avec cette variable ne sert pas à **cibler** un visiteur à l’arrivée. Réponse : *« En prod je l’enlève ou je ne l’utilise qu’en analyse descriptive. Pour une action marketing ex ante, country / age / new_user / source. »*

**Q/R.** Accuracy trompeuse (peu de conversions). Baseline Dummy / toujours 0. Split user-level si plusieurs lignes.

### 5.4 AT&T spam (Bloc 4) — notebook perso présent

**Pitch 30 s.** Classif texte ham/spam (SMS). Preprocessing NLP → embedding / réseau (Keras) plutôt que règles métier. Métrique : **recall spam** (laisser passer un spam est coûteux) + ne pas tout classer spam.

**Preuve.** `at$t_perso.ipynb` travaillé ; le `01-AT&T_spam_detector.ipynb` du cours est un stub.

**Q/R.** Train/test **avant** vectorizer (fit vocabulaire sur le train seulement). Déséquilibre ham/spam. *Transformers ?* Possible ; pour un SMS court un modèle simple suffit au cas Jedha.

**Bonus.** Vitizen RAG (ci-dessous) montre du **non-structuré génératif**, ce n’est pas le livrable AT&T.

### 5.5 Getaround (Bloc 5) — **trou**

**Constat.** Sur Drive : uniquement le stub cours `01-Getaround_analysis (1).ipynb` (~9 ko). Pas d’API pricing, pas de dashboard délai entre locations, pas de Docker Getaround.

**Ce que Jedha attend en général.** Analyse du delay entre locations **et** API documentée de prédiction de prix, packagée (Docker / cloud).

**Quoi dire.** *« Je n’ai pas abouti Getaround. L’industrialisation que je montre : HPP (Streamlit + Compose) et CathQ (FastAPI, MLflow, PSI, CI pytest). »* Ne pas inventer un déploiement Render/Heroku.

Si Jedha a **déjà validé** le bloc 5 sur Julie pendant le bootcamp, ce trou Drive n’empêche pas l’oral Bloc 6. Si le bloc 5 n’a **jamais** été rendu, c’est un **risque titre**, pas un risque DemoDay 10 min — à clarifier avec l’équipe pédagogique **avant** le jury, pas pendant.

---

## 6. Portfolio GitHub — pitchs (si on sort de HPP)

### 6.1 HPP Lean — Bloc 6 (projet du jour)

Voir [`FICHE_ORALE.md`](FICHE_ORALE.md). Une ligne : *curseur de charge, pas un DM ; Dummy battu ; 57 % ≠ 65 % ; 1 vraie HPP / 70 alertes.*

### 6.2 CathQ — MLOps junior (Lead / portfolio)

**Pitch 30 s.** Rebut (`is_scrap`) sur extrusion de cathéters. **Données 100 % synthétiques.** Décision `PASS` / `HOLD_REVIEW` (humain). XGBoost vs RF, seuil **coût** FN×50 / FP×1 → τ = **0,05**. Test : recall **30 %**, précision **5,2 %** (TP 24, FP 435, FN 55). FastAPI + Docker + MLflow + PSI + CI (9 tests pytest). **Pas un dispositif médical.**

**Chiffres à ne pas confondre.** Dans `train_metrics.json`, precision/recall à **0** : c’est le seuil sklearn **0,5** par défaut, inutilisable. Les vrais chiffres métier sont ceux d’**eval coût** (τ = 0,05).

**Q/R.**
- *Pourquoi synthétique ?* MES usine propriétaire ; le projet démontre la **chaîne** MLOps, pas une usine réelle.
- *Drift ?* PSI sur melt / vacuum / OD / moisture (seuil 0,2). `mean_shift_z` et `alert_on_scrap_spike` sont dans le YAML, **pas implémentés** dans `drift.py` — le dire si on creuse.
- *Airflow ?* Prévu au design ; le cœur démo = `make demo` + API. Ne pas raconter un cluster Airflow en prod.

### 6.3 ERP Stock Prediction — intégration, pas du ML sklearn

**Pitch 30 s.** Module Python FastAPI branché sur un ERP **Laravel + Postgres**. Rupture = stock / demande moyenne 30 j. Safety stock = **1,65 × σ × √7** (lead time 7 j, ~95 %). Forecast = **moyenne mobile 14 j + pente `polyfit`**. Démo Docker, ~45 jours, UI en **espagnol** (contexte mission).

**Piège.** Le README dit « ML léger » : **il n’y a pas de sklearn / XGBoost**. C’est de la **stat d’inventaire**. Assume-le : *intégration ERP + règles métier*, pas un modèle entraîné. Pas de MAPE reportée.

**Q/R.** *Pourquoi 1,65 ?* z d’une normale pour ~95 % de couverture. *Limite ?* Saisonnalité, ruptures, 45 jours de seed : trop court pour un vrai forecast.

### 6.4 Vitizen RAG — démo RAG, corpus jouet

**Pitch 30 s.** Assistant pulvérisation viticole : 4 `.txt` (**~399 mots**), embeddings + LLM **Mistral**, index **Chroma**, FastAPI `/query` + sources. Docker réindexe au start. Pas un conseil réglementaire.

**Q/R.** *Éval ?* Pas de RAGAS. *Hallucinations ?* Prompt « je ne sais pas » + sources ; corpus trop petit pour une prod. *AWS ?* Mentionné, **non livré**. Hors scope : app Vitizen, re-rank, mémoire.

---

## 7. Questions « parcours » (réponses toutes faites)

**« Montre-moi que tu es fullstack, pas seulement un notebook HPP. »**  
Collecte (Kayak APIs), EDA (Speed Dating), ML tabulaire (Conversion + HPP), NLP (AT&T), serving (HPP Docker + CathQ FastAPI), RAG (Vitizen). Getaround non livré.

**« Pourquoi tant de projets lean / synthétiques ? »**  
Même doctrine Jedha : livrer un **cadrage + un POC reproductible** plutôt qu’un zoo. HPP réel PMSI ; CathQ synthétique assumé ; Vitizen corpus pédagogique.

**« Spark / Big Data ? »**  
Pas dans le portfolio GitHub. Kayak = APIs + pandas, pas Spark. Si le bloc 1 Jedha l’exigeait via un lab Databricks, le citer **seulement si tu l’as fait** ; sinon : hors de ce que je peux montrer aujourd’hui.

**« Non-supervisé ? »**  
Pas de projet portfolio dédié (pas de clustering clients / PCA Speed Dating abouti en repo). Ne pas inventer. HPP n’est pas du non-supervisé.

**« Tu vises aussi le Lead ? »**  
CathQ est cadré Lead Bloc 4. Spotify / Stripe / Fraud = autres blocs Lead, pas dans ce GitHub.

---

## 8. Ce qui suffit vs ce qui bloque la validation

### Suffisant pour **passer l’oral Bloc 6** (DemoDay)

- HPP tenu (chiffres, limites, démo Streamlit).
- 4 phrases honnêtes sur le reste du parcours.
- Pas besoin que Kayak/Getaround/Vitizen soient « parfaits ».

### **Ne bloque pas** l’oral, mais **peut bloquer le titre** si non déjà validé sur Julie

- **Getaround absent** (bloc 5 officiel).
- **Kayak** sans S3/RDS/Booking abouti (bloc 1).

Je n’ai pas accès à Julie / aux PV de jury : **demande à Jedha** si les blocs 1–5 sont déjà capitalisés. Si oui, l’oral = Bloc 6. Si non, les mini-projets GitHub **ne ferment pas** ces trous à eux seuls.

### Suffisant pour un **portfolio emploi** (autre sujet)

- HPP + CathQ = les deux piliers.
- ERP = carte « j’intègre un SI ».
- Vitizen = carte « j’ai touché au RAG », à présenter comme **jouet**.

---

## 9. Mini-plan de révision (hors HPP)

La veille, **à voix haute**, chrono 3 min :

1. Kayak : Collioure 0,935 ; lake vs warehouse ; Booking non fini.  
2. Speed Dating : dit vs fait sur l’attractivité ; unité = date.  
3. Conversion : `total_pages_visited` = leakage.  
4. AT&T : recall spam ; vectorizer fit sur train.  
5. Getaround : pas livré ; relais CathQ/HPP.  
6. CathQ : synthétique, τ 0,05, recall 30 %, pas un DM.  
7. ERP : pas sklearn, z=1,65, LT=7.  
8. Vitizen : 399 mots, sources, pas RAGAS.

Le matin : relire [`FICHE_ORALE.md`](FICHE_ORALE.md) (HPP) + [`FICHE_ORALE_PARCOURS.md`](FICHE_ORALE_PARCOURS.md) (cette page condensée).
