import json, os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(BASE_DIR, 'data', 'attck_extended_mapping.json')) as f:
    ATTCK = json.load(f)

def score_threat(label, confidence, features=None):
    info     = ATTCK.get(label, {})
    base     = info.get('criticality_score', 0)
    modifier = 0
    reasons  = []
    if features:
        if features.get('num_failed_logins', 0) > 50:
            modifier += 1; reasons.append("Nombreuses tentatives (+1)")
        if features.get('src_bytes', 0) > 50000:
            modifier += 1; reasons.append("Volume élevé (+1)")
        if features.get('logged_in', 0) == 1 and label != 'NORMAL':
            modifier += 2; reasons.append("Connexion réussie (+2)")
    final = min(10, base + modifier)
    return {
        'base_score': base, 'modifier': modifier,
        'final_score': final, 'reasons': reasons,
        'alert_level': ('INFO' if final==0 else 'LOW' if final<=4
                        else 'MEDIUM' if final<=6 else 'HIGH' if final<=8
                        else 'CRITICAL')
    }
