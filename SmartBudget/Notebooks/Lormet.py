import pandas as pd
from datetime import datetime
import os
import shutil

import PyTableUtils as PTU
#from deltalake import DeltaTable
from pyspark.sql import SparkSession
from delta.tables import DeltaTable

RAW_SRC_PATH = "Raw/Lormet/"
RAW_SRC_SAVINGS_PATH = "Raw/Lormet/Savings/"
RAW_SRC_CHECKING_PATH = "Raw/Lormet/Checking/"
RAW_HISTORY_PATH = RAW_SRC_PATH+'History/'
RAW_FILE_EXTENSION = ".csv"
ENRICHED_PATH = 'Enriched/Lormet/'
ENRICHED_FILE_NAME = 'LormetTable.parquet'
ENRICHED_FILE_PATH = ENRICHED_PATH + ENRICHED_FILE_NAME

COLUMNS = ["Date", "Description", "Amount", "Balance"]

#Extract the csv file into a dataframe
def Load():
    dataframe = pd.DataFrame()

    # Check if the destination directory exists, if not, create it
    if not os.path.exists(ENRICHED_PATH):
        os.makedirs(ENRICHED_PATH)
        
    #First, we handle the SAVINGS path
    # List all files in the source directory
    for file_name in os.listdir(RAW_SRC_SAVINGS_PATH):
        if file_name.endswith(RAW_FILE_EXTENSION):
            # Construct the full file paths
            source_file = os.path.join(RAW_SRC_SAVINGS_PATH, file_name)
            dest_file = os.path.join(RAW_HISTORY_PATH, file_name)

            # Read the CSV file into a pandas DataFrame
            try:
                dataframe = pd.read_csv(source_file, header=None, skip_blank_lines=True, na_values=["", " "])
                dataframe = dataframe.dropna(axis=1, how='all')
                dataframe.columns = COLUMNS
                print(f"File {file_name} loaded into DataFrame.")
                
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

            dataframe['Account Type'] = 'Savings'
            break



    #At this stage, our csv file is loaded into dataframe
    #We can now begin loading the data into Enriched

    #Use pandas for initial transformations because its faster than spark
    #And easier to use in my opinion.
    dataframe = PTU.addCrcHash(dataframe)
    PTU.upsert_parquet(dataframe, ENRICHED_FILE_PATH, key_columns=['CRC32'])

    #Start over
    dataframe = pd.DataFrame()

    #Rather than concat the data into the dataframe then upsert
    #We do each dataframe one at a time and upsert twice.
    #Why? Laziness.
    #Handle checkings
    # List all files in the source directory
    for file_name in os.listdir(RAW_SRC_CHECKING_PATH):
        if file_name.endswith(RAW_FILE_EXTENSION):
            # Construct the full file paths
            source_file = os.path.join(RAW_SRC_CHECKING_PATH, file_name)
            dest_file = os.path.join(RAW_HISTORY_PATH, file_name)

            # Read the CSV file into a pandas DataFrame
            try:
                dataframe = pd.read_csv(source_file, header=None, skip_blank_lines=True, na_values=["", " "])
                dataframe = dataframe.dropna(axis=1, how='all')
                dataframe.columns = COLUMNS
                print(f"File {file_name} loaded into DataFrame.")
                
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

            dataframe['Account Type'] = 'Checking'
            break

    dataframe = PTU.addCrcHash(dataframe)
    PTU.upsert_parquet(dataframe, ENRICHED_FILE_PATH, key_columns=['CRC32'])


if __name__ == "__main__":
    Load()