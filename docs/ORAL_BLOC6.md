# Préparation orale — Bloc 6 Jedha (HPP Lean)

Ce document sert à **t’approprier** le projet pour la soutenance. Ce n’est pas un second README : c’est un script, des chiffres à mémoriser, et des réponses aux questions du jury.

Durée typique Bloc 6 CDSD (RNCP 35288) : **10 minutes de présentation + 5 à 10 minutes de questions**.

---

## 1. Verdict : ce projet suffit-il ?

### Pour le Bloc 6 (projet final / DemoDay)

**Oui, il est suffisant si tu le défends comme un POC de direction de projet, pas comme un zoo de modèles.**

Le référentiel CDSD évalue le Bloc 6 sur la **conduite de projet data de A à Z**, pas sur la présence de XGBoost, Spark ou d’un GAN. Le jury regarde surtout :

| Compétence RNCP | Ce projet | Ton oral doit… |
|-----------------|-----------|----------------|
| C6.1 Traduire un enjeu métier en problème data | Très fort | Dire *pourquoi* recall, *pourquoi* admission, *pourquoi* pas l’accuracy |
| C6.2 Choisir la techno adaptée (veille) | Fort si assumé | Justifier le *lean* (LogReg + Docker) vs la version complète archivée |
| C6.3 Cahier des charges, planning, budget | Absent du code | Le **verbaliser** (voir §5) |
| C6.4 KPI + suivi + RGPD | Fort sur KPI/RGPD | Citer les 4 chiffres et la confidentialité PMSI |
| C6.5 Vulgariser pour le métier | À toi | Zéro jargon non expliqué |
| C6.6 Mener le projet bout en bout | POC réel | Montrer Streamlit / Docker, puis les limites |

### Pour la certification Full Stack complète (6 blocs CDSD)

**Non : ce dépôt ne remplace pas les 6 blocs.**

La certification CDSD s’obtient par **capitalisation des 6 blocs**. Les blocs 1 à 5 sont évalués par des **études de cas du bootcamp** (Spark / ETL, EDA, ML supervisé + déséquilibre, non-supervisé, deep learning, API / MLflow / déploiement). Ce repo est **l’artefact du Bloc 6**.

Ce projet **ne couvre pas** à lui seul :

- Big Data / Spark / Data Lake
- scraping / multi-sources
- ML non supervisé
- deep learning / texte / image
- API (FastAPI / SageMaker) et tracking MLflow

Si on te le reproche : *« Ces compétences ont été évaluées dans les cas pratiques des blocs 1 à 5. Ici je montre que je sais **cadrer, simplifier et livrer** un POC métier. »*

Audit Drive + GitHub public : [`ORAL_MINI_PROJETS.md`](ORAL_MINI_PROJETS.md). Fiche 1 page hors HPP : [`FICHE_ORALE_PARCOURS.md`](FICHE_ORALE_PARCOURS.md). Kayak Drive = **partiel**. Getaround **pas dans le public** — probablement dans le repo privé `CDSD_Certification_Projets` (branche `certification`), non lu ici. Ne pas nier ce que ce dépôt contient.

### Piège de la version « Lean »

La version complète (XGBoost, MLflow, etc.) existe en archive. Le Lean n’est pas un recul : c’est le message Jedha (Conversion / module 05) : **un modèle simple bien seuillé > un boosting mal cadré**. Assume-le dès la première minute, sinon le jury croira que tu as « enlevé des trucs par manque de temps ».

---

## 2. L’histoire du projet (à raconter, pas à lire)

Phrase d’accroche (15 s) :

> « L’hémorragie du post-partum sévère est rare — moins de 1 % des accouchements — mais c’est une urgence vitale. Je construis un score de **triage à l’admission**, avant l’accouchement, pour aider une maternité à anticiper (surveillance, sang, astreinte), **pas** pour décider à la place du clinicien. »

Problème → contrainte data → métrique → modèle → seuil → POC → limites.

---

## 3. Script 10 minutes (à répéter à voix haute)

Chronomètre obligatoire. Si tu dépasses 10 min, coupe la partie « stack », pas la partie « métier / limites ».

### 0:00–1:00 — Contexte et enjeu

- HPP sévère = transfusion **ou** geste invasif (embolisation, tamponnement, hystérectomie, ligature).
- Données : PMSI / réseau périnatal **Bourgogne 2013–2023**, **65 535** accouchements, **535** cas (≈ **0,82 %**).
- Moment de prédiction : **admission uniquement**. Tout ce qui se passe pendant ou après l’accouchement est du **leakage** : on tricherait.

### 1:00–2:30 — Traduction métier → data (C6.1)

- Cible `HPPsev` : union de `hpp_trans`, `embo`, `Tampo_int`, `hyst`, `liga`.
- 22 variables d’admission : 9 numériques, 13 catégorielles (IMC, terme, parité, cicatrice utérine, accreta, HELLP, etc.).
- **Ce que je n’utilise pas** : mode d’accouchement, poids du bébé, scores néonataux, actes d’hémostase — ce sont des conséquences, pas des causes disponibles à l’entrée.
- Cadre : aide au triage, données anonymisées, **pas un dispositif médical**.

### 2:30–4:00 — Pourquoi ces métriques

- Accuracy ≈ 99 % en prédisant tout le monde négatif → **hors sujet**.
- Faux négatif = on rate une HPP sévère → coût clinique élevé → **recall prioritaire**.
- Faux positif = alerte inutile → charge de travail → on plafonne le **taux d’alerte à 35 %**.
- Cible de cadrage : recall ≥ 65 % **et** alertes ≤ 35 %, seuil calibré sur la **validation**.
- On suit aussi le **PR-AUC** (aire sous la courbe précision-rappel), plus honnête que le ROC-AUC en déséquilibre : le hasard vaut la prévalence (0,008), pas 0,5.

### 4:00–6:00 — Modèle et résultats (les 4 chiffres)

Pipeline sklearn : médiane / most-frequent → StandardScaler + OneHot → classifieur. **Fit sur le train seulement** (anti-leakage technique).

| Modèle | Recall | Precision | PR-AUC | Alertes |
|--------|--------|-----------|--------|---------|
| Dummy (prior) | 0 % | — | 0,008 | 0 % |
| **LogReg balanced (retenu)** | **57 %** | **1,4 %** | **0,093** | **32 %** |
| RF challenger | 65 % | 1,5 % | 0,035 | 34 % |

À dire **sans notes** :

- Test : **13 107** dossiers, **107** HPP sévères.
- LogReg au seuil τ ≈ **0,45** : **61** vrais positifs, **46** ratés, **4 165** fausses alertes.
- On bat clairement le Dummy (PR-AUC ×11).
- La RF a un meilleur recall mais un **pire PR-AUC** : elle classe moins bien les rares positifs. On garde la LogReg : ranking + interprétabilité.
- **Honnêteté** : l’objectif 65 % de recall n’est **pas tenu sur le test** (57 %). Le seuil a été choisi sur la val ; le test a reculé. Je le dis avant qu’on me le demande.

Phrase métier sur la précision :

> « 1,4 % de précision, ça veut dire environ **1 vraie HPP pour 70 alertes**. Sur 2 000 accouchements par an, 32 % d’alertes ≈ 640 femmes. On en capterait ~9 des ~16 HPP sévères. Donc l’alerte ne peut être qu’une **action peu coûteuse** : check-list, confirmation de groupe, info de l’équipe — pas mobiliser le bloc et la banque de sang pour un tiers des admissions. »

### 6:00–7:30 — Stack volontairement lean

- Baseline Dummy + **une** LogReg `class_weight="balanced"` + RF optionnelle.
- Pas de SMOTE : en clinique, je ne fabrique pas de patientes synthétiques ; le déséquilibre se traite par le poids de classe et le **seuil**.
- Pas de MLflow / FastAPI / XGBoost dans cette variante : délai, lisibilité, démontrabilité.
- Livrable : `joblib` + **Streamlit** + **Docker Compose** → démo reproductible.

### 7:30–9:00 — Démo (si écran autorisé)

1. `docker compose up` ou Streamlit déjà lancé.
2. « Charger le dataset de démo » → « Prédire ».
3. Montrer le seuil, le recall, le taux d’alerte en en-tête.
4. Une ligne à forte proba vs une ligne basse.

Si la démo plante : enchaîne sur les limites, **ne t’excuse pas 30 secondes**.

### 9:00–10:00 — Limites et suite (le jury note ça)

1. Signal d’admission **faible** : beaucoup d’HPP sévères n’ont pas de facteur de risque visible à l’entrée (atonie imprévisible).
2. Pas de validation **prospective** ni multi-centres.
3. Split **aléatoire stratifié**, pas temporel (2013–2023) : un split par année serait plus réaliste pour le drift.
4. Pas de monitoring en production (volume d’alertes, data drift).
5. Suite : co-construire le seuil avec les sages-femmes ; action d’alerte **graduée** ; journal des prédictions ; éventuellement variables du travail (mais ce n’est plus « dès l’admission »).

Phrase de clôture :

> « Le livrable n’est pas un modèle magique. C’est un **curseur de charge de travail** calibré avec le métier, dans un cadre RGPD, déployable en POC. »

---

## 4. Chiffres à connaître par cœur

| Élément | Valeur |
|---------|--------|
| Accouchements | 65 535 |
| HPP sévères | 535 (0,82 %) |
| Features | 22 (9 num + 13 cat) |
| Train+val / test | 52 428 / 13 107 |
| Positifs test | 107 |
| Seuil τ | ≈ 0,45 (calibré val) |
| Politique seuil | recall ≥ 65 % et alertes ≤ 35 % |
| LogReg recall / prec / alertes | 57 % / 1,4 % / 32 % |
| LogReg PR-AUC / ROC-AUC | 0,093 / 0,68 |
| Matrice test LogReg | TP 61, FP 4165, FN 46, TN 8835 |
| Dummy PR-AUC | 0,008 (= prévalence) |
| sklearn | 1.6.1, `random_state=42` |

Règle : **ne jamais citer un chiffre que tu ne peux pas expliquer**.

---

## 5. Cahier des charges à verbaliser (C6.3 — rien n’est dans le code)

Le jury peut demander planning / budget / CDC. Réponds comme un chef de projet, pas comme un notebook.

**Objectif.** Score de triage à l’admission pour HPP sévère, utilisable par une équipe de garde.

**Hors scope.** Décision automatique ; features per-partum ; remplacement du protocole HPP CNGOF ; déploiement multi-établissements.

**Contraintes.** Recall prioritaire ; volume d’alertes plafonné ; modèle interprétable ; reproductibilité (seed, pipeline, Docker) ; aucune donnée identifiant dans le Git.

**Budget.** Projet pédagogique : 0 € cloud. Coût réel d’industrialisation à citer : temps clinicien pour valider le seuil, hébergement, DPI (dossier patient), assurance / qualification logiciel.

**Planning type (à dire en 20 s).** Semaine 1 cadrage + définition cible ; semaine 2 EDA + anti-leakage ; semaine 3 modèle + seuil ; semaine 4 app + Docker + limites.

**KPI de suivi projet.** Recall test, taux d’alerte, PR-AUC vs Dummy, et *plus tard* : taux d’alertes hebdomadaire, drift des features (IMC, âge).

---

## 6. Glossaire des variables (à savoir expliquer)

Tu n’as pas besoin de réciter les 22. Sache **ce que c’est** et **pourquoi ça peut compter** (facteurs de risque HPP connus : obésité, âge, multiparité, utérus cicatriciel, accreta, pré-éclampsie / HELLP, grossesse multiple, PMA).

### Numériques

| Colonne | Sens probable | Pourquoi à l’oral |
|---------|---------------|-------------------|
| `bmi` | IMC | Obésité = FdR classique d’HPP |
| `terme` | Terme (SA) | Prématurité / post-terme, contexte obstétrical |
| `dsm_g` | Durée de séjour pendant la grossesse | Proxy de grossesse pathologique ; **clip** si &lt; 0 ou ≥ 270 j (aberrant) |
| `taille_mere` | Taille (cm) | Anthropométrie ; liée à l’IMC |
| `age_m` | Âge maternel | Âge &gt; 35 ans = FdR |
| `parite` | Parité (accouchements antérieurs) | Grande multiparité → atonie |
| `nbilan` | Nb de bilans | Proxy de suivi / pathologie |
| `hosp_m_g` | Hospitalisations pendant la grossesse | Grossesse à risque |
| `nsej18` | Nb de séjours (fenêtre type 18 mois) | Consommation de soins antérieure |

### Catégorielles

| Colonne | Sens probable | Pourquoi à l’oral |
|---------|---------------|-------------------|
| `AMP` / `pma` | Aide médicale à la procréation | Grossesses souvent plus surveillées ; possible **redondance** AMP/PMA à assumer |
| `g_type` | Type de grossesse (1 = unique, 2 = multiple…) | Gémellité = surdistension utérine = FdR |
| `diabete` | Diabète | Contexte métabolique / macrosomie (indirect) |
| `preecl` | Pré-éclampsie | FdR HPP / coagulopathie |
| `hta_tot` | HTA | Terrain vasculaire |
| `tabac` | Tabac | Terrain ; lien plus faible / discuté |
| `cortico` | Corticoïdes | Souvent prématurité menaçante |
| `ut_cica` | Utérus cicatriciel | ATCD césarienne / chirurgie |
| `creta` | Placenta accreta | **Très fort** FdR d’HPP catastrophique |
| `hellp` | Syndrome HELLP | Forme grave de pré-éclampsie |
| `cholestase` | Cholestase gravidique | Associée dans certaines études |
| `bilan` | Bilan réalisé (oui/non) | Proxy de parcours de soins |

**Nettoyage assumé.** `AMP` vide → `"Aucune"` (pas de PMA documentée). Ce n’est pas un oubli : c’est une règle métier.

---

## 7. Comment le code est organisé (pour une question « montre-moi »)

```text
src/config.py         → features, cible, chemins, seed
src/prepare_data.py   → brut → admission_hpp.csv + construction HPPsev
src/train.py          → Dummy + LogReg + RF, seuil, export joblib/meta
notebooks/01_eda_court.ipynb → taux, NA, rappel anti-leakage
app/app.py            → Streamlit (seuil + prédiction)
app/Dockerfile + compose → démo isolée
```

Trois anti-leakages à citer :

1. **Temporel / métier** : features d’admission seulement (`config.FEATURES`).
2. **Technique** : `Pipeline` + `ColumnTransformer` (imputer / scaler / OHE fit train).
3. **Évaluation** : seuil sur **val**, métriques sur **test une seule fois**.

Fichier `app/artifacts/meta.json` : c’est ta **source de vérité** pour les chiffres à l’oral.

---

## 8. Questions / réponses (entraîne-toi à voix haute)

### Métier et éthique

**Pourquoi pas un seuil à 0,5 ?**  
0,5 n’a aucun sens métier. Le score `class_weight="balanced"` n’est pas une probabilité bien calibrée. On choisit τ pour un **compromis recall / volume d’alertes**.

**Le modèle est-il utilisable demain en salle de naissance ?**  
Non. POC rétrospectif, une région, pas d’étude prospective, précision trop faible pour une action lourde. Cadre : recherche / pédagogie / aide au cadrage.

**RGPD ?**  
Données PMSI **anonymisées**, usage pédagogique, **pas d’identifiants dans le repo**, brut hors Git. Minimisation : seulement les variables d’admission. Pas de décision automatique sur une personne.

**Dispositif médical / AI Act ?**  
Si on automatisait une décision clinique, on basculerait vers un logiciel de DM et un cadre réglementaire lourd. Ici : **outil d’aide**, humain dans la boucle.

**Pourquoi cette définition de cible ?**  
Le volume de sang n’est pas toujours fiable dans le PMSI. Transfusion + gestes invasifs = **sévérité opérationnelle** (ce qui mobilise réellement l’équipe). Limite : on rate peut-être des HPP sévères non transfusées, et on inclut des transfusions pour une autre raison.

### Data et fuite

**Leakage, un exemple concret ?**  
Utiliser `hyst` (hystérectomie) en feature pour prédire `HPPsev` : l’hystérectomie **fait partie de la cible**. Autre exemple : score d’Apgar, poids de naissance — connus **après** la naissance.

**Pourquoi un split aléatoire et pas temporel ?**  
Choix lean : préserver la prévalence (stratify) avec une seed. Limite : on mélange 2013 et 2023. Un split 2013–2021 train / 2022–2023 test serait plus proche de la prod. Je le mets dans les perspectives.

**Valeurs manquantes ?**  
Imputation **dans** le pipeline (médiane / mode), fit train. `dsm_g` aberrant → NA puis imputé. On ne droppe pas les lignes : trop de perte, et les NA sont informatifs en soins.

**AMP et PMA, c’est la même chose ?**  
Risque de colinéarité. En Lean on les a gardées (alignement historique). En amélioration : une seule variable, ou un test de redondance.

### Modèle et métriques

**Pourquoi pas XGBoost ?**  
Je l’ai fait dans la version complète. Ici le signal d’admission est faible : un modèle plus complexe **surapprend** le bruit. Preuve locale : la RF a un PR-AUC **pire** (0,035 vs 0,093).

**Pourquoi `class_weight="balanced"` plutôt que SMOTE ?**  
SMOTE invente des accouchements. En santé c’est discutable (validité clinique, fuite potentielle). Le poids de classe + le seuil suffisent pour un POC lisible.

**Pourquoi le Dummy est à recall 0 % ?**  
Stratégie `prior` : proba constante = 0,82 % &lt; 0,5 → tout le monde négatif. C’est **exactement** la politique « on ne fait rien de plus que le protocole standard ». Le modèle doit battre ça.

**PR-AUC 0,093 c’est nul non ?**  
Absolu : faible. Relatif : **11 fois** la prévalence. Sur un événement &lt; 1 % avec peu de signal pré-partum, c’est un signal réel mais **modeste** — d’où le cadrage « triage large », pas « diagnostic ».

**Vous visiez 65 % de recall, vous avez 57 %. Échec ?**  
Écart val → test, classique. Je ne retouche pas τ après avoir vu le test (sinon je triche). Conclusion : la contrainte était trop ambitieuse **ou** le signal est insuffisant. En prod on **renégocierait** le seuil avec le métier (ex. viser 50 % de recall pour moins d’alertes).

**Comment choisir entre LogReg et RF ?**  
Critère principal annoncé : PR-AUC (qualité de ranking) + interprétabilité. La RF gagne le recall au seuil, perd le ranking. On documente les deux dans `meta.json`.

**Calibration ?**  
Non faite (pas de `CalibratedClassifierCV`). Donc on ne vend pas la proba comme un « 45 % de risque individuel ». On vend un **score + seuil d’alerte**.

**Feature importance ?**  
Non exportée dans le Lean (à connaître comme limite). En LogReg on lirait les coefficients après scaling (signe = direction du log-odds). Cliniquement on s’attend à `creta`, `g_type` multiple, `preecl` / `hellp`, `bmi`, `parite`.

**Cross-validation ?**  
Split train/val/test stratifié, une seed. Pas de CV k-fold dans le Lean (temps / simplicité). Plus robuste : CV stratifiée pour le modèle, val dédiée au seuil.

### Déploiement

**Pourquoi Streamlit et pas FastAPI + front ?**  
L’utilisateur cible de la démo est le **clinicien / le jury**, pas un SI hospitalier. Streamlit = interface en heures, pas en semaines. En industrialisation : API + DPI + auth + logs.

**Pourquoi Docker ?**  
Même Python, mêmes artefacts, même port. Reproductibilité de démo (compétence C5/C6, industrialisation légère). `compose` mappe `8501:80`.

**Où est le modèle dans Git ?**  
`app/artifacts/meta.json` et le CSV de démo sont là. Les `.joblib` peuvent être absents du clone : il faut `python -m src.train` **si** on a le CSV brut (voir `DATA_LOCATION.md`). Pour l’oral : soit tu as l’image / les artefacts en local, soit tu montres des captures et `meta.json`.

**Monitoring ?**  
Pas en place. Ce que je mettrais : taux d’alertes glissant, prévalence observée, distribution de `bmi`/`age_m`, alerte si le taux d’alertes dérive de 32 % → 50 %.

### Projet / Jedha

**Pourquoi Lean alors que des camarades ont MLflow + AWS ?**  
Le référentiel Bloc 6 demande de **choisir** la techno adaptée et de **mener** le projet. Un overengineering qui n’améliore pas le PR-AUC ni le cadrage clinique est un anti-signal. J’ai une version complète archivée ; j’ai **décidé** de simplifier.

**C’est de la data science ou du data engineering ?**  
Les deux à petite échelle : ETL d’admission (`prepare_data`), modèle, packaging. Pas de data lake. Honnête vis-à-vis du Bloc 1.

**Quel est ton rôle ?**  
Chef de projet data : cadrage clinique, définition cible, choix de métriques, arbitre modèle vs complexité, livrable démo, limites.

---

## 9. Phrases à éviter / à remplacer

| À éviter | Dire plutôt |
|----------|-------------|
| « On a un recall de 57 %, c’est bien » | « On capte 57 % des HPP sévères en alertant 32 % des admissions ; le Dummy en capte 0 % » |
| « La précision est faible donc le modèle est mauvais » | « Elle est **attendue** sous 1 % de prévalence ; le débat est le **coût de l’alerte** » |
| « L’accuracy est de 99 % » | Ne jamais ouvrir avec l’accuracy |
| « L’IA va sauver des vies » | « Aide au triage, humain dans la boucle, validation clinique manquante » |
| « J’ai pas eu le temps de faire XGBoost » | « J’ai **choisi** de ne pas le mettre : la RF déjà n’améliore pas le PR-AUC » |
| « Le seuil est 0,45 parce que le script l’a trouvé » | « Politique recall ≥ 65 % et alertes ≤ 35 % sur la val ; fallback = max recall sous 35 % d’alertes » |

---

## 10. Plan de répétition (48 h avant l’oral)

1. Lire ce fichier une fois, puis **fermer** l’écran.
2. Enregistrer le script 10 min (téléphone). Vérifier : accroche, 4 chiffres, phrase des 70 alertes, 3 limites, clôture.
3. Tirer 10 questions au hasard de la §8, répondre chrono 45 s.
4. Relancer Docker **ou** Streamlit une fois ; préparer un plan B (captures + `meta.json`).
5. Relire uniquement la **fiche 1 page** (`docs/FICHE_ORALE.md`) le matin.

Tu es prêt quand tu peux expliquer **pourquoi la RF est battue**, **pourquoi 57 % n’est pas 65 %**, et **à quelle action d’alerte le modèle a droit** — sans regarder tes notes.
