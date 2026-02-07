import pandas as pd

def preprocess_data(df):
    # Example preprocessing
    df['weather'] = df['weather'].map({'Sunny': 0, 'Rainy': 1, 'Cloudy': 2})
    return df
