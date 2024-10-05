import streamlit as st
from scripts.data_loader import load_data
from scripts.model_loader import load_model
from scripts.map_util import display_map
from scripts.prediction import prepare_features, predict_price

# Custom CSS for better aesthetics
st.markdown("""
    <style>
        .main { background-color: #f4f7f8; }
        h1 { color: #2c3e50; text-align: center; }
        .stButton>button { background-color: #3498db; color: white; }
        .stButton>button:hover { background-color: #2980b9; }
        .stNumberInput input { border: 2px solid #2c3e50; }
        .stSelectbox>div>div { background-color: #ecf0f1; color: #34495e; }
    </style>
""", unsafe_allow_html=True)

# Load model and data
model = load_model('model/model_harga_rumah1.pkl')
data = load_data('data/Final_data.csv')

# Extract unique cities and districts from the data
unique_cities = data['city'].unique()

# Streamlit Interface
st.title("🛒 Jual Beli Properti Rumah Jabodetabek 🏡")

st.markdown("<h4 style='text-align: center; color: grey;'>Membantu Anda menemukan properti impian</h4>", unsafe_allow_html=True)

# Step 1: City Selection
st.subheader("1️⃣ Pilih Kota")
city = st.selectbox("Pilih Kota", options=unique_cities)

# Step 2: District Selection based on City
if city:
    st.subheader("2️⃣ Pilih Daerah")
    filtered_districts = data[data['city'] == city]['district'].unique()
    district = st.selectbox("Pilih Daerah", options=filtered_districts)

# Step 3: Display Map based on selected district's lat and long
if district:
    st.subheader("3️⃣ Lokasi Properti di Peta")
    selected_data = data[(data['city'] == city) & (data['district'] == district)]
    
    # Calculate the average latitude and longitude for the district
    lat = selected_data['lat'].mean()
    long = selected_data['long'].mean()
    
    # Display map
    display_map(lat, long)

# Step 4: Input Property Features (Updated with maid's rooms and bathrooms)
st.subheader("4️⃣ Isi Fitur Properti")
st.markdown("<small>Masukkan detail properti Anda untuk mendapatkan estimasi harga.</small>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    land_size = st.slider("Luas Tanah (m²)", 0, 1000, 100, step=10)
    building_size = st.slider("Luas Bangunan (m²)", 0, 1000, 100, step=10)
    electricity = st.slider("Daya Listrik (watt)", 450, 10000, 2200, step=50)
with col2:
    bedrooms = st.number_input("🛏 Jumlah Kamar Tidur", min_value=0, max_value=9, value=3)
    bathrooms = st.number_input("🚿 Jumlah Kamar Mandi", min_value=0, max_value=10, value=2)
    carports = st.number_input("🚗 Jumlah Carport", min_value=0, max_value=4, value=1)
    garages = st.number_input("🅿 Jumlah Garasi", min_value=0, max_value=4, value=1)
    floors = st.number_input("🏠 Jumlah Lantai", min_value=1, value=2)

# Optional Features for maid's rooms and bathrooms
st.subheader("🛏 Kamar Pembantu dan Kamar Mandi Pembantu (Opsional)")
col3, col4 = st.columns(2)
with col3:
    maid_bedrooms = st.number_input("Jumlah Kamar Tidur Pembantu", min_value=0, max_value=4, value=0)
with col4:
    maid_bathrooms = st.number_input("Jumlah Kamar Mandi Pembantu", min_value=0, max_value=4, value=0)

# Optional Features
st.subheader("5️⃣ Fasilitas Tambahan")
ac = st.checkbox("🌀 AC", value=True)
garden = st.checkbox("🌳 Taman", value=True)
pool = st.checkbox("🏊 Kolam Renang", value=False)

# predicting the price
if st.button("🔮 Prediksi Harga"):
    input_data = prepare_features(city, district, land_size, building_size, electricity, 
                                  bedrooms, bathrooms, carports, garages, floors, 
                                  maid_bedrooms, maid_bathrooms, ac, garden, pool)
    
    # Predict price using the model
    lower_bound, price_prediction, upper_bound = predict_price(model, input_data)
    
    # Display prediction
    st.markdown(f"<h3>🏷 Prediksi Harga Properti: Rp {price_prediction:,}</h3>", unsafe_allow_html=True)
    st.markdown(f"<h3>🏷 Range Harga Properti   : Rp {lower_bound:,} - Rp {upper_bound:,}</h3>", unsafe_allow_html=True)
