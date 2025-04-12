import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

def plot_cluster_distribution(df, cluster_col='Cluster'):
    """Plot distribution of customers across clusters"""
    plt.figure(figsize=(10, 6))
    sns.countplot(x=cluster_col, data=df)
    plt.title('Customer Distribution Across Clusters')
    plt.xlabel('Cluster')
    plt.ylabel('Number of Customers')
    plt.show()

def plot_rfm_distribution(df):
    """Plot distribution of RFM metrics"""
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    sns.histplot(df['Recency'], ax=axes[0])
    axes[0].set_title('Recency Distribution')
    
    sns.histplot(df['Frequency'], ax=axes[1])
    axes[1].set_title('Frequency Distribution')
    
    sns.histplot(df['Monetary'], ax=axes[2])
    axes[2].set_title('Monetary Distribution')
    
    plt.tight_layout()
    plt.show()

def plot_cluster_characteristics(df, cluster_col='Cluster'):
    """Plot characteristics of each cluster"""
    cluster_stats = df.groupby(cluster_col).agg({
        'Recency': 'mean',
        'Frequency': 'mean',
        'Monetary': 'mean'
    })
    
    plt.figure(figsize=(12, 6))
    cluster_stats.plot(kind='bar')
    plt.title('Cluster Characteristics')
    plt.xlabel('Cluster')
    plt.ylabel('Average Value')
    plt.legend(title='Metric')
    plt.show()

def save_results(df, filename):
    """Save analysis results to CSV"""
    df.to_csv(filename, index=False)
    print(f"Results saved to {filename}") 