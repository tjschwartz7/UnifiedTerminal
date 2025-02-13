import zlib

# Define a function to compute CRC32 hash of a row
def compute_crc32(row):
    # Concatenate the values of the columns as a single string
    combined_str = ''.join(map(str, row))
    # Compute and return the CRC32 hash
    return zlib.crc32(combined_str.encode('utf-8'))