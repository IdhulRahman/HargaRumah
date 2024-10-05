import pandas as pd

def load_data(csv_file):
    """Load data from CSV file."""
    return pd.read_csv(csv_file)
