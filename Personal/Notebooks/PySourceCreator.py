import pandas as pd
from datetime import datetime
import os
import shutil

import PyTableUtils as PTU


#Extract the csv file into a dataframe
def Load(name, cols):
    cols = cols + ['CRC32']
    dest = 'Enriched/'
    enriched_dest_path = dest + name + '/'

    # Check if the destination directory exists, if not, create it
    if not os.path.exists(enriched_dest_path):
        os.makedirs(enriched_dest_path)

    dataframe = pd.DataFrame(columns=cols)

    # Construct the full file paths
    dest_file = os.path.join(enriched_dest_path, name+".parquet")
    if not os.path.exists(dest_file):
        dataframe.to_parquet(dest_file)


if __name__ == "__main__":
    Load('Goals', cols=['Name', 'Date', 'Description'])
    Load('Parts', cols=['Name', 'Date', 'Description'])
    Load('Emotions', cols=['Name', 'Physical Manifestations'])
    Load('FeelingTracker', cols=['Emotion Name', 'Date', 'Description'])
    Load('Needs', cols=['Name', 'Date', 'Description'])
    Load('Likes', cols=['Name', 'Date', 'Description'])
    Load('Boundaries', cols=['Name', 'Date', 'Description'])
