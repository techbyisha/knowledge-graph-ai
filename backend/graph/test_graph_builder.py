from backend.graph.graph_builder import GraphBuilder

data = {
    "entities": [
        {"name": "Authentication Service", "type": "Service"},
        {"name": "Identity Team", "type": "Team"},
        {"name": "Kubernetes", "type": "Technology"},
        {"name": "GCP", "type": "Cloud"}
    ],
    "relationships": [
        {"source": "Authentication Service", "relation": "OWNED_BY", "target": "Identity Team"},
        {"source": "Authentication Service", "relation": "DEPLOYED_ON", "target": "Kubernetes"},
        {"source": "Kubernetes", "relation": "HOSTED_IN", "target": "GCP"}
    ]
}

builder = GraphBuilder()

builder.build_graph(data)

print("Graph successfully created!")