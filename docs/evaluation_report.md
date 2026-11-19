
# Rapport d'évaluation — Sprint 2 RootTrap

## Random Forest
- Accuracy  : 0.9930
- Precision : 0.9978
- Recall    : 0.9930
- F1-score  : 0.9951

## Observations
- Dataset : CICIDS2017 (504151 échantillons test)
- Classes  : ['Bots', 'Brute Force', 'DDoS', 'DoS', 'Normal Traffic', 'Port Scanning', 'Web Attacks']
- SMOTE appliqué pour corriger le déséquilibre (83% Normal Traffic)

## Prochaines étapes Sprint 3
- Ajouter DBSCAN pour le clustering comportemental
- Intégrer les logs Cowrie de P2
- Connecter l'API Flask vers P4
