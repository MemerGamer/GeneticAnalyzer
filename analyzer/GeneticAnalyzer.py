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
        # Use graphviz_layout for better spacing
        pos = nx.nx_agraph.graphviz_layout(self.lineage, prog="dot", args='-Gnodesep=0.5 -Granksep=1.5')
        plt.figure(figsize=(16, 12))  # Larger figure size for better visualization

        # Draw all nodes
        nx.draw_networkx_nodes(self.lineage, pos, node_size=300, node_color="lightblue")

        # Draw all edges
        nx.draw_networkx_edges(
            self.lineage, pos,
            edgelist=[(u, v) for u, v, d in self.lineage.edges(data=True)],
            width=1, alpha=0.7, edge_color="gray"
        )

        # Add labels with fitness values
        labels = {node: f"{node}\n{data['fitness']:.2f}" for node, data in self.lineage.nodes(data=True)}
        nx.draw_networkx_labels(self.lineage, pos, labels=labels, font_size=8)

        # Highlight the best individual
        if highlight_best is not None:
            # Highlight the best node
            nx.draw_networkx_nodes(
                self.lineage, pos,
                nodelist=[highlight_best],
                node_size=600,  # Larger size
                node_color="orange"  # Distinct color
            )

            # Highlight the path from the root to the best individual
            path = self._get_path_from_root(highlight_best)
            if path:
                nx.draw_networkx_edges(
                    self.lineage, pos,
                    edgelist=list(zip(path[:-1], path[1:])),
                    width=3, edge_color="red"
                )

        plt.title("Family Tree of Population")
        plt.axis('off')  # Hide axis
        plt.show()


    def _get_path_from_root(self, target):
        # Traverse the tree from the root (0) to the target node
        path = []
        current_node = target
        while current_node != 0:
            path.append(current_node)
            parents = list(self.lineage.predecessors(current_node))
            if parents:
                current_node = parents[0]  # Move to the parent node
            else:
                break
        path.append(0)  # Add the root node to the path
        path.reverse()  # Reverse the path to go from root to target
        return path if path[-1] == 0 else None
