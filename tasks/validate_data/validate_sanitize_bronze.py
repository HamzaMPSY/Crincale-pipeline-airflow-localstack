import os
from pydantic import ValidationError
from functions import convert_to_csv, read_csv_as_dicts, sanitize_data
from models import InEarMonitor, Headphone


if __name__ == "__main__":
    bronze_headphones_file = os.getenv('PATH_TO_BRONZE_HEADPHONE_FILE')
    bronze_iems_file = os.getenv('PATH_TO_BRONZE_IEMS_FILE')
    silver_headphones_file = os.getenv('PATH_TO_SILVER_HEADPHONE_FILE')
    silver_iems_file = os.getenv('PATH_TO_SILVER_IEMS_FILE')

    iems_list = read_csv_as_dicts(bronze_headphones_file)
    headphones_list = read_csv_as_dicts(bronze_iems_file)

    # Sanitize both CSV files with similar parameters
    iems_list_sanitized = sanitize_data(iems_list)
    headphones_list_sanitized = sanitize_data(headphones_list)

    # Validates all headphones/iems in a list based on the validators
    # defined in the respective PyDantic models
    try:
        iems_list = [InEarMonitor.parse_obj(iem)
                     for iem in iems_list_sanitized]
    except ValidationError as exception:
        print(f"IEM - {exception}")

    try:
        headphones_list = [
            Headphone.parse_obj(headphone) for headphone in headphones_list_sanitized
        ]
    except ValidationError as exception:
        print(f"Headphone - {exception}")

    convert_to_csv(
        device_data=iems_list_sanitized,
        path=silver_headphones_file)
    convert_to_csv(
        device_data=headphones_list_sanitized,
        path=silver_iems_file)
