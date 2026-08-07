# Emplacement des données brutes

Les CSV volumineux / sensibles ne sont **pas** versionnés ici.

## Source recommandée

| Fichier | Chemin local typique |
|---------|----------------------|
| `Bourgogne20132023.csv` | `/home/burgovida21/Bureau/Jedha_Full_Stack_HPP_Prediction/00_Data/Bourgogne20132023.csv` |
| Repo source | https://github.com/thibautmodrin/Jedha_Full_Stack_HPP_Prediction |

## Générer le jeu processed

```bash
cd "Projet 9b - HPP Prediction Lean"
python -m src.prepare_data
# ou
python -m src.prepare_data --raw /chemin/vers/Bourgogne20132023.csv
```

Sortie : `data/processed/admission_hpp.csv` (features admission + cible `HPPsev`).
