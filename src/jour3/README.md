## Exercices du jour 3
Aujourd'hui nous passons a la preparation de donnees & Data versionning avec DVC. Les concepts cles a maitriser : 
- Le traitement distribué et vectorisé (Polars)
- Data versionning avec DVC
- Reproductibilité des splits train/test
- Gestion des schemas evolutifs
- Sampling et stratification intelligente

L'objectif est de comprendre et implementer le traitement distribué et vectorisé avec Polars, ainsi que versionning de nos données pour un modèle de machine learning.

## Exercice 
- installer polars et pandas. Afin de construire un pipeline de preparation de donnees eet de comparer les deux
- Installer DVC pour versionner un dataset
- Modifier volontairement le schema du dataset et gerer la compatibilite avec DVC. 
- Ecrire un script qui generer un split train/test identique. 

## Architecture 
Donnees -> Pandas
|              |
Polars -> versionning (DVC)
              |
          train/test (seed)
              |
          Dataset final -> (DVC) 
                

## Mini-projet

## Notes
DVC est un outils permettant de versionner des données et de reproduire des pipelines de traitement. 
Polars est un outils permettant de traiter des données distribuées et vectorisées, le but n'est pas de remplacer pandas mais de proposer une alternative performante sur de grandes bases de donnees.


## Regles importante

## Utlisation
executer les fichiers `process_pandas.py` et `process_polars.py` pour voir les differences entre les deux approches ainsi que la vitesse de traitement.

- intiailiser dvc ```uv run dvc init```
- versionner les donnees avec DVC ```uv run dvc add <path_to_data>```
- lancer le traitement avec DVC ```uv run dvc run -n <name> <command>```

## Realisation

## Resultat