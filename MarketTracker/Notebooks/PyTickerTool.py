import pandas as pd
from datetime import datetime
import os
import shutil

import PyTableUtils as PTU


#Extract the csv file into a dataframe
def Load(ticker_name, enriched_fname):
    src = 'Raw/'
    dest = 'Enriched/'
    raw_src_path = src + ticker_name + '/'
    dest_ticker_path = dest + ticker_name + '/'
    raw_history_path = src + ticker_name + "/History/"
    enriched_file_path = dest + ticker_name + '/' + enriched_fname
    if not enriched_file_path.endswith('.parquet'):
        enriched_file_path = enriched_file_path + '.parquet'

    # Check if the destination directory exists, if not, create it
    if not os.path.exists(dest_ticker_path):
        os.makedirs(dest_ticker_path)
        
    # List all files in the source directory
    for file_name in os.listdir(raw_src_path):
        dataframe = pd.DataFrame()
        if file_name.endswith('.csv'):
            # Construct the full file paths
            source_file = os.path.join(raw_src_path, file_name)
            dest_file = os.path.join(raw_history_path, file_name)

            # Read the CSV file into a pandas DataFrame
            try:
                dataframe = pd.read_csv(source_file)
                print(f"File {file_name} loaded into DataFrame.")
                
            except Exception as e:
                print(f"Failed to read {file_name}: {e}")
                continue
            
            # Check if the destination directory exists, if not, create it
            if not os.path.exists(raw_history_path):
                os.makedirs(raw_history_path)
            
            # Move the file
            shutil.move(source_file, dest_file)
            print(f"Moved {file_name} to {raw_history_path}")
            #We only do this for one file, so we're done
            #At this stage, our csv file is loaded into dataframe
            #We can now begin loading the data into Enriched

            #Use pandas for initial transformations because its faster than spark
            #And easier to use in my opinion.
            dataframe = PTU.addCrcHash(dataframe)

            PTU.upsert_parquet(dataframe, enriched_file_path, key_columns=['CRC32'])


if __name__ == "__main__":
    Load('FNILX', "FNILX")
    Load('FRESX', "FRESX")
    Load('FSKAX', "FSKAX")
    Load('FSPSX', "FSPSX")
    Load('FSPTX', "FSPTX")
    Load('FXAIX', "FXAIX")
    Load('FZILX', "FZILX")
    Load('SPX', 'SPX')
    Load('DJI', 'DJI')
    Load('IXIC', 'IXIC')