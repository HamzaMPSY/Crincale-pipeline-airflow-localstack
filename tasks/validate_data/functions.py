import csv
from typing import List
import pandas as pd
import re
import os


def convert_to_csv(device_data: list, path: str) -> None:
    """
    Converts a list of dictionaries to a csv file

    Args:
        device_data (list[dict]): List of dictionaries containing each device
        device_type (str): String specifiying the type of device: headphones or iems
        data_level (str): Signifies the level of data, ie, gold, bronze, silver
    """
    with open(path, "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=device_data[0].keys())
        writer.writeheader()
        writer.writerows(device_data)


def read_csv_as_dicts(filename: str) -> List[dict]:
    """
    Returns a list of dictionaries read from specified csv

    Args:
        filename (str): name of file to be read

    Returns:
        List[dict]
    """
    try:
        with open(filename, "r") as file:
            reader = csv.DictReader(file)
            return list(reader)
    except OSError as exception:
        print(f"{filename} - {exception}")


def sanitize_data(data: List[dict]) -> List[dict]:
    """
    Performs rudimentary sanitizations on bronze data

    Args:
        data (List[dict]): list of IEMs/Headphones

    Returns:
        List[dict]: Sanitized data
    """
    df = pd.DataFrame(data)
    columns_to_drop = [
        "comments",
        "based_on",
        "note_weight",
        "pricesort",
        "techsort",
        "tonesort",
        "ranksort"
    ]

    df = df.drop(columns_to_drop, axis=1, errors='ignore')

    # Some signatures have quotes around them, unneeded
    df["signature"] = df["signature"].str.replace('"', "")

    for index, row in df.iterrows():
        # Replacing discontinued devices with no price with -1
        if re.search("Discont", str(row["price"])):
            row["price"] = -1

        # Replacing ? device prices with -1
        if re.search("\\?", str(row["price"])):
            row["price"] = -1

        # Some prices have models embedded to them, this replaces with only price
        # Ex: 3000(HE1000) gives 3000
        if re.search("[a-zA-Z]", str(row["price"])):
            row["price"] = list(
                filter(None, re.split(r"(\d+)", str(row["price"]))))[0]

            # Some are still text even after splits and earlier cleanses
            if re.search("[a-zA-Z]", str(row["price"])):
                row["price"] = -1

        # Replace star text rating with number. If no stars, replace with -1
        row["value_rating"] = len(
            row["value_rating"]) if row["value_rating"] else -1

    return df.to_dict("records")


if __name__ == "__main__":
    bronze_headphones_file = os.getenv('PATH_TO_BRONZE_HEADPHONE_FILE')
    bronze_iems_file = os.getenv('PATH_TO_BRONZE_IEMS_FILE')

    iems_list = read_csv_as_dicts(bronze_headphones_file)
    headphones_list = read_csv_as_dicts(bronze_iems_file)

    # Sanitize both CSV files with similar parameters
    iems_list_sanitized = sanitize_data(iems_list)
    headphones_list_sanitized = sanitize_data(headphones_list)
