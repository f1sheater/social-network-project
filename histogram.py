import pandas as pd
import matplotlib.pyplot as plt
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

plt.show()
