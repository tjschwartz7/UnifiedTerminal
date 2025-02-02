import pandas as pd
from datetime import datetime
import os
import shutil

import PyTableUtils as PTU
#from deltalake import DeltaTable
from pyspark.sql import SparkSession
from delta.tables import DeltaTable

RAW_SRC_PATH = "Raw/"
RAW_HISTORY_PATH = RAW_SRC_PATH+'History/'

ENRICHED_DELTA_PATH = 'Enriched/Citi/'
ENRICHED_DELTA_FILE_NAME = 'CitiTable.parquet'
ENRICHED_DELTA_FILE_PATH = ENRICHED_DELTA_PATH + ENRICHED_DELTA_FILE_NAME


#Extract the csv file into a dataframe
def Load():
    dataframe = pd.DataFrame()
    # List all files in the source directory
    for file_name in os.listdir(RAW_SRC_PATH):
        if file_name.endswith('.csv'):
            # Construct the full file paths
            source_file = os.path.join(RAW_SRC_PATH, file_name)
            dest_file = os.path.join(RAW_HISTORY_PATH, file_name)

            # Read the CSV file into a pandas DataFrame
            try:
                dataframe = pd.read_csv(source_file)
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

    #.config("spark.jars.packages", "io.delta:delta-core_2.12:1.0.0") \
    #.config("hadoop.home.dir", " C:/Users/tjsch/AppData/Local/Programs/Python/Python311/Lib/site-packages") \

    # Initialize Spark session
    spark = SparkSession.builder \
        .appName("DeltaCheckCreate") \
        .getOrCreate()


    # Check if the Delta table exists at the specified path
    if not os.path.exists(ENRICHED_DELTA_FILE_PATH):
        print(f"Delta table does not exist at {ENRICHED_DELTA_FILE_PATH}. Creating an empty Delta table.")
        
        spark.sql(
            f"""
            CREATE TABLE IF NOT EXISTS citi (
                Status STRING NOT NULL,
                Date DATE NOT NULL,
                Description STRING NOT NULL,
                Debit FLOAT NOT NULL,
                Credit FLOAT NOT NULL,
                CRC32 STRING NOT NULL
            )
            USING PARQUET
            LOCATION '{ENRICHED_DELTA_PATH}';
            """
        )
        
        
        # Load the newly created empty Delta table
        delta_table_dest = DeltaTable.forPath(spark, ENRICHED_DELTA_PATH)
        print(f"Empty Delta table created at {ENRICHED_DELTA_PATH}.")
    else:
        # If the Delta table exists, load it
        delta_table_dest = DeltaTable.forPath(spark, ENRICHED_DELTA_PATH)
        print(f"Delta table already exists at {ENRICHED_DELTA_PATH}.")


    delta_table_src = DeltaTable.from_pandas(dataframe)

     # Perform the merge operation
    delta_table_dest.alias("target").merge(
        delta_table_src.alias("source"),
        "target.CRC32 = source.CRC32"  # Merge condition on CRC32 column
    ).whenMatchedUpdate(
        condition="target.CRC32 = source.CRC32",  # Update only if CRC32 matches
        set={
            "Debit": "source.Debit",
            "Credit": "source.Credit",
            "Description": "source.Description",
            "Date": "source.Date",
            "Status": "source.Status"
        }
    ).whenNotMatchedInsert(
        values={
            "Debit": "source.Debit",
            "Credit": "source.Credit",
            "Description": "source.Description",
            "Date": "source.Date",
            "Status": "source.Status",
            "CRC32": "source.CRC32"
        }
    ).execute()

    delta_table_dest.toDF().show()


if __name__ == "__main__":
    Load()