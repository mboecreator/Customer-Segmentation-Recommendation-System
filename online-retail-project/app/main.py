import os
import sys
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pandas as pd

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# Now import our modules
from src.data_preprocessing import DataPreprocessor
from src.feature_engineering import FeatureEngineer
from src.clustering import CustomerClustering
from src.recommender import ProductRecommender
from src.utils import plot_cluster_distribution, plot_rfm_distribution, plot_cluster_characteristics

app = Flask(__name__)
CORS(app)

# Initialize components
preprocessor = DataPreprocessor()
feature_engineer = FeatureEngineer()
clustering = CustomerClustering()
recommender = ProductRecommender()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and file.filename.endswith('.csv'):
        try:
            # Save the file
            file_path = os.path.join('data', file.filename)
            file.save(file_path)
            
            # Process the data
            df = preprocessor.load_data(file_path)
            customer_data = preprocessor.get_customer_data()
            
            # Feature engineering
            customer_data = feature_engineer.prepare_features(customer_data)
            customer_data = feature_engineer.create_rfm_score(customer_data)
            customer_data = feature_engineer.get_customer_segments(customer_data)
            
            # Clustering
            clustering.fit(customer_data)
            customer_data['Cluster'] = clustering.predict(customer_data)
            
            # Recommendation system
            recommender.create_user_item_matrix(df)
            recommender.compute_item_similarity()
            
            return jsonify({
                'message': 'File processed successfully',
                'customer_data': customer_data.to_dict(orient='records')
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Invalid file format'}), 400

@app.route('/recommendations', methods=['POST'])
def get_recommendations():
    data = request.json
    customer_id = data.get('customer_id')
    
    if not customer_id:
        return jsonify({'error': 'Customer ID is required'}), 400
    
    try:
        recommendations = recommender.get_recommendations(customer_id)
        return jsonify({
            'recommendations': recommendations
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001) 