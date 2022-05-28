import json
import os
import glob

# all scraped files are present inside places_to_visit folder
current_directory_path = os.getcwd() + "/" + os.path.dirname(__file__)

# function to get all the json files and put it inside a dedicated data directory directory
def get_scraped_json_file_path():
    yield from glob.glob(f"{current_directory_path}/[a|n]*.json")


def main():
    consolidated_json = list()
    for json_file in get_scraped_json_file_path():
        print(json_file)
        with open(json_file, "r") as each_json_data:
            consolidated_json.extend(json.load(each_json_data))

    with open(f"{current_directory_path}/raw.json", "w") as raw_file: 
        json.dump(consolidated_json, raw_file, indent=2)


if __name__ == "__main__" :
    main()