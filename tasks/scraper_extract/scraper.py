import logging
import re
import requests
from bs4 import BeautifulSoup
import csv
import os

logging.basicConfig(filename="logs.log", level=logging.INFO)
# truncating log file before new run
with open("logs.log", "w"):
    pass


class Scraper:
    """
        Encapsulates all the logic for the web scraper.
    """

    def __init__(self) -> None:
        self.base_url = "https://crinacle.com/rankings/"

    def clean_headers(self, headers: list) -> list:
        """
        Formats the table headers in snake case, code friendly format

        Args:
            headers (list): Contains the unformatted dirty table headers

        Returns:
            list: Returns properly formatted table headers
        """
        clean_headers = []

        for header in headers:
            # Remove unnecessary terms
            if "(" in header or "/" in header:
                header = header.split(" ")[0]

            # Rename header for conformity between both IEMS and headphones
            if "Setup" == header:
                header = "driver_type"

            # Convert to snake_case
            clean_headers.append(
                re.sub(r"(?<=[a-z])(?=[A-Z])|[^a-zA-Z]",
                       " ", header).replace(" ", "_").lower()
            )

        return clean_headers

    def scrape(self, device_type: str) -> list:
        """
            Scrapes Crinacle's databases containing technical information about Headphones and IEMs.
            Try to read the whole table to pandas

            Args:
                device_type (str): specifies the device type and url to be scraped.
        """
        url = self.base_url + device_type
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
        except requests.exceptions.RequestException as e:
            logging.log(msg=e, level=logging.ERROR)

        # Find all tables within page, in this case, the only one
        data_table = soup.findChildren("table")[0]

        # Get all the headers for the table
        thead = data_table.find_all("thead", recursive=False)
        headers = thead[0].findChildren("th")
        headers = [cell.text for cell in headers]
        headers = self.clean_headers(headers)

        # Get all rows within the table (excluding links)
        tbody = data_table.find_all("tbody", recursive=False)
        rows = tbody[0].find_all("tr", recursive=False)

        device_data = []

        for row in rows:
            row_data = {}
            for i, cell in enumerate(row.find_all("td", recursive=False)):
                row_data[headers[i]] = cell.get_text()
            device_data.append(row_data)

        return device_data

    def convert_to_csv(self, device_data: list, path: str) -> None:
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


if __name__ == "__main__":
    scraper = Scraper()
    headphones = scraper.scrape(device_type="headphones")
    iems = scraper.scrape(device_type="iems")

    scraper.convert_to_csv(
        device_data=headphones,
        path=os.getenv('PATH_TO_HEADPHONE_FILE'))

    scraper.convert_to_csv(
        device_data=iems,
        path=os.getenv('PATH_TO_IEMS_FILE'))
