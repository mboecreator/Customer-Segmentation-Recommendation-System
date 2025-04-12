from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd

class CustomerClustering:
    def __init__(self, n_clusters=4):
        self.n_clusters = n_clusters
        self.model = KMeans(n_clusters=n_clusters, random_state=42)
        self.scaler = StandardScaler()
        self.features = ['Recency', 'Frequency', 'Monetary']
        
    def prepare_data(self, df):
        """Prepare data for clustering"""
        # Log transform monetary value
        df['Monetary_log'] = np.log1p(df['Monetary'])
        
        # Scale features
        X = df[self.features].copy()
        X_scaled = self.scaler.fit_transform(X)
        
        return X_scaled
    
    def fit(self, df):
        """Fit the clustering model"""
        X_scaled = self.prepare_data(df)
        self.model.fit(X_scaled)
        return self
    
    def predict(self, df):
        """Predict clusters for new data"""
        X_scaled = self.prepare_data(df)
        return self.model.predict(X_scaled)
    
    def get_cluster_centers(self):
        """Get cluster centers in original scale"""
        centers_scaled = self.model.cluster_centers_
        centers_original = self.scaler.inverse_transform(centers_scaled)
        return pd.DataFrame(centers_original, columns=self.features)
    
    def get_silhouette_score(self, df):
        """Calculate silhouette score"""
        X_scaled = self.prepare_data(df)
        labels = self.predict(df)
        return silhouette_score(X_scaled, labels)
    
    def find_optimal_clusters(self, df, max_clusters=10):
        """Find optimal number of clusters using elbow method"""
        X_scaled = self.prepare_data(df)
        inertia = []
        silhouette_scores = []
        
        for k in range(2, max_clusters + 1):
            kmeans = KMeans(n_clusters=k, random_state=42)
            kmeans.fit(X_scaled)
            inertia.append(kmeans.inertia_)
            silhouette_scores.append(silhouette_score(X_scaled, kmeans.labels_))
            
        return inertia, silhouette_scores
    
    def get_cluster_statistics(self, df):
        """Get statistics for each cluster"""
        df['Cluster'] = self.predict(df)
        cluster_stats = df.groupby('Cluster').agg({
            'Recency': ['mean', 'std', 'min', 'max'],
            'Frequency': ['mean', 'std', 'min', 'max'],
            'Monetary': ['mean', 'std', 'min', 'max']
        }).round(2)
        
        return cluster_stats 