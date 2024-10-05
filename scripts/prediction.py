import pandas as pd
import numpy as np

def prepare_features(city, district, land_size, building_size, electricity, bedrooms, 
                     bathrooms, carports, garages, floors, maid_bedrooms, maid_bathrooms, 
                     ac, garden, pool):
    """Prepare input features for the model."""
    features = {
        'city': city,
        'district': district,
        'land_size_m2': land_size,
        'building_size_m2': building_size,
        'electricity': electricity,
        'bedrooms': bedrooms,
        'bathrooms': bathrooms,
        'carports': carports,
        'garages': garages,
        'floors': floors,
        'maid_bedrooms': maid_bedrooms,
        'maid_bathrooms': maid_bathrooms,
        'Ac': 1 if ac else 0,
        'Taman': 1 if garden else 0,
        'KolamRenang': 1 if pool else 0
    }
    return pd.DataFrame([features])

def predict_price(model, input_data):
    """Predict property price using the model and return a price range with a margin of ±15%."""
    log_prediction = model.predict(input_data)
    price_prediction = np.exp(log_prediction)  # Transform back from log to original scale
    price_prediction = int(price_prediction[0])  # Convert to integer

    # Calculate the price range
    margin = price_prediction * 0.15  # 15% margin
    lower_bound = int(price_prediction - margin)
    upper_bound = int(price_prediction + margin)

    return lower_bound, price_prediction, upper_bound  # Return as a tuple
