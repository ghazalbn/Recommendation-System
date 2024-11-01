from surprise import Dataset, Reader, SVD
import pandas as pd

class MatrixFactorizationRecommender:
    def __init__(self, df_interactions):
        reader = Reader(rating_scale=(1, 5))
        data = Dataset.load_from_df(df_interactions[['user_id', 'product_id', 'weight']], reader)
        self.trainset = data.build_full_trainset()
        # Train SVD model
        self.model = SVD()
        self.model.fit(self.trainset)
    
    def predict(self, user_id, product_id):
        return self.model.predict(user_id, product_id)
    
    def recommend_products(self, user_id, top_n=5):
        # Check if the user exists in the training set
        try:
            user_inner_id = self.trainset.to_inner_uid(user_id)
        except ValueError:
            # User is unknown - handle cold start
            return []

        # Get the items rated by the user
        user_rated_items = set(
            [self.trainset.to_raw_iid(iid) for (iid, _) in self.trainset.ur[user_inner_id]]
        )

        all_items = self.trainset.all_items()
        all_product_ids = [self.trainset.to_raw_iid(iid) for iid in all_items]
        items_to_predict = [iid for iid in all_product_ids if iid not in user_rated_items]

        # Predict scores for all items not rated by the user
        predictions = [self.predict(user_id, pid) for pid in items_to_predict]

        # Predictions
        pred_df = pd.DataFrame({
            'product_id': items_to_predict,
            'score': [pred.est for pred in predictions]
        })

        # Get the top N recommendations
        recommendations = pred_df.sort_values('score', ascending=False).head(top_n)['product_id'].tolist()
        return recommendations