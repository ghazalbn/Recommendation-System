import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

class ContentBasedRecommender:
    def __init__(self, df_products):
        self.df_products = df_products.reset_index(drop=True)
        self.product_ids = self.df_products['product_id']
        self.indices = pd.Series(self.df_products.index, index=self.df_products['product_id'])
        self.df_products['combined_metadata'] = self.df_products.apply(self.combine_metadata, axis=1)
        self.tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.df_products['combined_metadata'])
        self.cosine_sim_matrix = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)

    def combine_metadata(self, row):
        tags = ' '.join(row['tags']) if isinstance(row['tags'], list) else ''
        category = row['category']
        description = row.get('description', '')
        return f"{tags} {category} {description}"

    def create_tfidf_matrix(self, metadata_series):
        return self.tfidf_vectorizer.fit_transform(metadata_series)

    def get_similar_products(self, product_id, top_n=5):
        if product_id not in self.indices:
            self.add_new_product(product_id)
        idx = self.indices[product_id]
        sim_scores = list(enumerate(self.cosine_sim_matrix[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = [score for score in sim_scores if score[0] != idx][:top_n]
        similar_products = [self.product_ids.iloc[i[0]] for i in sim_scores]
        return similar_products

    def add_new_product(self, product_id):
        new_product = self.df_products[self.df_products['product_id'] == product_id]
        if new_product.empty:
            raise ValueError(f"Product ID {product_id} not found in the product DataFrame.")

        self.df_products = self.df_products.append(new_product, ignore_index=True)
        self.product_ids = self.df_products['product_id']
        self.indices = pd.Series(self.df_products.index, index=self.df_products['product_id'])
        self.df_products['combined_metadata'] = self.df_products.apply(self.combine_metadata, axis=1)
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.df_products['combined_metadata'])
        self.cosine_sim_matrix = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)
