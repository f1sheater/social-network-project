import requests
import pandas as pd
import time
from collections import Counter
import matplotlib.pyplot as plt

def main():
    database = create_database()
    save_csv(database)

def create_database():
    # Define the base URL and parameters
    base_url = "https://api.openalex.org/works"
    params = {
        "filter": "primary_location.source.issn:0043-1397,from_publication_date:2020-01-01,to_publication_date:2024-12-31",
        "per-page": 200,
        "cursor": "*"
    }

    # Initialize an empty list to store the results
    results = []

    while True:
        response = requests.get(base_url, params=params)
        data = response.json()
        results.extend(data['results'])
        if 'next_cursor' in data['meta'] and data['meta']['next_cursor']:
            params['cursor'] = data['meta']['next_cursor']
            time.sleep(1)  # To respect API rate limits
        else:
            break

    titles = []
    ids = []
    authors_list = []
    affiliations_list = []
    keywords_list = []
    references_list = []

    for work in results:
        title = work.get('title', '')
        if title != None and title != "Issue Information" and title != "":
            titles.append(work.get('title', ''))
            ids.append(work.get('id', '').split('/')[-1])

            authors = []
            affiliations = []
            for author in work.get('authorships', []):
                authors.append(author.get('author', {}).get('display_name', ''))
                
                institutions = author.get('institutions', [])
                if institutions:
                    affiliations.append(institutions[0].get('display_name', ''))
                else:
                    affiliations.append('N/A')

            authors_list.append(f'"{",".join(authors)}"')
            affiliations_list.append(f'"{",".join(affiliations)}"')

            # Extract keywords (concepts)
            concepts = work.get('concepts', [])
            keywords = [concept.get('display_name', '') for concept in concepts]
            keywords_list.append(f'"{",".join(keywords)}"')

            # References (may be missing)
            references = work.get('referenced_works', [])
            for i, ref in enumerate(references):
                references[i] = ref.split('/')[-1]
            references_list.append(f'"{",".join(references) if references else "N/A"}"')

    # Create DataFrame
    df = pd.DataFrame({
        'Title': titles,
        'Work ID': ids,
        'Authors': authors_list,
        'Affiliations': affiliations_list,
        'Keywords': keywords_list,
        'References': references_list
    })

    return df

def save_csv(data):
    # Save to CSV
    data.to_csv('water_resources_research_2020_2024.csv', index=False)

print("Creating database...")
main()
print("Database created")
