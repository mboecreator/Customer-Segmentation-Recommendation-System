import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler

class FeatureEngineer:
    def __init__(self):
        self.scaler = StandardScaler()
        self.minmax_scaler = MinMaxScaler()
        
    def prepare_features(self, df):
        """Prepare features for clustering"""
        # Log transform monetary value
        df['Monetary_log'] = np.log1p(df['Monetary'])
        
        # Scale features
        features = ['Recency', 'Frequency', 'Monetary_log']
        df_scaled = df.copy()
        df_scaled[features] = self.scaler.fit_transform(df[features])
        
        return df_scaled
    
    def create_rfm_score(self, df):
        """Create RFM score for each customer"""
        # Create quartiles
        df['R_quartile'] = pd.qcut(df['Recency'], 4, labels=[4, 3, 2, 1])
        df['F_quartile'] = pd.qcut(df['Frequency'], 4, labels=[1, 2, 3, 4])
        df['M_quartile'] = pd.qcut(df['Monetary'], 4, labels=[1, 2, 3, 4])
        
        # Calculate RFM score
        df['RFM_Score'] = df['R_quartile'].astype(int) + df['F_quartile'].astype(int) + df['M_quartile'].astype(int)
        
        return df
    
    def get_customer_segments(self, df):
        """Assign customer segments based on RFM score"""
        df['Segment'] = pd.cut(df['RFM_Score'], 
                              bins=[0, 4, 6, 8, 12],
                              labels=['Low Value', 'Medium Value', 'High Value', 'Top Value'])
        return df 