import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import requests
from collections import Counter
from collections import defaultdict

database = pd.read_csv("water_resources_research_2020_2024.csv")

### 2)
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

plt.figure(figsize=(10,6))
plt.hist(author_collaborators_df['Number_of_Collaborators'], bins=20, color='salmon', edgecolor='black')
plt.title('Distribution of Number of Collaborators per Author')
plt.xlabel('Number of Collaborators')
plt.ylabel('Number of Authors')
plt.grid(True)


### 3)
all_affiliations = []
for affiliations in database['Affiliations']:
    affil_list = affiliations.strip('"').split(',')
    affil_set = set(affil_list)
    for affil in affil_set:
        if affil != "N/A":
            all_affiliations.append(affil)


# Count publications per institution
institution_publications = Counter(all_affiliations)
publication_counts = list(institution_publications.values())

# Turn into a DataFrame
institution_publications_df = pd.DataFrame(institution_publications.items(), columns=['Author', 'Number_of_Publications'])

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

# Collect all keywords (concepts)
all_keywords = []
for keywords in database['Keywords']:
    keyword_list = keywords.strip("").split(',')  # Split keywords by comma
    all_keywords.extend(keyword_list)

# Count how many times each keyword appears
keyword_counts = Counter(all_keywords)
keyword_publications = list(keyword_counts.values())

# Turn into a DataFrame
keyword_counts_df = pd.DataFrame(keyword_counts.items(), columns=['Author', 'Number_of_Publications'])

# Sort descending
keyword_counts_df = keyword_counts_df.sort_values(by='Number_of_Publications', ascending=False)

print(keyword_counts_df.head())

# Plot histogram of keyword publication counts
plt.figure(figsize=(10,6))
plt.hist(keyword_publications, bins=30, color='purple', edgecolor='black')

# Titles and labels
plt.title('Distribution of Keywords Across Articles')
plt.xlabel('Number of Articles per Keyword')
plt.ylabel('Number of Keywords')

plt.grid(True)

# Assume df is the DataFrame containing your paper data, with 'Title' and 'References' columns
# df['Title'] contains paper titles
# df['References'] contains a list of references (paper titles that this paper references)

# Step 1: Create the Undirected Graph

# Initialize an empty undirected graph
G = nx.Graph()
counter = 0

# Add nodes (papers) and edges (references between papers)
for index, row in database.iterrows():
    id = row['Work ID']
    print(id)
    references = row['References'].strip('"').split(',')  # Assuming references are separated by semicolon

    # Add the node for the paper
    if id not in G:
        counter += 1
        print(counter)
        G.add_node(id)

    # For each reference, create an undirected edge (bidirectional link)
    id_list = list(database["Work ID"])
    for ref in references:
        if ref in id_list:
            if ref not in G:
                G.add_node(ref)  # Ensure the referenced paper is in the graph
            G.add_edge(id, ref)  # Paper -- Reference (undirected)
            print("edge added")

# Step 2: Compute Global Properties

# Number of nodes (papers)
num_nodes = G.number_of_nodes()
print(num_nodes)

# Number of edges (references)
num_edges = G.number_of_edges()


# Diameter (longest shortest path between any two nodes)
# The diameter is only defined for connected graphs, so we will check if the graph is connected.
# If not, we will use the largest connected component for diameter calculation.
if nx.is_connected(G):
    diameter = nx.diameter(G)
    print("if")
else:
    # Find the largest connected component and compute diameter
    largest_component = max(nx.connected_components(G), key=len)
    print("comp got")
    subgraph = G.subgraph(largest_component)
    print(f"subgraph size: {subgraph.number_of_nodes()}")
    diameter = nx.diameter(subgraph)
    print("else")
print("diameter")
print(database["Work ID"])
print(list(database["Work ID"]))

# Clustering coefficient (average for the whole graph)
avg_clustering_coefficient = nx.average_clustering(G)

# Number of connected components (subgraphs)
num_components = nx.number_connected_components(G)

# Average degree (average number of edges per node)
avg_degree = np.mean([d for n, d in G.degree()])

# Standard deviation of degrees
std_degree = np.std([d for n, d in G.degree()])

# Step 3: Compile the results in a DataFrame
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
print(graph_properties)

plt.figure(figsize=(10, 10))
nx.draw(subgraph, with_labels=True, node_size=50, font_size=8)
plt.show()
