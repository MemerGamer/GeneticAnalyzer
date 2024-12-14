import networkx as nx
import matplotlib.pyplot as plt


class GeneticAnalyzer:
    def __init__(self):
        self.population = []
        self.lineage = nx.DiGraph()  # Directed graph for lineage
        self.generation = 0
        self.history = []  # Store historical data

    def add_individual(
        self, individual, parents=None, mutation_info=None, generation=0
    ):
        node_id = len(self.population)
        self.population.append(individual)
        self.lineage.add_node(
            node_id,
            fitness=individual["fitness"],
            details=individual,
            generation=generation,
        )

        if parents:
            for parent in parents:
                self.lineage.add_edge(parent, node_id, type="crossover")

        if mutation_info:
            self.lineage.nodes[node_id]["mutation"] = mutation_info

        return node_id

    def plot_fitness_over_generations(self):
        # Group fitness values by generation
        generations = {}
        for node, data in self.lineage.nodes(data=True):
            generation = data["details"].get("generation", 0)
            fitness = data["fitness"]
            generations.setdefault(generation, []).append(fitness)

        # Sort generations and calculate average fitness
        sorted_generations = sorted(generations.items())
        gen_numbers = [gen for gen, _ in sorted_generations]
        avg_fitness = [sum(fits) / len(fits) for _, fits in sorted_generations]

        # Plot the fitness values
        plt.figure(figsize=(10, 6))
        plt.plot(gen_numbers, avg_fitness, marker="o", label="Average Fitness")
        plt.title("Fitness Over Generations")
        plt.xlabel("Generation")
        plt.ylabel("Average Fitness")
        plt.grid()
        plt.legend()
        plt.show()

    def visualize_tree(
        self, highlight_best=None, layout="dot", node_style=None, edge_style=None
    ):
        if layout == "dot":
            pos = nx.nx_agraph.graphviz_layout(
                self.lineage, prog="dot", args="-Gnodesep=0.5 -Granksep=1.5"
            )
        elif layout == "spring":
            pos = nx.spring_layout(self.lineage)
        elif layout == "circular":
            pos = nx.circular_layout(self.lineage)
        elif layout == "random":
            pos = nx.random_layout(self.lineage)
        else:
            raise ValueError(f"Unsupported layout: {layout}")

        plt.figure(figsize=(16, 12))

        # Define node colors dynamically based on fitness
        max_fitness = max(nx.get_node_attributes(self.lineage, "fitness").values())
        node_colors = [
            plt.cm.viridis(
                data["fitness"] / max_fitness
            )  # Normalized fitness for colormap
            for _, data in self.lineage.nodes(data=True)
        ]
        node_sizes = [300 for _ in self.lineage.nodes]

        # Draw nodes with dynamic styles
        nx.draw_networkx_nodes(
            self.lineage, pos, node_size=node_sizes, node_color=node_colors
        )

        # Define edge colors dynamically based on edge type
        edge_colors = [
            (
                "blue"
                if d["type"] == "crossover"
                else "purple" if d.get("type") == "mutation" else "gray"
            )
            for _, _, d in self.lineage.edges(data=True)
        ]

        # Draw edges with dynamic styles
        nx.draw_networkx_edges(
            self.lineage,
            pos,
            edgelist=[(u, v) for u, v, d in self.lineage.edges(data=True)],
            width=1,
            alpha=0.7,
            edge_color=edge_colors,
        )

        # Add labels with fitness values
        labels = {
            node: f"{node}\n{data['fitness']:.2f}"
            for node, data in self.lineage.nodes(data=True)
        }
        nx.draw_networkx_labels(self.lineage, pos, labels=labels, font_size=8)

        # Highlight the best individual
        if highlight_best is not None:
            nx.draw_networkx_nodes(
                self.lineage,
                pos,
                nodelist=[highlight_best],
                node_size=600,
                node_color="orange",
            )
            path = self._get_path_from_root(highlight_best)
            if path:
                nx.draw_networkx_edges(
                    self.lineage,
                    pos,
                    edgelist=list(zip(path[:-1], path[1:])),
                    width=3,
                    edge_color="red",
                )

        plt.title("Family Tree of Population")
        plt.axis("off")
        plt.show()

    def _get_path_from_root(self, target):
        # Traverse the tree from the oldest ancestor to the target node
        # Find all root nodes (nodes with no predecessors)
        roots = [
            node
            for node in self.lineage.nodes
            if not list(self.lineage.predecessors(node))
        ]

        # If there are multiple roots, pick the one connected to the target
        for root in roots:
            try:
                # Compute the path from root to the target using shortest path
                path = nx.shortest_path(self.lineage, source=root, target=target)
                return path
            except nx.NetworkXNoPath:
                continue  # Try the next root if no path exists

        return None  # Return None if no path is found
