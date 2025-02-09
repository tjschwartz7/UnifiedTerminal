import pandas as pd
from datetime import datetime
import os


SRC_ENRICHED_PATH = "Enriched/"
DEST_CURATED_PATH = 'Curated/FidelityTickers/'


COLUMNS=['Date', 'Open', 'High', 'Low', 'Close', '% Change', '% Change vs Average', 'Volume', 'Ticker Name', 'CRC32']

def Transform(tickers):

    curated_df = pd.DataFrame(columns=COLUMNS)
    # Check if the destination directory exists, if not, create it
    if not os.path.exists(DEST_CURATED_PATH):
        os.makedirs(DEST_CURATED_PATH)

    for ticker in tickers:
        enriched_src_path = SRC_ENRICHED_PATH + ticker + '/' + ticker + '.parquet'
        ticker_df = pd.read_parquet(enriched_src_path)
        ticker_df['Ticker Name'] = ticker
        curated_df = pd.concat([curated_df, ticker_df], axis=0, ignore_index=True)
    curated_df.to_parquet(DEST_CURATED_PATH + 'FidelityTickers.parquet')




if __name__ == "__main__":
    Transform(tickers=['FNILX', 'FRESX', 'FSKAX', 'FSPSX', 'FSPTX', 'FXAIX', 'FZILX', 'SPX', 'DJI', 'IXIC'])


