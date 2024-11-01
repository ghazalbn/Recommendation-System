from data.load_data import *
from data.preprocess import preprocess_timestamps, encode_product_tags
from utils.helpers import assign_interaction_weights
from models.hybrid import HybridRecommender
from utils.explainability import Explainability
from utils.caching import CacheManager
import pandas as pd

def main():
    # Load data
    df_users = load_users()
    df_products = load_products()
    df_browsing = load_browsing_history()
    df_purchase = load_purchase_history()
    df_context = load_contextual_signals()

    # Preprocess data
    df_browsing = preprocess_timestamps(df_browsing)
    df_purchase = preprocess_timestamps(df_purchase)

    # Merge interactions
    df_browsing["event"] = "view"
    df_purchase["event"] = "purchase"
    df_interactions = pd.concat([df_browsing, df_purchase], ignore_index=True)
    df_interactions = assign_interaction_weights(df_interactions)

    # Initialize recommender
    hybrid_recommender = HybridRecommender(
        df_users, df_products, df_interactions, df_context
    )

    explainability = Explainability(
        df_users,
        df_products,
        hybrid_recommender.df_interactions,  
        hybrid_recommender.collaborative_filtering,
    )

    # Cache
    cache_manager = CacheManager()

    # List of users to test
    users_to_test = [
        {"user_id": 1, "description": "Existing user with rich interaction history (Alice)"},
        {"user_id": 2, "description": "Existing user with rich interaction history (Bob)"},
        {"user_id": 5, "description": "Cold start user (Eve)"},
        {"user_id": 6, "description": "User testing contextual recommendations (Frank)"},
    ]

    # Test recommendations for each user
    for user in users_to_test:
        user_id = user["user_id"]
        print(f"\nRecommendations for User {user_id} ({user['description']}):")

        # Get recommendations for the user
        recommendations = hybrid_recommender.get_recommendations(user_id)

        # Explain recommendations
        explanations = explainability.explain_recommendations(user_id, recommendations)

        # Output recommendations
        for product_id in recommendations:
            product_name = df_products[df_products["product_id"] == product_id]["name"].values[0]
            reasons = explanations.get(product_id, [])
            print(f"- {product_name} (Product ID: {product_id})")
            print(f"  Reasons: {', '.join(reasons) if reasons else 'No specific reason'}")

        # Cache recommendations
        cache_manager.cache_recommendations(user_id, recommendations)

    # Testing recommendations for a new product
    print("\n--- Testing Recommendations with a New Product Added ---")

    new_product = {
        "product_id": 109,
        "name": "Wireless Charger",
        "category": "Electronics",
        "tags": ["wireless", "charger", "accessory"],
        "rating": 4.7,
    }

    pd.concat([df_products, pd.DataFrame([new_product])], ignore_index=True)
    hybrid_recommender = HybridRecommender(
        df_users, df_products, df_interactions, df_context
    )

    explainability = Explainability(
        df_users,
        df_products,
        hybrid_recommender.df_interactions,
        hybrid_recommender.collaborative_filtering,
    )

    user_id = 2  # Bob
    print(f"\nRecommendations for User {user_id} after adding new product:")

    recommendations = hybrid_recommender.get_recommendations(user_id)
    explanations = explainability.explain_recommendations(user_id, recommendations)

    for product_id in recommendations:
        product_name = df_products[df_products["product_id"] == product_id]["name"].values[0]
        reasons = explanations.get(product_id, [])
        print(f"- {product_name} (Product ID: {product_id})")
        print(f"  Reasons: {', '.join(reasons) if reasons else 'No specific reason'}")

    cache_manager.cache_recommendations(user_id, recommendations)


if __name__ == "__main__":
    main()