import networkx as nx
import matplotlib.pyplot as plt

class GeneticAnalyzer:
    def __init__(self):
        self.population = []
        self.lineage = nx.DiGraph()  # Directed graph for lineage
        self.generation = 0
        self.history = []  # Store historical data

    def add_individual(self, individual, parents=None, mutation_info=None):
        node_id = len(self.population)
        self.population.append(individual)
        self.lineage.add_node(node_id, fitness=individual["fitness"], details=individual)

        if parents:
            for parent in parents:
                self.lineage.add_edge(parent, node_id, type="crossover")

        if mutation_info:
            self.lineage.nodes[node_id]["mutation"] = mutation_info

        return node_id

    def visualize_tree(self, highlight_best=None):
        pos = nx.spring_layout(self.lineage)
        plt.figure(figsize=(12, 8))

        # Draw nodes
        nx.draw_networkx_nodes(self.lineage, pos, node_size=500)

        # Draw edges
        nx.draw_networkx_edges(
            self.lineage, pos, 
            edgelist=[(u, v) for u, v, d in self.lineage.edges(data=True)],
            width=1, alpha=0.7
        )

         # Highlight best individual
        if highlight_best is not None:
            try:
                best_path = nx.shortest_path(self.lineage, source=0, target=highlight_best)
                nx.draw_networkx_edges(self.lineage, pos, edgelist=list(zip(best_path[:-1], best_path[1:])), width=3, edge_color="red")
            except nx.NetworkXNoPath:
                print(f"No path found between node 0 and node {highlight_best}. The graph may be disconnected.")

        # Add labels
        labels = {node: f"{node}\n{data['fitness']:.2f}" for node, data in self.lineage.nodes(data=True)}
        nx.draw_networkx_labels(self.lineage, pos, labels=labels)

        plt.title("Family Tree of Population")
        plt.show()
