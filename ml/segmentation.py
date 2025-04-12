import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

class CustomerSegmentation:
    def __init__(self, n_clusters=4):
        self.n_clusters = n_clusters
        self.model = KMeans(n_clusters=n_clusters, random_state=42)
        self.scaler = StandardScaler()
        
    def preprocess_data(self, df):
        # Select relevant features for segmentation
        features = ['Recency', 'Frequency', 'Monetary']
        X = df[features].copy()
        
        # Handle missing values
        X = X.fillna(X.mean())
        
        # Scale the features
        X_scaled = self.scaler.fit_transform(X)
        return X_scaled
    
    def fit_predict(self, df):
        # Preprocess the data
        X_scaled = self.preprocess_data(df)
        
        # Fit the model and predict clusters
        clusters = self.model.fit_predict(X_scaled)
        
        # Add cluster labels to the original dataframe
        df['Cluster'] = clusters
        
        return clusters
    
    def get_cluster_centers(self):
        return self.model.cluster_centers_
    
    def get_cluster_statistics(self, df):
        cluster_stats = df.groupby('Cluster').agg({
            'Recency': ['mean', 'std'],
            'Frequency': ['mean', 'std'],
            'Monetary': ['mean', 'std']
        }).round(2)
        
        return cluster_stats 