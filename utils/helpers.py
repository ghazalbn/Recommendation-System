def assign_interaction_weights(df_interactions):
    interaction_weights = {
        'view': 1,
        'click': 2,
        'add_to_cart': 3,
        'purchase': 5
    }
    df_interactions['weight'] = df_interactions['event'].map(interaction_weights)
    return df_interactions
