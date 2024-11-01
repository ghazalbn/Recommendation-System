class Explainability:
    def __init__(self, df_users, df_products, df_interactions, collaborative_model):
        self.df_users = df_users
        self.df_products = df_products
        self.df_interactions = df_interactions
        self.collaborative_model = collaborative_model

    def explain_recommendations(self, user_id, recommendations):
        explanations = {}
        user_interactions = self.df_interactions[self.df_interactions['user_id'] == user_id]
        user_products = set(user_interactions['product_id'])
        if user_interactions.empty:
            similar_users = []
        else:
            similar_users = self.collaborative_model.get_similar_users(user_id)
        similar_users_products = set(
            self.df_interactions[self.df_interactions['user_id'].isin(similar_users)]['product_id']
        ) if similar_users else set()

        for product_id in recommendations:
            reasons = []
            # For cold start users
            if user_interactions.empty:
                reasons.append("Popular among all users")
            else:
                # Add explanation if there are similar users
                if similar_users and product_id in similar_users_products:
                    reasons.append("Users similar to you purchased this")

                # Content-based explanation
                product_tags = self.df_products[self.df_products['product_id'] == product_id]['tags'].values
                if len(product_tags) > 0:
                    product_tags = product_tags[0]
                    for tag in product_tags:
                        for up in user_products:
                            up_tags = self.df_products[self.df_products['product_id'] == up]['tags'].values
                            if len(up_tags) > 0:
                                up_tags = up_tags[0]
                                if tag in up_tags:
                                    reasons.append(f"Because you showed interest in {tag} products")
                                    break

                # Category-based explanation
                if 'category' in user_interactions.columns:
                    product_category = self.df_products[self.df_products['product_id'] == product_id]['category'].values[0]
                    if product_category in user_interactions['category'].unique():
                        reasons.append(f"Because you interacted with {product_category} products")

            # If no reasons, mark as popular product
            if not reasons:
                reasons.append("Popular product")

            explanations[product_id] = list(set(reasons)) 
        return explanations
