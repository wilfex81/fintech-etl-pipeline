import pandas as pd
import csv

def write_csv(filepath, rows):
    if not rows:
        print(f"No data to write to {filepath}.")
        return

    # Create a DataFrame from the list of dictionaries
    # Note: Pandas automatically uses the dictionary keys as column names/headers
    df = pd.DataFrame(rows)

    # index=False removes the default row number column pandas adds
    # quoting=csv.QUOTE_NONNUMERIC quotes strings, leaves numerics unquoted
    df.to_csv(filepath, index=False, quoting=csv.QUOTE_NONNUMERIC)
    print(f"Data written to {filepath}.")