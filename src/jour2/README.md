## Exercice du jour 2
Aujoud'hui nous passons dans la partie Feature Engineering & Feature Store. Les differents concepts a maitriser sont : 
 - Le dataLeakage
 - Les features Stores
 - Le versioning des données reutilisables
 - Le feature freshness / lateny
 - Transformation batch vs on-demande vs streaming features
L'Objectif est de montrer comment transformer les donnees en informations utiles pour un modèle de machine learning, puis de comment stocker et reutiliser ecs informations de facons fiable.

## Excercies
- Instaler Feast (deps) et Redis via Docker
- Analyser les données (transactions.csv) et identifier une feature à extraire 
- Implémenter la feature extraite dans Feast  
- Interroger le online store en simulant une requête en temps reel

## Architecture 
          DONNÉES NETTOYES
                │
                ▼
          Feature Engineering
                │
                ▼
          Feature Store
      ┌────────┴────────┐
      │                 │
      ▼                 ▼
Offline Store         Online Store
   Parquet              Redis
      │                 │
      │                 │
      ▼                 ▼
Entraînement ML      Inférence API

## Mini-projet
Faire une demonstraction. Construire un pipeline de features qui introduit un data leakage temporel, et mesurer l'impact sur la performance du modele. Corriger le tout avec un point-in-time join dans Feast et de montrer la chute de performance vers un score realiste  

## Notes
Une feature est simplement une variable utilisable pour l'entraînement d'un modèle ML. Une feature store est un système de gestion de features qui permet de stocker, versionner et interroger les features. Le Online Store vs Offline Store est un concept permettant de séparer les données utilisées pour l'entraînement et les analyses historiques (offline) et les données utilisées pour l'inférence (online). Le Point-in-time join est une technique permettant de joindre les données historiques avec les données en temps réel pour éviter le data leakage temporel.

## Regles importante
```Les features doivent être calculées en temps réel pour éviter le data leakage temporel.```
```Les features disponible aujourd'hui ne doivent pas etre utilisees pour predire un evenement qui s'est produit hier```
```Toujours commencer par verifier, comprendre, analyser les donnees.```

## Utlisation
Installation avec uv
```
uv add "feast>=0.38.0"
```

Utilisation de feast (se mettre dans le dossier `feature_repo` contract .yaml) 
```
uv run feast apply
```

deployer les donnees dans Redis
```uv run feast entities list et uv run feast feature-views list```

## Realisation
Grace au donnees on cree un feature ou indicateurs pour permettre a un modele de machine learning de mieux comprendre une situation. L'indicateur creer etait un les depenses d'une transaction au cours des 7 derniers jours. Mettre en place un feature store avec feast pour centraliser les features afin qu'ils puissent etre reutilises facilements par le ML ou l'application, ainsi que redis pour simuler le stockage des informations necessaire pour une prediction. Le chemin choisi est alors : Donnees nettoyees -> travail de feature -> feature store -> Utilisation par le modele de machine learning

- Creer un indicateur a partir de donnees 
- reutiliser les indicateurs avec un feature store
- preparer les features pour une utilisation reel
- eviter le data leakage
- garantir que les donnees correspondent bien a la situation
- Mettre intentionnelement le dataleakage  
- Demontraction avec measure_leakage.py

## Resultat
a travers le script ```uv run src/jour2/measure_leakage.py``` nous avons une difference. Les features avec data leakage donne un meilleur resultat mais le modele est encore faible, du au donnee manquante ou pas assez nombreux. Modifier le script en fonction ```uv run scripts/generate_datasets.py ```   
