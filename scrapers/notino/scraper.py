# import any libraries you want
import pandas as pd
import json
from datetime import datetime
from bs4 import BeautifulSoup

from abstract.abstract_scraper import AbstractScraper

class NotinoScraper(AbstractScraper):
    # implement scraper for notino - toothpastes
    # choose any Notino website your prefer (they operates in 28 countries) 
    # https://www.notino.cz/zubni-pasty/ // https://www.notino.co.uk/toothpaste/ // https://www.notino.de/zahnpasten/ ...

    # to each product get at least (but the more, the better) these data:
    # - product name
    # - brand
    # - price
    # - price after sale (if any)
    # - promocode (if any)
    # - url
    # - image

    # place for your code here...

    def __init__(self, retailer, country):
        super().__init__(retailer, 'notino')
        super().__init__(country, 'uk')
        self.url = 'https://www.notino.co.uk/toothpaste/'

    def notino_req(self, page: int, headers: dict) -> dict:
        response = self.send_get_request(self.url + f'?npc={page}', headers=headers)
        if response is None:
            self.logger.error("Failed to fetch page")
            return None

        soup = BeautifulSoup(response.text, 'html.parser')
        if not soup:
            self.logger.error("Failed to create soup")
            return None

        json_data_raw = soup.find('script', {'type': 'application/json', 'id': 'navigation-fragment-state'})
        if not json_data_raw:
            self.logger.error("Script tag is missing")
            return None

        try:
            json_data = json.loads(json_data_raw.get_text())
        except json.JSONDecodeError:
            self.logger.error("Failed to parse json data")
            return None
        
        return json_data

    def scrape(self):
        # Most common headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/html, application/xhtml+xml, application/xml;q=0.9, image/webp, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-GB,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,en-US;q=0.6,cs-CZ;q=0.5,cs;q=0.4',
            'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json; charset=UTF-8'
        }

        # Pagination
        json_data = self.notino_req(0, headers)
        if not json_data:
            return None
        
        last_page = json_data.get('fragmentContextData', {}).get('DataContextProvider', {}).get('listing', {}).get('numberOfPages', 0)

        # I eventually found that all the items in a category can be 
        # found by accessing the last page of the list directly
        json_data = self.notino_req(last_page + 1, headers)
        if not json_data:
            return None
        
        products = json_data.get('fragmentContextData', {}).get('DataContextProvider', {}).get('listing', {}).get('products', [])
            
        print(f'Products in total: {len(products)}')

        # Extracting essential data
        essential_data = []
        for item in products:
            item_data = {
                'id': item.get('id', '####'),
                'name': item.get('name', ''),
                'brand': item.get('brandName', ''),
                'price': item.get('priceInformation', {}).get('price', ''),
                'has_discount': item.get('promotionData', {}).get('isDiscount', False),
                'promocode': item.get('promotionData', {}).get('voucherCode', ''),
                'discount_value': item.get('promotionData', {}).get('discountValue', 0.0),
                'url': item.get('url', ''),
                'img': item.get('imageUrl', ''),
                'scraped_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            essential_data.append(item_data)

        df = pd.DataFrame(essential_data)
        return df

def main(retailer: str, country: str) -> pd.DataFrame:
    scraper = NotinoScraper(retailer=retailer, country=country)
    products_df = scraper.scrape()
    return products_df

if __name__ == "__main__":
    df_raw = main(retailer="notino", country="uk")
    if df_raw is None:
        print("Failed to scrape data")
    else:
        df_raw.to_csv("notino_raw.csv", index=False)