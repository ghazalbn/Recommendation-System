import pandas as pd
from datetime import datetime

def preprocess_timestamps(df, timestamp_col='timestamp'):
    df[timestamp_col] = pd.to_datetime(df[timestamp_col])
    df['day_of_week'] = df[timestamp_col].dt.day_name()
    df['hour'] = df[timestamp_col].dt.hour
    return df

def encode_product_tags(df_products):
    df_products = df_products.copy()
    df_products_exploded = df_products.explode('tags')

    # One-hot encode the tags
    df_product_tags = pd.get_dummies(df_products_exploded['tags'])
    df_product_tags['product_id'] = df_products_exploded['product_id']
    df_product_features = df_product_tags.groupby('product_id').sum().reset_index()
    df_products_merged = pd.merge(df_products, df_product_features, on='product_id', how='left')
    return df_products_merged
