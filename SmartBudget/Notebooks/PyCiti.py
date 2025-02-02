import pandas as pd
from datetime import datetime
import os
import shutil
from pyspark.sql import SparkSession
import PyTableUtils as PTU

from deltalake import DeltaTable

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



    # Check if the Delta table exists
    if not os.path.exists(ENRICHED_DELTA_FILE_PATH):
        print(f"Delta table does not exist at {ENRICHED_DELTA_FILE_PATH}. Creating an empty Delta table.")
        
        # Initialize Spark session
        spark = SparkSession.builder \
            .appName("DeltaCheckCreate") \
            .getOrCreate()

        # Define an empty schema for the Delta table (adjust to your needs)
        from pyspark.sql.types import StructType, StructField, StringType, FloatType, DateType
        schema = StructType([
            StructField("Status", StringType(), False),
            StructField("Date", DateType(), False),
            StructField("Description", StringType(), False),
            StructField("Debit", FloatType(), False),
            StructField("Credit", FloatType(), False),
            StructField("CRC32", StringType(), False)
        ])

        # Create an empty DataFrame with the schema
        empty_df = spark.createDataFrame(spark.sparkContext.emptyRDD(), schema)
        
        # Write the empty DataFrame to the Delta table path
        empty_df.write.format("delta").save(ENRICHED_DELTA_FILE_PATH)
        
        # Load the newly created empty Delta table
        delta_table_dest = DeltaTable(ENRICHED_DELTA_FILE_PATH)
        print(f"Empty Delta table created at {ENRICHED_DELTA_FILE_PATH}.")
        spark.stop()
    else:
        delta_table_dest = DeltaTable(ENRICHED_DELTA_FILE_PATH)

    delta_table_dest = DeltaTable(ENRICHED_DELTA_FILE_PATH)
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