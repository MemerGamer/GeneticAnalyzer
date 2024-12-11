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
        # Use graphviz_layout to create a more tree-like layout
        pos = nx.nx_agraph.graphviz_layout(self.lineage, prog="dot")  # 'dot' is a good choice for hierarchical layouts
        plt.figure(figsize=(12, 8))

        # Draw nodes
        nx.draw_networkx_nodes(self.lineage, pos, node_size=500, node_color="lightblue")

        # Draw edges
        nx.draw_networkx_edges(
            self.lineage, pos, 
            edgelist=[(u, v) for u, v, d in self.lineage.edges(data=True)],
            width=1, alpha=0.7, edge_color="gray"
        )

        # Highlight best individual (if there is a path, highlight it)
        if highlight_best is not None:
            try:
                # Find path to highlight (if possible)
                best_path = nx.shortest_path(self.lineage, source=0, target=highlight_best)
                nx.draw_networkx_edges(self.lineage, pos, edgelist=list(zip(best_path[:-1], best_path[1:])), width=3, edge_color="red")
            except nx.NetworkXNoPath:
                # If no path, highlight the generation instead
                print(f"No path found between node 0 and node {highlight_best}. Highlighting generation instead.")
                # Find the generation of the highlighted individual
                generation_level = self._get_generation(highlight_best)
                generation_nodes = [node for node, data in self.lineage.nodes(data=True) if data.get("generation") == generation_level]
                nx.draw_networkx_nodes(self.lineage, pos, nodelist=generation_nodes, node_size=500, node_color="orange")

        # Add labels with fitness values
        labels = {node: f"{node}\n{data['fitness']:.2f}" for node, data in self.lineage.nodes(data=True)}
        nx.draw_networkx_labels(self.lineage, pos, labels=labels)

        plt.title("Family Tree of Population")
        plt.axis('off')  # Hide the axis for a cleaner visualization
        plt.show()

    def _get_generation(self, node):
        # Traverse the tree from node to root and count generations
        generation = 0
        while True:
            parents = list(self.lineage.predecessors(node))
            if not parents:
                break
            node = parents[0]  # Move to the parent node
            generation += 1
        return generation
