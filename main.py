import os.path
import create_csv
import task2_to_5
import task6_to_8
import task10

def main():
    if not os.path.exists("water_resources_research_2020_2024.csv"):
        create_csv.save_csv()

    #task2_to_5.compute_all()
    #task6_to_8.compute_all()
    #task10.compute_all()


if __name__ == "__main__":
    main()
