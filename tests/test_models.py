import unittest
from models.hybrid import HybridRecommender
from utils.explainability import Explainability
from tests.test_data import get_test_data

class TestRecommendationModels(unittest.TestCase):
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

    def test_recommendations_for_existing_user(self):
        user_id = 1  # Alice
        recommendations = self.hybrid_recommender.get_recommendations(user_id, top_n=3)
        self.assertIsInstance(recommendations, list)
        self.assertEqual(len(recommendations), 3)
        # Check that recommended product IDs are in the products list
        for pid in recommendations:
            self.assertIn(pid, self.df_products['product_id'].values)

    def test_recommendations_for_cold_start_user(self):
        user_id = 5  # Eve
        recommendations = self.hybrid_recommender.get_recommendations(user_id, top_n=3)
        self.assertIsInstance(recommendations, list)
        self.assertEqual(len(recommendations), 3)
        for pid in recommendations:
            self.assertIn(pid, self.df_products['product_id'].values)

    def test_explanations(self):
        user_id = 1
        recommendations = self.hybrid_recommender.get_recommendations(user_id, top_n=3)
        explanations = self.explainability.explain_recommendations(user_id, recommendations)
        self.assertIsInstance(explanations, dict)
        self.assertEqual(len(explanations), 3)
        # Check that explanations correspond to recommended products
        for pid in recommendations:
            self.assertIn(pid, explanations)
            self.assertIsInstance(explanations[pid], list)
            self.assertTrue(len(explanations[pid]) > 0)

    def test_recommendations_length(self):
        user_id = 2  # Bob
        recommendations = self.hybrid_recommender.get_recommendations(user_id, top_n=5)
        self.assertIsInstance(recommendations, list)
        self.assertLessEqual(len(recommendations), 5)
        # Check that recommended product IDs are in the products list
        for pid in recommendations:
            self.assertIn(pid, self.df_products['product_id'].values)

    def test_invalid_user_id(self):
        user_id = 999  # Non-existent user
        with self.assertRaises(IndexError):
            self.hybrid_recommender.get_recommendations(user_id, top_n=3)

    def test_user_with_multiple_categories(self):
        user_id = 2  # Bob
        recommendations = self.hybrid_recommender.get_recommendations(user_id, top_n=5)
        self.assertIsInstance(recommendations, list)
        self.assertLessEqual(len(recommendations), 5)
        # Check that recommendations are from expected categories
        for pid in recommendations:
            self.assertIn(pid, self.df_products['product_id'].values)

    def test_all_recommendations_are_unique(self):
        user_id = 1
        recommendations = self.hybrid_recommender.get_recommendations(user_id, top_n=5)
        self.assertEqual(len(recommendations), len(set(recommendations)))

    def test_recommendations_not_contain_interacted_products(self):
        user_id = 1
        recommendations = self.hybrid_recommender.get_recommendations(user_id, top_n=5)
        interacted_products = set(self.hybrid_recommender.df_interactions[self.hybrid_recommender.df_interactions['user_id'] == user_id]['product_id'])
        for pid in recommendations:
            self.assertNotIn(pid, interacted_products)

if __name__ == '__main__':
    unittest.main()
