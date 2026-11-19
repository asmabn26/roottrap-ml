import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(BASE_DIR, 'data', 'attck_extended_mapping.json'), 'r') as f:
    LABEL_TO_ATTCK = json.load(f)

def map_prediction_to_attck(label_name: str, confidence: float,
                             features: dict = None) -> dict:
    """
    Mappe une prédiction ML vers ATT&CK complet.
    Retourne le format event_contract.json pour P4.
    """
    info = LABEL_TO_ATTCK.get(label_name, {
        'att_ck_technique_id':   None,
        'att_ck_technique_name': None,
        'att_ck_tactic':         None,
        'subtechniques':         [],
        'criticality_score':     0,
        'color':                 '#888888'
    })

    # Choisir la sous-technique la plus probable selon les features
    best_subtechnique = _select_subtechnique(label_name, info['subtechniques'], features)

    return {
        'predicted_label':         label_name,
        'confidence_score':        round(confidence, 4),
        'att_ck_technique_id':     info['att_ck_technique_id'],
        'att_ck_technique_name':   info['att_ck_technique_name'],
        'att_ck_tactic':           info['att_ck_tactic'],
        'subtechnique_id':         best_subtechnique.get('id') if best_subtechnique else None,
        'subtechnique_name':       best_subtechnique.get('name') if best_subtechnique else None,
        'all_subtechniques':       info['subtechniques'],
        'criticality_score':       info['criticality_score'],
        'color':                   info['color'],
        'alert_level':             _get_alert_level(info['criticality_score'])
    }

def _select_subtechnique(label: str, subtechniques: list, features: dict) -> dict:
    """Logique simple pour choisir la sous-technique selon les features."""
    if not subtechniques:
        return None
    if features is None:
        return subtechniques[0]

    # Brute Force : choisir selon le nombre de tentatives
    if label == 'BRUTE_FORCE':
        failed = features.get('num_failed_logins', 0)
        if failed > 100:  return subtechniques[2]  # Password Spraying
        if failed > 50:   return subtechniques[0]  # Password Guessing
        return subtechniques[3]                     # Credential Stuffing

    # DoS : choisir selon les bytes
    if label == 'DoS':
        bytes_val = features.get('src_bytes', 0)
        if bytes_val > 10000: return subtechniques[1]  # Service Exhaustion
        return subtechniques[0]                         # OS Exhaustion

    return subtechniques[0]

def _get_alert_level(score: int) -> str:
    if score == 0:  return 'INFO'
    if score <= 4:  return 'LOW'
    if score <= 6:  return 'MEDIUM'
    if score <= 8:  return 'HIGH'
    return 'CRITICAL'

if __name__ == '__main__':
    # Test avec features
    result = map_prediction_to_attck(
        'BRUTE_FORCE', 0.94,
        features={'num_failed_logins': 75}
    )
    print(json.dumps(result, indent=2))
