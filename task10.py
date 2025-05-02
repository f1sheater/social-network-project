import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import powerlaw

database = pd.read_csv("water_resources_research_2020_2024.csv")

### 10)
def compute_all():
    G = nx.Graph()

    for affiliations in database['Affiliations']:
        affiliations_set = set(affiliations.strip('"').split(","))
        for institution in affiliations_set:
            if institution != 'N/A' and institution != '':
                for other_institution in affiliations_set:
                    if institution != other_institution and other_institution != 'N/A':
                        G.add_edge(institution, other_institution)

    ### Compute Global Properties
    # Number of nodes
    num_nodes = G.number_of_nodes()

    # Number of edges
    num_edges = G.number_of_edges()

    # Diameter
    if nx.is_connected(G):
        diameter = nx.diameter(G)
    else:
        largest_component = max(nx.connected_components(G), key=len)
        subgraph = G.subgraph(largest_component)
        diameter = nx.diameter(subgraph)

    # Clustering coefficient
    avg_clustering_coefficient = nx.average_clustering(G)

    # Number of connected components
    num_components = nx.number_connected_components(G)

    # Average degree
    avg_degree = np.mean([d for n, d in G.degree()])

    # Standard deviation of degrees
    std_degree = np.std([d for n, d in G.degree()])

    # Compile the results in a DataFrame
    graph_properties = pd.DataFrame({
        'Number of Nodes': [num_nodes],
        'Number of Edges': [num_edges],
        'Diameter': [diameter],
        'Average Clustering Coefficient': [avg_clustering_coefficient],
        'Number of Components': [num_components],
        'Average Degree': [avg_degree],
        'Degree Standard Deviation': [std_degree]
    })

    # Display the properties
    print("Institutions graph properties: ")
    print(graph_properties)

    ### Get degree distribution
    degrees = []

    for (key, value) in G.degree():
        degrees.append(value)

    plt.figure(figsize=(8, 6))
    plt.hist(degrees, bins=20, color='steelblue', edgecolor='black')
    plt.xlabel("Degree")
    plt.ylabel("Number of Nodes")
    plt.title("Histogram of Degree of Nodes")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.savefig("institution_degree_distribution.png", dpi=300)
    plt.tight_layout()

    print("Figure: Degree of institutions histogram")
    plt.show()

    ### Fitting power law distribution
    # Filter out zero degrees
    filtered_degrees = [d for d in degrees if d > 0]

    # Fit a power law model
    fit = powerlaw.Fit(filtered_degrees, discrete=True)
    print(f"Alpha: {fit.alpha:.2f}")
    print(f"Xmin: {fit.xmin}")

    # Plot histogram and fit on log-log scale
    plt.figure(figsize=(8, 6))
    fit.plot_pdf(color='steelblue', label='Empirical', linewidth=2)
    fit.power_law.plot_pdf(color='darkred', linestyle='--', label=f'Power Law fit\nα = {fit.alpha:.2f}', linewidth=2)

    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel("Degree (log scale)")
    plt.ylabel("Probability Density (log scale)")
    plt.title("Degree Distribution with Power-Law Fit (Log-Log Scale)")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend()
    plt.savefig("power_law_fit.png", dpi=300)
    plt.tight_layout()

    print("Figure: Power law fit")
    plt.show()
