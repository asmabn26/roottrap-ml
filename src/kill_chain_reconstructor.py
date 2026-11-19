import networkx as nx
import json

def build_kill_chain_dag(events: list) -> nx.DiGraph:
    G = nx.DiGraph()
    for i, event in enumerate(events):
        node_id = f"evt_{i}"
        G.add_node(node_id,
            label       = event["label"],
            source_ip   = event["source_ip"],
            timestamp   = event["timestamp"],
            confidence  = event["confidence"],
            att_ck      = event.get("att_ck_technique_id", "N/A"),
            criticality = event.get("criticality_score", 0)
        )
        if i > 0:
            G.add_edge(f"evt_{i-1}", node_id)
    return G

def dag_to_json(G: nx.DiGraph) -> dict:
    """Convertit le DAG en JSON pour P4 (dashboard)."""
    return {
        "nodes": [{"id": n, **G.nodes[n]} for n in G.nodes],
        "edges": [{"from": u, "to": v} for u, v in G.edges],
        "is_valid_dag": nx.is_directed_acyclic_graph(G),
        "total_events": G.number_of_nodes(),
        "attack_duration": f"{G.number_of_nodes() * 15} min"
    }

if __name__ == "__main__":
    events = [
        {"label": "PORT_SCAN",   "source_ip": "1.2.3.4", "timestamp": "14:00", "confidence": 0.91, "att_ck_technique_id": "T1046", "criticality_score": 5},
        {"label": "BRUTE_FORCE", "source_ip": "1.2.3.4", "timestamp": "14:15", "confidence": 0.94, "att_ck_technique_id": "T1110", "criticality_score": 6},
        {"label": "BOT",         "source_ip": "1.2.3.4", "timestamp": "15:00", "confidence": 0.95, "att_ck_technique_id": "T1071", "criticality_score": 10},
    ]
    G    = build_kill_chain_dag(events)
    data = dag_to_json(G)
    print(json.dumps(data, indent=2))
