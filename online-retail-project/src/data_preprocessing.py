import pandas as pd
import numpy as np
from datetime import datetime

class DataPreprocessor:
    def __init__(self):
        self.data = None
        
    def load_data(self, file_path):
        """Load and clean the retail data"""
        self.data = pd.read_csv(file_path, encoding='latin1')
        self._clean_data()
        return self.data
    
    def _clean_data(self):
        """Clean the dataset"""
        # Remove rows with missing values
        self.data = self.data.dropna()
        
        # Convert InvoiceDate to datetime
        self.data['InvoiceDate'] = pd.to_datetime(self.data['InvoiceDate'])
        
        # Remove negative quantities and prices
        self.data = self.data[self.data['Quantity'] > 0]
        self.data = self.data[self.data['UnitPrice'] > 0]
        
        # Calculate total price
        self.data['TotalPrice'] = self.data['Quantity'] * self.data['UnitPrice']
        
        # Remove cancelled transactions
        self.data = self.data[~self.data['InvoiceNo'].str.startswith('C')]
        
        # Convert CustomerID to string
        self.data['CustomerID'] = self.data['CustomerID'].astype(str)
    
    def get_customer_data(self):
        """Extract customer-level data for RFM analysis"""
        # Calculate recency (days since last purchase)
        max_date = self.data['InvoiceDate'].max()
        
        customer_data = self.data.groupby('CustomerID').agg({
            'InvoiceDate': lambda x: (max_date - x.max()).days,  # Recency
            'InvoiceNo': 'nunique',  # Frequency
            'TotalPrice': 'sum'      # Monetary
        }).reset_index()
        
        # Rename columns
        customer_data = customer_data.rename(columns={
            'InvoiceDate': 'Recency',
            'InvoiceNo': 'Frequency',
            'TotalPrice': 'Monetary'
        })
        
        return customer_data
    
    def get_product_data(self):
        """Extract product-level data for recommendations"""
        product_data = self.data.groupby('StockCode').agg({
            'Description': 'first',
            'UnitPrice': 'mean',
            'Quantity': 'sum'
        }).reset_index()
        
        return product_data 