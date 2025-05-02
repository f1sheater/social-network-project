import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict

erdos_author = str()
erdos_numbers = dict()
G = nx.Graph()

### 6/7)
def calculate_erdos_numbers():
    database = pd.read_csv("water_resources_research_2020_2024.csv")
    author_collaborators = defaultdict(set)

    for authors in database['Authors']:
        author_list = authors.strip('"').split(',')
        if author_list != ['']:
            for author in author_list:
                co_authors = set(author_list) - {author}  # Exclude self
                for co_author in co_authors:
                    G.add_edge(author, co_author)

    erdos_author = max(G.degree, key=lambda x: x[1])[0]

    erdos_numbers = nx.single_source_shortest_path_length(G, erdos_author)

    values = list(erdos_numbers.values())

    plt.figure(figsize=(8, 6))
    plt.hist(values, bins=range(max(values)+2), align='left', color='mediumseagreen', edgecolor='black')
    plt.xlabel(f"Distance from {erdos_author} (Erdős Number)")
    plt.ylabel("Number of Authors")
    plt.title(f"Erdős Number Distribution from {erdos_author}")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.savefig("erdos_histogram.png", dpi=300)
    plt.tight_layout()

    print("Figure: Erdos numbers histogram")
    plt.show()


    ### 8)
    ### create_erdos_subgraph
    subset_nodes = [author for author, dist in erdos_numbers.items() if dist in [0, 1, 2]]
    H = G.subgraph(subset_nodes)

    node_colors = []
    for node in H.nodes():
        if erdos_numbers[node] == 0:
            node_colors.append("red")
        elif erdos_numbers[node] == 1:
            node_colors.append("skyblue")
        elif erdos_numbers[node] == 2:
            node_colors.append("lightgreen")

    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(H, seed=42)
    nx.draw_networkx_nodes(H, pos, node_color=node_colors, node_size=300, alpha=0.9)
    nx.draw_networkx_edges(H, pos, alpha=0.4)

    plt.title(f"Author Collaboration Network: Erdős Number 1 and 2 from '{erdos_author}'")
    plt.axis('off')
    plt.savefig("erdos_graph.png", dpi=300)
    plt.tight_layout()

    print("Figure: Graph of authors with erdos number < 3")
    plt.show()

def compute_all():
    calculate_erdos_numbers()
