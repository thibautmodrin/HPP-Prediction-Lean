# Fiche orale 1 page — hors HPP (filet jury)

**Règle.** Les 10 min = **HPP Lean**. Cette fiche = si on sort du projet.

**Où sont les cas.** [CDSD_Certification_Projets](https://github.com/thibautmodrin/CDSD_Certification_Projets) → branche **`cursor/cdsd-certification-portfolio`** (pas de branche `certification`). `main` est incomplet : merge la PR avant le jury.

| Bloc | Projet | 1 chiffre / 1 phrase |
|------|--------|----------------------|
| 1 | Kayak | Nominatim → météo → S3 → Scrapy → RDS → carte. CCM **Le Havre ~0,93** (un run). |
| 2 | Steam + Tinder | Spark Databricks ; Tinder = dit vs fait, unité = un date. |
| 3 | Conversion / Walmart / Uber | F1 **0,777** LogReg ; Ridge R² test ~0,95 ; KMeans **k=6** + DBSCAN. |
| 4 | AT&T | Sequential **F1 0,92** ; BERT **0,18**. |
| 5 | Getaround | Ridge → FastAPI `/predict` + Streamlit threshold. **Pas de Docker.** |
| 6 | HPP Lean | Recall test **57 %**, 0,82 %. **Pas** les 69 % / ~2 % de l’archive CDSD. |

**Phrases 15 s**

- *Kayak.* « Pipeline cloud bout-en-bout ; ranking météo du jour ; scrape Booking fragile. »
- *Steam.* « JSON S3, PySpark Databricks ; peu d’outputs dans le .ipynb local. »
- *Conversion.* « F1 0,777 LogReg > boosting. `total_pages_visited` fuit pour une action *ex ante*. »
- *Uber.* « Zones NYC : KMeans k=6 vs densité DBSCAN. »
- *AT&T.* « Modèle léger bat BERT sur ce corpus — même leçon que Conversion / HPP. »
- *Getaround.* « API prix + dash délai. Industrialisation Jedha. »
- *CathQ / ERP / Vitizen.* Uniquement si on sort du cursus Fullstack (Lead / portfolio).

**Ne jamais.** Mélanger 57 % Lean et 69 % archive. Dire « Getaround n’existe pas ». Inventer un Docker Getaround. Citer Collioure *et* Le Havre comme tops simultanés sans dire « deux runs météo ».

**Sécurité.** `.env` Drive Kayak : révoquer. Le dépôt public a `.env.example` seulement.
