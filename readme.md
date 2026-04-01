🍷 BottleNeck – Industrial Data Pipeline (Kestra)

📌 Contexte

Ce projet a pour objectif de mettre en place un pipeline de données industriel pour l’analyse des performances commerciales d’une entreprise (BottleNeck).

Le pipeline permet de traiter automatiquement les données, de garantir leur qualité, et de produire des indicateurs fiables pour le métier.

🎯 Objectifs:

Automatiser le traitement des données
Garantir la qualité des données via des tests
Implémenter une logique Fail-Fast
Produire des indicateurs métiers (chiffre d’affaires)
Générer des exports fiables
Assurer la traçabilité et l’auditabilité du pipeline

🏗️ Architecture du Pipeline

Kestra : orchestration du pipeline
Python (Pandas, NumPy) : traitement des données
DuckDB : moteur analytique
Docker : exécution isolée des scripts
GitHub : versioning du code
Email (Google Workspace) : alertes en cas d’échec
⏱️ Orchestration
🔹 Déclenchement automatique

Le pipeline est exécuté automatiquement :

📅 Le 15 de chaque mois
🕘 À 09h
via un trigger CRON :
0 9 15 * *

🔄 Pipeline de Données

Le pipeline suit une logique industrielle structurée :

1. Ingestion
Récupération des fichiers de données
Clonage du dépôt GitHub
Gestion des erreurs avec retry (3 tentatives)
2. Chargement
Import des données dans DuckDB
3. Nettoyage
Standardisation des données
Suppression des valeurs aberrantes
4. Test qualité des données
Vérification de l’intégrité
Fail-Fast : arrêt immédiat si erreur
5. Fusion des données
Consolidation des différentes sources
6. Test de cohérence des jointures
Validation des relations entre tables
7. Calcul du chiffre d’affaires
Génération des métriques financières
8. Test de cohérence du CA
Vérification des incohérences financières
9. Analyse des vins premium
Segmentation des produits
Extraction d’insights
10. Test statistiques et export
Validation finale avant export
11. Export des résultats

Fichiers générés :

ca_par_produit.xlsx
vins_premium.csv
vins_ordinaires.csv

🧪 Stratégie de Qualité des Données

Le pipeline repose sur un principe clé :

👉 1 script de traitement → 1 script de test

Exemples :

01_load_data.py → test_quality_data.py
03_fusion_data.py → test_coherence_jointure.py
04_calcul_ca.py → test_coherence_ca.py
Avantages
détection rapide des erreurs
pipeline fiable
données auditables
logique Fail-Fast

⚠️ Gestion des erreurs & alertes

En cas d’échec :

arrêt automatique du pipeline
log d’erreur dans Kestra
envoi d’un email d’alerte contenant :
ID d’exécution
date et heure
étape en erreur

🔁 Robustesse

Retry automatique :
3 tentatives
intervalle de 30 secondes
Isolation via Docker
Pipeline reproductible

📊 Résultats & Valeur

Ce projet démontre :

mise en place d’un pipeline data industriel
orchestration avec Kestra
intégration de tests qualité à chaque étape
approche Fail-Fast
production d’indicateurs fiables
gestion des erreurs et alerting

🚀 Perspectives d’amélioration

intégration avec un Data Lake (S3)
monitoring avancé (CloudWatch / Prometheus)
dashboard BI (Power BI / Tableau)
CI/CD pipeline

👩‍💻 Auteur

Projet réalisé par Marwa El Allouchi
Data Engineer (OpenClassrooms)
