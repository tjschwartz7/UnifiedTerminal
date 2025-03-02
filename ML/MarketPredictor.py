import tensorflow as tf
import pandas as pd

PATH = "../MarketTracker/Curated/FidelityTickers/FidelityTickers.parquet"

if __name__ == '__main__':
    marketDF = pd.read_parquet(PATH)

    dataset = tf.data.Dataset.from_tensor_slices(dict(marketDF))

    