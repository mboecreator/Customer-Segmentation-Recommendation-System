# Customer Segmentation & Recommendation System

A web application for customer segmentation and personalized recommendations.

## Features
- Customer data analysis and visualization
- K-means clustering for customer segmentation
- Personalized product recommendations
- Interactive dashboard

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Access the web interface at `http://localhost:5000`

## Project Structure
```
├── app.py                 # Flask application
├── static/               # Static files (CSS, JS, images)
├── templates/            # HTML templates
├── ml/                   # Machine learning models
│   ├── segmentation.py   # Customer segmentation logic
│   └── recommendation.py # Recommendation system
├── data/                 # Data files
└── requirements.txt      # Python dependencies
``` 