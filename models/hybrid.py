# models/hybrid.py

from models.content_based import ContentBasedRecommender
from models.collaborative_filtering import CollaborativeFilteringRecommender
from models.context_aware import ContextAwareAdjuster
from models.clustering import ClusteringModel
from models.matrix_factorization import MatrixFactorizationRecommender
from data.preprocess import encode_product_tags
import pandas as pd


class HybridRecommender:
    """
    Hybrid recommender system that combines content-based filtering, collaborative filtering,
    clustering, and matrix factorization to generate personalized product recommendations.
    """

    def __init__(self, df_users, df_products, df_interactions, df_context):
        self.df_users = df_users
        self.df_products = df_products
        self.df_interactions = df_interactions
        self.df_context = df_context

        self.prepare_data()
        self.content_based = ContentBasedRecommender(self.df_products_encoded)
        self.collaborative_filtering = CollaborativeFilteringRecommender(self.user_item_matrix)
        self.context_aware = ContextAwareAdjuster(self.df_users, self.df_products_encoded, self.df_context)
        self.clustering_model = ClusteringModel(self.df_users, self.df_products_encoded, self.df_interactions)
        self.matrix_factorization = MatrixFactorizationRecommender(self.df_interactions)

        # Clustering
        self.clustering_model.cluster_users()
        self.clustering_model.cluster_products()
        self.df_users = self.clustering_model.df_users
        self.df_products_encoded = self.clustering_model.df_products_encoded

    def prepare_data(self):
        """
        Prepares the data by encoding product tags and creating the user interaction matrix.
        """

        self.df_products_encoded = encode_product_tags(self.df_products)

        self.df_interactions = pd.merge(
            self.df_interactions,
            self.df_products[['product_id', 'category']],
            on='product_id',
            how='left'
        )

        # Create user-item interaction matrix
        self.user_item_matrix = self.df_interactions.pivot_table(
            index='user_id',
            columns='product_id',
            values='weight',
            aggfunc='sum',
            fill_value=0
        )

    def recommend_products(self, user_id, top_n=3):
        user_interactions = self.df_interactions[self.df_interactions['user_id'] == user_id]
        user_products = set(user_interactions['product_id'])
        user_device = self.df_users[self.df_users['user_id'] == user_id]['device'].values[0]
        user_categories = user_interactions['category'].unique()

        # Check for cold start (new user)
        if user_interactions.empty:
            # Cold start for new user - Most common cluster
            most_common_cluster = self.df_users['cluster'].mode()[0]
            cluster_products = self.df_products_encoded[
                self.df_products_encoded['cluster'] == most_common_cluster
            ]['product_id'].tolist()

            # Recommend popular products in the cluster
            cluster_popular_products = self.df_interactions[
                self.df_interactions['product_id'].isin(cluster_products)
            ]['product_id'].value_counts().index.tolist()
            recommendations = cluster_popular_products[:top_n]
        else:
            # Use matrix factorization
            mf_recommendations = self.matrix_factorization.recommend_products(user_id, top_n=top_n)

            # Use collaborative filtering
            cf_recommendations = []
            similar_users = self.collaborative_filtering.get_similar_users(user_id)
            if similar_users:
                cf_recommendations = self.collaborative_filtering.recommend_products(user_id, top_n=top_n)

            # Include products from previously interacted categories
            category_products = list(
                self.df_products_encoded[
                    self.df_products_encoded['category'].isin(user_categories)
                ]['product_id']
            )

            # Use content-based recommendations
            cb_recommendations = []
            for product_id in user_products:
                similar_products = self.content_based.get_similar_products(product_id, top_n=top_n)
                cb_recommendations.extend(similar_products)

            # Use Cluster-based recommendations
            user_cluster = self.df_users.loc[self.df_users['user_id'] == user_id, 'cluster'].values[0]
            cluster_products = self.df_products_encoded[
                self.df_products_encoded['cluster'] == user_cluster
            ]['product_id'].tolist()

            # print(f"MF Recommendations for user {user_id}: {mf_recommendations}")
            # print(f"CF Recommendations for user {user_id}: {cf_recommendations}")
            # print(f"CB Recommendations for user {user_id}: {cb_recommendations}")
            # print(f"Category Products for user {user_id}: {category_products}")
            # print(f"Cluster Products for user {user_id}: {cluster_products}")

            # Define weights
            mf_weight = 0.5
            cf_weight = 0.3
            cb_weight = 0.15
            popularity_weight = 0.05
            product_scores = {}

            # Update product scores
            def update_scores(products, weight):
                for rank, pid in enumerate(products):
                    score = weight * (1 / (rank + 1))  
                    product_scores[pid] = product_scores.get(pid, 0) + score

            update_scores(mf_recommendations, mf_weight)
            update_scores(cf_recommendations, cf_weight)
            update_scores(cb_recommendations, cb_weight)
            update_scores(category_products, cb_weight)
            update_scores(cluster_products, cb_weight)

            # For cold start users, include popular products
            if user_interactions.empty:
                popular_products = self.df_interactions['product_id'].value_counts().index.tolist()
                update_scores(popular_products, popularity_weight)

            # Exclude products the user has already interacted with
            user_products = set(user_interactions['product_id'])
            for pid in user_products:
                product_scores.pop(pid, None)

            # Sort products
            sorted_products = sorted(product_scores.items(), key=lambda x: x[1], reverse=True)
            recommendations = [pid for pid, score in sorted_products][:top_n]
            recommendations = self.context_aware.adjust_for_context(user_id, recommendations)

            return recommendations

    def ensure_diversity(self, recommendations, top_n):
        diverse_recommendations = []
        categories = set()
        for pid in recommendations:
            category = self.df_products_encoded[self.df_products_encoded['product_id'] == pid]['category'].values[0]
            if category not in categories or len(categories) < top_n // 2:
                diverse_recommendations.append(pid)
                categories.add(category)
            if len(diverse_recommendations) >= top_n:
                break

        if len(diverse_recommendations) < top_n:
            remaining_pids = [pid for pid in recommendations if pid not in diverse_recommendations]
            diverse_recommendations.extend(remaining_pids[:top_n - len(diverse_recommendations)])
        return diverse_recommendations

    def get_recommendations(self, user_id, top_n=3):
        recommendations = self.recommend_products(user_id, top_n)
        return recommendations
