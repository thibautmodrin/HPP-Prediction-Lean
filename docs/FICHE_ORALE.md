# Fiche orale 1 page — HPP Lean (à relire le matin)

**Accroche.** HPP sévère rare (0,82 %) mais vitale. Score de **triage à l’admission**, pas une décision automatique.

**Cible.** `HPPsev` = transfusion **ou** embo / tamponnement / hystérectomie / ligature.

**Data.** Bourgogne 2013–2023, 65 535 dossiers, 535 positifs. 22 features connues **avant / à l’entrée**. Anti-leakage temporel + pipeline sklearn fit train + seuil sur val / test une fois.

**Métriques.** Accuracy hors sujet. Recall prioritaire (rater une HPP coûte cher) + plafond 35 % d’alertes + PR-AUC (hasard = 0,008).

**Résultats test (13 107 ; 107 cas).** Dummy recall 0 %. **LogReg** τ≈0,45 : recall **57 %**, prec **1,4 %**, PR-AUC **0,093**, alertes **32 %** (TP 61, FP 4165, FN 46). RF : recall 65 % mais PR-AUC 0,035 → on garde la LogReg.

**Phrase métier.** ≈ 1 vraie HPP / 70 alertes. Alerte = action **peu coûteuse** (check-list), pas bloc + sang pour 32 % des femmes. Objectif 65 % de recall **non tenu** sur le test : je le dis.

**Stack.** Dummy + LogReg `class_weight="balanced"` (+ RF). Pas de SMOTE. Streamlit + Docker. Version XGBoost/MLflow archivée volontairement écartée.

**Limites.** Signal d’admission faible ; pas de prospective ; split non temporel ; pas de monitoring ; précision incompatible avec une action lourde.

**Clôture.** Livrable = **curseur de charge de travail** cadré avec le métier, RGPD, POC déployable.

**Si question « certification / 6 blocs ».** Ce repo = **Bloc 6**. Spark, DL, API, non-supervisé = blocs 1–5 du bootcamp, pas ce POC.
