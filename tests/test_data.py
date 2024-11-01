import pandas as pd

def get_test_data():
    # Users 
    df_users = pd.DataFrame({
        'user_id': [1, 2, 3, 4, 5],
        'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
        'device': ['mobile', 'desktop', 'mobile', 'desktop', 'mobile']
    })

    # Products
    df_products = pd.DataFrame({
        'product_id': [101, 102, 103, 104, 105, 106, 107, 108],
        'name': ['Wireless Earbuds', 'Smartphone Case', 'Yoga Mat', 'Electric Toothbrush',
                 'Laptop Stand', 'Gaming Mouse', 'Cookbook', 'Winter Jacket'],
        'category': ['Electronics', 'Accessories', 'Fitness', 'Personal Care',
                     'Office Supplies', 'Electronics', 'Books', 'Apparel'],
        'tags': [['wireless', 'audio'], ['phone', 'case'], ['fitness', 'exercise'],
                 ['personal care', 'electronics'], ['office', 'ergonomics'],
                 ['gaming', 'electronics'], ['cooking', 'recipes'], ['winter', 'clothing']],
        'rating': [4.5, 4.0, 4.7, 4.3, 4.2, 4.6, 4.8, 4.5]
    })

    # Interactions DataFrame
    df_interactions = pd.DataFrame({
        'user_id': [1, 1, 2, 2, 3, 4, 5],  # Added interaction for user_id=5
        'product_id': [101, 103, 102, 105, 103, 104, 101],  # user_id=5 interacts with product_id=101
        'weight': [5, 3, 4, 5, 2, 4, 1]
    })

    # Context 
    df_context = pd.DataFrame({
        'category': ['Electronics', 'Fitness', 'Books', 'Apparel'],
        'peak_days': [['Monday', 'Tuesday'], ['Wednesday'], ['Thursday'], ['Friday']],
        'season': ['All Year', 'All Year', 'Holiday', 'Winter']
    })

    return df_users, df_products, df_interactions, df_context
