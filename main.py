import pandas as pd
from tqdm import tqdm
import requests
from bs4 import BeautifulSoup
from src.utils import current_time

def get_quotes_data(num_of_page):

    # list to store all extracted data
    full_data = []

    for page in tqdm(range(1, num_of_page)):
        resp = requests.get(f"https://quotes.toscrape.com/page/{page}")

        soup = BeautifulSoup(resp.text, "html.parser")

        raw_data = soup.find_all("div", class_ = "quote")

        for data in raw_data:
            # extract quotes data
            quotes = data.find("span").text

            # extract author data
            author = data.find("small").text

            # get tags data
            tags = data.find_all("a", class_ = "tag")

            # create empty list for store all tag value
            get_tag = []

            # iterate tag in each quotes card
            for tag in tags:
                # store the tag value
                get_tag.append(tag.text)

            data = {
                "quote": quotes,
                "author": author,
                "tags": get_tag,
                "scrapped_at": current_time()
            }

            full_data.append(data)

    return full_data
    
def save_output(data, filename):
    data = pd.DataFrame(data)

    data.to_csv(filename, index = False)

    print(f"Data berhasil disimpan dengan nama file {filename}")

if __name__ == "__main__":

    OUTPUT_DIR = "data/"

    print("=========== Start Scrape Data ===========")
    
    # 1. start scrape data
    quote_data = get_quotes_data(num_of_page = 10)

    # 2. save the scrape output
    save_output(data = quote_data,
                filename = OUTPUT_DIR + "dev_quote_data.csv")
    
    print("=========== End Scrape Data ===========")