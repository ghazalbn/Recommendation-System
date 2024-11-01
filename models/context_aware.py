from datetime import datetime

class ContextAwareAdjuster:
    def __init__(self, df_users, df_products, df_context):
        self.df_users = df_users
        self.df_products = df_products
        self.df_context = df_context
    
    def adjust_for_context(self, user_id, recommendations):
        # Get user's device
        device_type = self.df_users[self.df_users['user_id'] == user_id]['device'].values[0]
        
        # Current day and season
        current_day = datetime.now().strftime('%A')
        current_month = datetime.now().month
        if current_month in [12, 1, 2]:
            season = 'Holiday'
        elif current_month in [6, 7, 8]:
            season = 'Summer'
        else:
            season = 'All Year'
        
        adjusted_recommendations = recommendations.copy()
        for idx, product_id in enumerate(recommendations):
            category = self.df_products[self.df_products['product_id'] == product_id]['category'].values[0]
            context = self.df_context[self.df_context['category'] == category]
            if not context.empty:
                peak_days = context['peak_days'].values[0]
                context_season = context['season'].values[0]
                if current_day in peak_days or season == context_season:
                    adjusted_recommendations.insert(0, adjusted_recommendations.pop(idx))
        return adjusted_recommendations
