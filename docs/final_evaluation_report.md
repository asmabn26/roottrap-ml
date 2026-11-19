
# Rapport Final ML — RootTrap Sprint 3

## Métriques Globales — Random Forest
| Métrique  | Score  |
|-----------|--------|
| Accuracy  | 0.9930 |
| Precision | 0.9978 |
| Recall    | 0.9930 |
| F1-score  | 0.9951 |

## Dataset
- Source       : CICIDS2017 (cleaned)
- Lignes test  : 504151
- Features     : 52
- Classes      : ['Bots', 'Brute Force', 'DDoS', 'DoS', 'Normal Traffic', 'Port Scanning', 'Web Attacks']

## Modèles entraînés
- Random Forest : models/random_forest_model.pkl
- LSTM          : models/lstm_model.h5
- Scaler        : models/scaler.pkl

## Fichiers générés
- Mapper ATT&CK étendu  : data/attck_extended_mapping.json
- Kill Chain DAG        : data/kill_chain_dag.png
- Confusion Matrix      : data/final_confusion_matrix.png

## Prochaines étapes — Sprint 4
- Fine-tuning Grid Search
- Analyse malware patterns
- Tests adversarial attacks
- Revue code sécurité P4
