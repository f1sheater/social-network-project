import os.path
import create_csv


def main():
    if not os.path.exists("water_resources_research_2020_2024.csv"):
        create_csv.save_csv()

    import histogram
    import erdos
    import affiliations

    histogram()
    erdos()
    affiliations()

if __name__ == "__main__":
    main()
