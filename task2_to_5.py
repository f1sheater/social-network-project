import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from collections import Counter
from collections import defaultdict

### 2)
def rank_authors(database):
    # Split the authors and flatten the list
    all_authors = []
    author_collaborators = defaultdict(set)

    for authors in database['Authors']:
        author_list = authors.strip('"').split(',')
        if author_list != ['']:
            all_authors.extend(author_list)
            for author in author_list:
                co_authors = set(author_list) - {author}  # Exclude self
                author_collaborators[author].update(co_authors)

    # Count publications per author
    author_publications = Counter(all_authors)

    # Turn into a DataFrame
    author_publications_df = pd.DataFrame(author_publications.items(), columns=['Author', 'Number_of_Publications'])

    # Sort descending
    author_publications_df = author_publications_df.sort_values(by='Number_of_Publications', ascending=False)

    print(author_publications_df.head())

    # Count number of unique collaborators
    author_collaborators_count = {author: len(collaborators) for author, collaborators in author_collaborators.items()}

    # Turn into a DataFrame
    author_collaborators_df = pd.DataFrame(author_collaborators_count.items(), columns=['Author', 'Number_of_Collaborators'])

    # Sort descending
    author_collaborators_df = author_collaborators_df.sort_values(by='Number_of_Collaborators', ascending=False)

    print(author_collaborators_df.head())

    plt.figure(figsize=(10,6))
    plt.hist(author_publications_df['Number_of_Publications'], bins=20, color='skyblue', edgecolor='black')
    plt.title('Distribution of Number of Publications per Author')
    plt.xlabel('Number of Publications')
    plt.ylabel('Number of Authors')
    plt.grid(True)
    plt.savefig("author_publications.png", dpi=300)

    plt.figure(figsize=(10,6))
    plt.hist(author_collaborators_df['Number_of_Collaborators'], bins=20, color='salmon', edgecolor='black')
    plt.title('Distribution of Number of Collaborators per Author')
    plt.xlabel('Number of Collaborators')
    plt.ylabel('Number of Authors')
    plt.grid(True)
    plt.savefig("author_collaborators.png", dpi=300)

    print("Figure: Author publications and affiliations histogram")
    plt.show()

### 3)
def rank_institutions(database):
    all_affiliations = []
    for affiliations in database['Affiliations']:
        affil_list = affiliations.strip('"').split(',')
        affil_set = set(affil_list)
        for affil in affil_set:
            if affil != "N/A" and affil != "":
                all_affiliations.append(affil)

    # Count publications per institution
    institution_publications = Counter(all_affiliations)
    publication_counts = list(institution_publications.values())

    # Turn into a DataFrame
    institution_publications_df = pd.DataFrame(institution_publications.items(), columns=['Affiliation', 'Number_of_Publications'])

    # Sort descending
    institution_publications_df = institution_publications_df.sort_values(by='Number_of_Publications', ascending=False)

    print(institution_publications_df.head())

    # Plot histogram of publication counts
    plt.figure(figsize=(10,6))
    plt.hist(publication_counts, bins=30, color='skyblue', edgecolor='black')

    # Titles and labels
    plt.title('Distribution of Publications Across Institutions')
    plt.xlabel('Number of Publications per Institution')
    plt.ylabel('Number of Institutions')
    plt.grid(True)
    plt.savefig("institution_publications.png", dpi=300)

    print("Figure: Institution publications histogram")
    plt.show()

def rank_keywords(database):
    # Collect all keywords
    all_keywords = []
    for keywords in database['Keywords']:
        keyword_list = keywords.strip("").split(',')  # Split keywords by comma
        all_keywords.extend(keyword_list)

    # Count how many times each keyword appears
    keyword_counts = Counter(all_keywords)

    # Convert keyword frequency values to a list
    frequencies = list(keyword_counts.values())

    # Turn into a DataFrame
    keyword_counts_df = pd.DataFrame(keyword_counts.items(), columns=['Keyword', 'Count'])

    # Sort descending
    keyword_counts_df = keyword_counts_df.sort_values(by='Count', ascending=False)

    print(keyword_counts_df.head())

    # Plot histogram of these frequencies
    plt.figure(figsize=(8, 6))
    plt.hist(frequencies, bins=range(1, max(frequencies)+2), color='steelblue', edgecolor='black', align='left')
    plt.xlabel("Number of Articles a Keyword Appears In")
    plt.ylabel("Number of Keywords")
    plt.title("Histogram of Keyword Frequencies")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.savefig("keyword_count.png", dpi=300)
    plt.tight_layout()
    plt.show()


    ### OLD CODE ###
    # # Count how many times each keyword appears
    # keyword_counts = Counter(all_keywords)
    # keyword_publications = list(keyword_counts.values())

    # # Plot histogram of keyword publication counts
    # plt.figure(figsize=(10,6))
    # plt.hist(keyword_publications, bins=30, color='purple', edgecolor='black')

    # # Titles and labels
    # plt.title('Distribution of Keywords Across Articles')
    # plt.xlabel('Number of Articles per Keyword')
    # plt.ylabel('Number of Keywords')
    # plt.grid(True)
    # plt.savefig("keyword_count.png", dpi=300)

    # print("Figure: Keyword count histogram")
    # plt.show()

### 4)
def create_paper_graph(database):
    # Initialize an empty graph
    G = nx.DiGraph()
    id_list = list(database["Work ID"])

    # Add nodes (papers) and edges (references between papers)
    for i, work_id in enumerate(id_list):
        references = database['References'][i].strip('"').split(',')

        # Add the node for the paper
        G.add_node(work_id)

        # For each reference, create an edge
        for ref in references:
            if ref in id_list:
                G.add_edge(work_id, ref)  # Paper -- Reference

    ### Compute Global Properties
    # Number of nodes
    num_nodes = G.number_of_nodes()

    # Number of edges
    num_edges = G.number_of_edges()

    # Diameter
    if nx.is_weakly_connected(G):
        diameter = nx.diameter(G.to_undirected())
    else:
        largest_weak_cc = max(nx.weakly_connected_components(G), key=len)
        subgraph = G.subgraph(largest_weak_cc)
        diameter = nx.diameter(subgraph.to_undirected())

    # Clustering coefficient
    avg_clustering_coefficient = nx.average_clustering(G)

    # Number of connected components
    num_components = nx.number_connected_components(G.to_undirected())

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
    print("Paper graph properties: ")
    print(graph_properties)


    ### 5)
    ### calculate_hub_scores
    # Compute HITS scores
    hubs, authorities = nx.hits(G, max_iter=1000, normalized=True)

    # Extract hub scores
    hub_scores = list(hubs.values())

    # Plot a histogram of hub score distribution
    plt.figure(figsize=(8, 6))
    plt.hist(hub_scores, bins=20, color='steelblue', edgecolor='black')
    plt.xlabel("Hub Score")
    plt.ylabel("Number of Papers")
    plt.title("Histogram of Hub Scores (HITS Algorithm)")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.savefig("hub_scores.png", dpi=300)
    plt.tight_layout()

    print("Figure: Hub scores histogram")
    plt.show()

def compute_all():
    database = pd.read_csv("water_resources_research_2020_2024.csv")
    rank_authors(database)
    rank_institutions(database)
    rank_keywords(database)
    create_paper_graph(database)
