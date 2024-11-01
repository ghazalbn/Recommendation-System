import unittest
from models.hybrid import HybridRecommender
from utils.explainability import Explainability
from tests.test_data import get_test_data

class TestRecommendations(unittest.TestCase):
    def setUp(self):
        df_users, df_products, df_interactions, df_context = get_test_data()
        self.hybrid_recommender = HybridRecommender(
            df_users, df_products, df_interactions, df_context
        )
        self.explainability = Explainability(
            df_users,
            df_products,
            df_interactions,
            self.hybrid_recommender.collaborative_filtering,
        )
        self.df_users = df_users
        self.df_products = df_products

    def test_existing_user_recommendations(self):
        user_id = 1  # Alice
        recommendations = self.hybrid_recommender.get_recommendations(user_id, top_n=3)
        self.assertEqual(len(recommendations), 3)
        for pid in recommendations:
            self.assertIn(pid, self.df_products['product_id'].values)

    def test_cold_start_user_recommendations(self):
        user_id = 5  # Eve
        recommendations = self.hybrid_recommender.get_recommendations(user_id, top_n=3)
        self.assertEqual(len(recommendations), 3)
        for pid in recommendations:
            self.assertIn(pid, self.df_products['product_id'].values)

    def test_explanations(self):
        user_id = 1
        recommendations = self.hybrid_recommender.get_recommendations(user_id, top_n=3)
        explanations = self.explainability.explain_recommendations(user_id, recommendations)
        self.assertIsInstance(explanations, dict)
        self.assertEqual(len(explanations), 3)
        for pid in recommendations:
            self.assertIn(pid, explanations)
            self.assertIsInstance(explanations[pid], list)
            self.assertTrue(len(explanations[pid]) > 0)

if __name__ == '__main__':
    unittest.main()
