import networkx as nx
import matplotlib.pyplot as plt


class GeneticAnalyzer:
    def __init__(self):
        """
        Initialize GeneticAnalyzer object.

        The GeneticAnalyzer is responsible for tracking a population, their
        lineage, and historical data. This object is used to visualize the
        evolution of a population over time.

        :param population: List of individuals in the population
        :param lineage: Directed graph for storing the population's lineage
        :param generation: Current generation number
        :param history: List of historical data
        """
        self.population = []
        self.lineage = nx.DiGraph()  # Directed graph for lineage
        self.generation = 0
        self.history = []  # Store historical data

    def add_individual(
        self, individual, parents=None, mutation_info=None, generation=0
    ):
        """
        Add an individual to the population.

        :param individual: A dictionary containing the individual's details
        :param parents: List of parent nodes in the lineage
        :param mutation_info: Mutation information associated with the individual
        :param generation: Generation number of the individual
        :return: The node ID of the added individual
        """
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
        """
        Plot the average fitness of the population across generations.

        This function groups individuals' fitness values by their generation,
        calculates the average fitness for each generation, and plots these
        averages over generations using a line graph.

        The x-axis represents the generation number, and the y-axis represents
        the average fitness score. The graph includes markers for each
        generation, a grid for better readability, and a legend indicating
        the plotted data series.

        The plot is displayed using matplotlib and will show a visual trend
        of how the average fitness of the population evolves over time.
        """
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
        """
        Visualize the family tree of the population as a directed graph.

        This method creates a visualization of the population's lineage using a
        directed graph. The graph is laid out according to the specified
        layout, and nodes are colored based on their fitness scores. Edges are
        colored based on the type of relationship they represent. The graph
        includes labels with the fitness values for each individual.

        If a node ID is provided for `highlight_best`, the best individual is
        highlighted in orange, and its lineage is traced from the root node to
        the individual in red.

        The graph is displayed using matplotlib.

        :param highlight_best: Node ID of the best individual to highlight
        :param layout: Layout style for the graph ("dot", "spring", "circular", "random")
        :param node_style: Dictionary of node styles (e.g. node_size, node_color)
        :param edge_style: Dictionary of edge styles (e.g. width, edge_color)
        """
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
        """
        Finds the path from the oldest ancestor to the target node in the
        lineage graph.

        The method starts by finding all root nodes (nodes with no
        predecessors) in the graph. If there are multiple roots, it will try
        each one in turn to find a path to the target node. If a path is found,
        it is returned. If no path is found, the method returns None.

        :param target: The node to find the path to
        :return: The path from the oldest ancestor to the target node, or None
        """

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
