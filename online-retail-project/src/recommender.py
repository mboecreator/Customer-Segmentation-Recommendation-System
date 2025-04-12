import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class ProductRecommender:
    def __init__(self):
        self.user_item_matrix = None
        self.item_similarity = None
        self.product_data = None
        
    def create_user_item_matrix(self, df):
        """Create user-item interaction matrix"""
        # Create pivot table for user-item interactions
        self.user_item_matrix = pd.pivot_table(
            df,
            values='Quantity',
            index='CustomerID',
            columns='StockCode',
            fill_value=0
        )
        
        # Store product information
        self.product_data = df.groupby('StockCode').agg({
            'Description': 'first',
            'UnitPrice': 'mean'
        })
        
        return self.user_item_matrix
    
    def compute_item_similarity(self):
        """Compute item-item similarity matrix"""
        # Normalize the user-item matrix
        matrix_norm = self.user_item_matrix.div(
            np.sqrt(np.square(self.user_item_matrix).sum(axis=0)), 
            axis=1
        )
        
        # Compute cosine similarity
        self.item_similarity = cosine_similarity(matrix_norm.T)
        return self.item_similarity
    
    def get_recommendations(self, customer_id, n_recommendations=5):
        """Get product recommendations for a customer"""
        if customer_id not in self.user_item_matrix.index:
            return []
            
        # Get customer's purchase history
        customer_purchases = self.user_item_matrix.loc[customer_id]
        
        # Calculate recommendation scores
        scores = np.dot(customer_purchases, self.item_similarity)
        
        # Get top N recommendations
        top_items = np.argsort(scores)[-n_recommendations:][::-1]
        
        # Return recommended items with their details
        recommendations = []
        for item_idx in top_items:
            item_id = self.user_item_matrix.columns[item_idx]
            score = scores[item_idx]
            item_info = self.product_data.loc[item_id]
            
            recommendations.append({
                'item_id': item_id,
                'description': item_info['Description'],
                'price': float(item_info['UnitPrice']),
                'score': float(score)
            })
            
        return recommendations
    
    def get_popular_items(self, n_items=5):
        """Get most popular items"""
        item_popularity = self.user_item_matrix.sum(axis=0)
        top_items = item_popularity.nlargest(n_items)
        
        popular_items = []
        for item_id, popularity in top_items.items():
            item_info = self.product_data.loc[item_id]
            popular_items.append({
                'item_id': item_id,
                'description': item_info['Description'],
                'price': float(item_info['UnitPrice']),
                'popularity': int(popularity)
            })
            
        return popular_items 