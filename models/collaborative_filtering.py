import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from joblib import Parallel, delayed

class CollaborativeFilteringRecommender:
    def __init__(self, user_item_matrix):
        self.user_item_matrix = user_item_matrix
        self.user_similarity_df = self.compute_user_similarity()

    def compute_user_similarity(self):
        user_similarity = cosine_similarity(self.user_item_matrix)
        user_similarity_df = pd.DataFrame(
            user_similarity, 
            index=self.user_item_matrix.index, 
            columns=self.user_item_matrix.index
        )
        return user_similarity_df

    def get_similar_users(self, user_id, top_n=3):
        if user_id not in self.user_similarity_df.index:
            return []
        # Check if the user has interactions
        if self.user_item_matrix.loc[user_id].sum() == 0:
            return []
        sim_users = self.user_similarity_df[user_id].sort_values(ascending=False)
        sim_users = sim_users[sim_users > 0]  
        sim_users = sim_users.index.tolist()
        sim_users = [uid for uid in sim_users if uid != user_id][:top_n]
        return sim_users

    def recommend_products(self, user_id, top_n=5):
        similar_users = self.get_similar_users(user_id, top_n=top_n)
        if not similar_users:
            return []
        # Get products that similar users interacted with
        similar_users_interactions = self.user_item_matrix.loc[similar_users]
        # Sum the interactions to get a score for each product
        product_scores = similar_users_interactions.sum().sort_values(ascending=False)
        user_products = set(self.user_item_matrix.loc[user_id][self.user_item_matrix.loc[user_id] > 0].index)
        recommended_products = [pid for pid in product_scores.index if pid not in user_products]
        return recommended_products[:top_n]
