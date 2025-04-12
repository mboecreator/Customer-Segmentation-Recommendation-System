import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class RecommendationSystem:
    def __init__(self):
        self.user_item_matrix = None
        self.item_similarity = None
        
    def create_user_item_matrix(self, df):
        # Create user-item interaction matrix
        self.user_item_matrix = pd.pivot_table(
            df,
            values='Purchase_Amount',
            index='CustomerID',
            columns='ProductID',
            fill_value=0
        )
        return self.user_item_matrix
    
    def compute_item_similarity(self):
        # Compute item-item similarity using cosine similarity
        self.item_similarity = cosine_similarity(self.user_item_matrix.T)
        return self.item_similarity
    
    def get_recommendations(self, customer_id, n_recommendations=5):
        if self.user_item_matrix is None:
            raise ValueError("User-item matrix not initialized. Call create_user_item_matrix first.")
            
        if self.item_similarity is None:
            self.compute_item_similarity()
            
        # Get user's purchase history
        user_purchases = self.user_item_matrix.loc[customer_id]
        
        # Calculate recommendation scores
        scores = np.dot(user_purchases, self.item_similarity)
        
        # Get top N recommendations
        top_items = np.argsort(scores)[-n_recommendations:][::-1]
        
        # Return recommended items with their scores
        recommendations = []
        for item_idx in top_items:
            item_id = self.user_item_matrix.columns[item_idx]
            score = scores[item_idx]
            recommendations.append({
                'item_id': item_id,
                'score': float(score)
            })
            
        return recommendations 