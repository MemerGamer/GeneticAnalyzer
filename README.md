# Genetic Algorithm Lineage Visualizer

A Python library for managing and visualizing the evolution of populations in genetic algorithms. The **GeneticAnalyzer** library tracks individuals, their lineage through crossovers and mutations, and provides intuitive visualizations of the family tree. This tool is perfect for understanding and presenting the evolutionary process.

> **Note**: The **GeneticAnalyzer** library uses **graphviz** to generate graphs, so make sure you have it installed and configured correctly.
> Refer to the [Graphviz Installation Guide](https://pygraphviz.github.io/documentation/stable/install.html) for platform-specific instructions.

---

## Features

- **Track Lineage**: Log individuals, parental relationships, and mutations across generations.
- **Visualize Family Tree**: Generate a graph of the population's lineage to trace genetic evolution.
- **Highlight Best Individuals**: Mark the highest-performing individual and trace their ancestry.
- **Customizable Workflows**: Integrate with any fitness function, mutation, or crossover mechanism.

---

## Installation

### Using pip

```bash
pip install geneticanalyzer
```

### Manually

1. Clone the repository:

   ```bash
   git clone https://github.com/MemerGamer/GeneticAnalyzer.git
   cd GeneticAnalyzer
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Install **Graphviz** (required by `pygraphviz`):

   Refer to the [Graphviz Installation Guide](https://pygraphviz.github.io/documentation/stable/install.html) for platform-specific instructions.

---

## Usage

### Overview

The **GeneticAnalyzer** class provides an easy-to-use interface to track the population's evolution and visualize its lineage. The main methods include:

- **`add_individual`**: Add an individual with optional parent relationships and mutation details.
- **`visualize_tree`**: Generate a graphical representation of the population's lineage.
- **`plot_fitness_over_generations`**: Plot the average fitness across generations.

### Example Usage

See examples in the [**GeneticAnalyzerExamples** repository](https://github.com/MemerGamer/GeneticAnalyzerExamples).

Below is an example of using **GeneticAnalyzer** in a Python script to track and visualize population evolution.

#### Example Script

```python
from analyzer import GeneticAnalyzer

# Initialize the GeneticAnalyzer
analyzer = GeneticAnalyzer()

# Add individuals to the population
individual_1 = {"genes": [1, 0, 1, 1, 0], "fitness": 3.0}
individual_2 = {"genes": [0, 1, 0, 1, 1], "fitness": 2.5}
id_1 = analyzer.add_individual(individual_1, generation=0)
id_2 = analyzer.add_individual(individual_2, generation=0)

# Create a child via crossover and mutation
child = {"genes": [1, 1, 1, 1, 0], "fitness": 4.0}
child_id = analyzer.add_individual(child, parents=[id_1, id_2], mutation_info="Bit flip", generation=1)

# Visualize the family tree
analyzer.visualize_tree(highlight_best=child_id)

# Plot fitness over generations
analyzer.plot_fitness_over_generations()
```

### Visualization Output

![demo](./demo.png)

1. **Family Tree**: A directed graph showing the lineage of individuals, with:

   - Nodes representing individuals (labeled with fitness scores).
   - Edges representing parent-child relationships via crossover or mutation.
   - Best individual highlighted in **orange**.
   - Lineage path traced in **red**.

2. **Fitness Plot**: A line graph showing the average fitness of the population over generations.

---

## Key Methods

### `GeneticAnalyzer.add_individual`

Adds an individual to the population and records relationships.

| Parameter       | Type              | Description                                                |
| --------------- | ----------------- | ---------------------------------------------------------- |
| `individual`    | `dict`            | Contains `genes` (list) and `fitness` (float).             |
| `parents`       | `list` (optional) | List of parent IDs.                                        |
| `mutation_info` | `str` (optional)  | Description of mutation applied.                           |
| `generation`    | `int` (optional)  | Generation to which this individual belongs. Default: `0`. |

Returns the unique ID of the individual.

---

### `GeneticAnalyzer.visualize_tree`

Generates a visual representation of the family tree.

| Parameter        | Type             | Description                                                                     |
| ---------------- | ---------------- | ------------------------------------------------------------------------------- |
| `highlight_best` | `int` (optional) | ID of the best individual to highlight in **orange**.                           |
| `layout`         | `str` (optional) | Layout style (`"dot"`, `"spring"`, `"circular"`, `"random"`). Default: `"dot"`. |

---

### `GeneticAnalyzer.plot_fitness_over_generations`

Plots the average fitness of the population across generations.

No parameters required.

---

## Advanced Customization

1. **Fitness Function**:  
   Replace the fitness function to evaluate individuals based on your custom criteria.

   ```python
   def fitness_function(individual):
       return sum(individual)  # Example: maximize the sum of binary genes
   ```

2. **Mutation**:  
   Modify the mutation mechanism to suit your requirements.

   ```python
   def mutate(individual, mutation_rate=0.1):
       for i in range(len(individual)):
           if random.random() < mutation_rate:
               individual[i] = 1 - individual[i]  # Flip binary bit
       return individual
   ```

3. **Crossover**:  
   Customize the crossover strategy to combine parent genes.

   ```python
   def crossover(parent1, parent2):
       point = random.randint(1, len(parent1) - 1)
       return parent1[:point] + parent2[point:], parent2[:point] + parent1[point:]
   ```

---

## Visualization Notes

- **Node Colors**: Nodes are colored dynamically based on fitness scores (normalized to a colormap).
- **Edge Colors**:
  - Blue: Crossover relationships.
  - Purple: Mutations.
- **Best Individual**:
  - Highlighted in **orange**.
  - Lineage traced in **red** from the root (oldest ancestor) to the individual.

---

## Requirements

- Python 3.7 or higher
- Libraries:
  - `matplotlib`
  - `networkx`
  - `pygraphviz`
- **Graphviz**: Ensure Graphviz is installed on your system.

---

## License

This project is licensed under the GPLv3 License. See the [LICENSE](LICENSE) file for details.

---

## Author

Developed by **Kovács Bálint-Hunor (MemerGamer)**. Contributions and suggestions are welcome!
