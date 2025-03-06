# This module contains the function to read URLs from an Excel file.

import pandas as pd

def read_urls_from_excel(uploaded_file):
    """
    Read the provided Excel file into a DataFrame and extract the 'URL' column.
    """
    df = pd.read_excel(uploaded_file)
    return df['URL'].tolist()
