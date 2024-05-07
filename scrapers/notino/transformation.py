import pandas as pd
from datetime import datetime

class NotinoTransformation:
    def __init__(self, country: str, retailer: str):
        self.country = country
        self.retailer = retailer

    # implement any methods you need to transform the scraped data

    # add to the scraped data at least these columns:
    # - country
    # - currency
    # - scraped_at (date and time when the data was scraped)

    # ensure that price and price_after_sale columns are in float format
    # add discount amount column with the discount (float)

    def transform_data(self, raw_df: pd.DataFrame) -> pd.DataFrame:
        transformed_df = raw_df.copy()
        
        transformed_df['country'] = self.country
        transformed_df['currency'] = 'gbp/£'
        transformed_df['scraped_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Price stuff
        transformed_df['price'] = transformed_df['price'].astype(float)
        transformed_df['price_after_sale'] = round(transformed_df['price'] - (transformed_df['price'] * (transformed_df['discount_value'] / 100)), 2)
        transformed_df['discount_amount'] = round(transformed_df['price'] - transformed_df['price_after_sale'], 2)

        # Re-order (looks better)
        columns = transformed_df.columns.tolist()
        columns.insert(4, columns.pop(columns.index('currency')))
        columns.insert(8, columns.pop(columns.index('price_after_sale')))
        columns.insert(9, columns.pop(columns.index('discount_amount')))
        transformed_df = transformed_df.reindex(columns=columns)

        return transformed_df

def main(raw_df: pd.DataFrame, country: str, retailer: str):
    transformation = NotinoTransformation(country=country, retailer=retailer)
    transformed_df = transformation.transform_data(raw_df)
    return transformed_df

if __name__ == "__main__":
    raw_df = pd.read_csv("notino_raw.csv")
    transformed_df = main(raw_df, country="uk", retailer="notino")
    transformed_df.to_csv("notino_transformed.csv", index=False)