import pandas as pd

def load_users():
    users = [
        {"user_id": 1, "name": "Alice", "location": "New York", "device": "mobile"},
        {"user_id": 2, "name": "Bob", "location": "Los Angeles", "device": "desktop"},
        {"user_id": 3, "name": "Charlie", "location": "Chicago", "device": "mobile"},
        {"user_id": 4, "name": "Diana", "location": "San Francisco", "device": "desktop"},
        {"user_id": 5, "name": "Eve", "location": "Boston", "device": "mobile"},  # Cold start user
        {"user_id": 6, "name": "Frank", "location": "Seattle", "device": "desktop"},
    ]
    return pd.DataFrame(users)

def load_products():
    products = [
        {"product_id": 101, "name": "Wireless Earbuds", "category": "Electronics", "tags": ["audio", "wireless", "Bluetooth"], "rating": 4.5},
        {"product_id": 102, "name": "Smartphone Case", "category": "Accessories", "tags": ["phone", "protection", "case"], "rating": 4.2},
        {"product_id": 103, "name": "Yoga Mat", "category": "Fitness", "tags": ["exercise", "mat", "yoga"], "rating": 4.7},
        {"product_id": 104, "name": "Electric Toothbrush", "category": "Personal Care", "tags": ["hygiene", "electric", "toothbrush"], "rating": 4.3},
        {"product_id": 105, "name": "Laptop Stand", "category": "Office Supplies", "tags": ["work", "laptop", "stand"], "rating": 4.6},
        {"product_id": 106, "name": "Gaming Mouse", "category": "Electronics", "tags": ["gaming", "mouse", "accessory"], "rating": 4.8},
        {"product_id": 107, "name": "Cookbook", "category": "Books", "tags": ["cooking", "recipes", "food"], "rating": 4.9},
        {"product_id": 108, "name": "Winter Jacket", "category": "Apparel", "tags": ["clothing", "winter", "jacket"], "rating": 4.5},
    ]
    return pd.DataFrame(products)


def load_browsing_history():
    browsing_history = [
        {"user_id": 1, "product_id": 101, "timestamp": "2023-10-01 10:00:00", "event": "view", "time_spent": 5},
        {"user_id": 1, "product_id": 103, "timestamp": "2023-10-01 10:05:00", "event": "click", "time_spent": 2},
        {"user_id": 2, "product_id": 102, "timestamp": "2023-10-02 11:30:00", "event": "add_to_cart", "time_spent": 3},
        {"user_id": 3, "product_id": 104, "timestamp": "2023-10-03 14:20:00", "event": "view", "time_spent": 4},
        {"user_id": 4, "product_id": 105, "timestamp": "2023-10-04 16:45:00", "event": "click", "time_spent": 6},
        {"user_id": 5, "product_id": 107, "timestamp": "2023-10-05 09:15:00", "event": "view", "time_spent": 2},
        {"user_id": 6, "product_id": 108, "timestamp": "2023-10-06 20:30:00", "event": "view", "time_spent": 5},
        {"user_id": 2, "product_id": 106, "timestamp": "2023-10-07 13:00:00", "event": "click", "time_spent": 4},
    ]
    return pd.DataFrame(browsing_history)


def load_purchase_history():
    purchase_history = [
        {"user_id": 1, "product_id": 104, "quantity": 1, "timestamp": "2023-10-10 15:20:00"},
        {"user_id": 2, "product_id": 105, "quantity": 2, "timestamp": "2023-10-12 12:00:00"},
        {"user_id": 3, "product_id": 103, "quantity": 1, "timestamp": "2023-10-15 09:30:00"},
        {"user_id": 4, "product_id": 101, "quantity": 1, "timestamp": "2023-10-16 10:15:00"},
        {"user_id": 6, "product_id": 106, "quantity": 1, "timestamp": "2023-10-17 18:45:00"},
    ]
    return pd.DataFrame(purchase_history)

def load_contextual_signals():
    contextual_signals = [
        {"category": "Electronics", "peak_days": ["Friday", "Saturday"], "season": "Holiday"},
        {"category": "Fitness", "peak_days": ["Monday", "Wednesday"], "season": "Summer"},
        {"category": "Office Supplies", "peak_days": ["Tuesday", "Thursday"], "season": "Back-to-School"},
        {"category": "Personal Care", "peak_days": ["Sunday"], "season": "All Year"},
        {"category": "Books", "peak_days": ["Saturday", "Sunday"], "season": "All Year"},
        {"category": "Apparel", "peak_days": ["Wednesday", "Friday"], "season": "Winter"},
    ]
    return pd.DataFrame(contextual_signals)
