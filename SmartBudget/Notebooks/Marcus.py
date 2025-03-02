import pandas as pd
from datetime import datetime
import os
import shutil

import PyTableUtils as PTU

RAW_SRC_PATH = "Raw/Marcus/"
RAW_HISTORY_PATH = RAW_SRC_PATH+'History/'

ENRICHED_PATH = 'Enriched/Marcus/'
ENRICHED_FILE_NAME = 'MarcusTable.parquet'
ENRICHED_FILE_PATH = ENRICHED_PATH + ENRICHED_FILE_NAME


#Extract the csv file into a dataframe
def Load():
    dataframe = pd.DataFrame()

    # Check if the destination directory exists, if not, create it
    if not os.path.exists(ENRICHED_PATH):
        os.makedirs(ENRICHED_PATH)

    # List all files in the source directory
    for file_name in os.listdir(RAW_SRC_PATH):
        if file_name.endswith('.xlsx'):
            # Construct the full file paths
            source_file = os.path.join(RAW_SRC_PATH, file_name)
            dest_file = os.path.join(RAW_HISTORY_PATH, file_name)

            # Read the CSV file into a pandas DataFrame
            try:
                dataframe = pd.read_excel(source_file)
                print(f"File {file_name} loaded into DataFrame.")
                
                # Optionally, print the first few rows of the DataFrame
                print(dataframe.head())
                
            except Exception as e:
                print(f"Failed to read {file_name}: {e}")
                continue
            
            # Check if the destination directory exists, if not, create it
            if not os.path.exists(RAW_HISTORY_PATH):
                os.makedirs(RAW_HISTORY_PATH)
            
            # Move the file
            shutil.move(source_file, dest_file)
            print(f"Moved {file_name} to {RAW_HISTORY_PATH}")
            #We only do this for one file, so we're done
            break

    #At this stage, our csv file is loaded into dataframe
    #We can now begin loading the data into Enriched

    #Use pandas for initial transformations because its faster than spark
    #And easier to use in my opinion.
    dataframe = PTU.addCrcHash(dataframe)

    PTU.upsert_parquet(dataframe, ENRICHED_FILE_PATH, key_columns=['CRC32'])


if __name__ == "__main__":
    Load()