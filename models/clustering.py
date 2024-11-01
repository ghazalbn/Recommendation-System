from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import numpy as np

class ClusteringModel:
    def __init__(self, df_users, df_products_encoded, df_interactions):
        self.df_users = df_users
        self.df_products_encoded = df_products_encoded
        self.df_interactions = df_interactions

    def cluster_users(self, n_clusters=3):
        # Use user interaction data to cluster users
        interaction_matrix = self.df_interactions.pivot_table(
            index='user_id',
            columns='product_id',
            values='weight',
            aggfunc='sum',
            fill_value=0
        )
        print(f"Interaction matrix shape: {interaction_matrix.shape}")
        if interaction_matrix.empty:
            print("No interaction data available for clustering users.")
            return

        # Reduce dimensionality
        n_samples, n_features = interaction_matrix.shape
        n_components = min(n_samples, n_features, 10)
        if n_components > 1:
            pca = PCA(n_components=n_components - 1)
            interaction_matrix_reduced = pca.fit_transform(interaction_matrix)
        else:
            interaction_matrix_reduced = interaction_matrix.values
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        self.user_clusters = kmeans.fit_predict(interaction_matrix_reduced)
        self.df_users['cluster'] = self.user_clusters
    
    def cluster_products(self, n_clusters=3):
        product_features = self.df_products_encoded.drop(
            ['product_id', 'name', 'category', 'rating', 'tags', 'cluster'], 
            axis=1, 
            errors='ignore'
        )
        # Only numeric columns 
        product_features = product_features.select_dtypes(include=[np.number])
        if product_features.empty:
            print("No features available for clustering products.")
            return
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        self.product_clusters = kmeans.fit_predict(product_features)
        self.df_products_encoded['cluster'] = self.product_clusters
