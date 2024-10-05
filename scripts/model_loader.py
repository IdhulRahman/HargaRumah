import joblib

def load_model(pkl_file):
    """Load machine learning model from pickle file."""
    model = joblib.load(pkl_file)
    return model
