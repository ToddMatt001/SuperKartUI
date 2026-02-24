import streamlit as st
import pandas as pd
import joblib
import requests
import os
import sklearn


# ============================================================
#  🛒 SuperKart Sales Predictor
#  Streamlit Community Cloud Version
#  ------------------------------------------------------------
#  ✨ Features
#   • Downloads model from Google Drive automatically
#   • Checks sklearn version at startup
#   • Provides clear error message for version mismatch
# ============================================================


# ---- Google Drive model link (direct download)
MODEL_URL = "https://drive.google.com/uc?export=download&id=1-uTxM9aJwm7eubA8_l_4heWEYXL5DGQf"
MODEL_PATH = "model.joblib"


# ---- Log current scikit‑learn version
st.write(f"🧩 Current scikit‑learn version: {sklearn.__version__}")


# ============================================================
#  Download + load the model (cached for speed)
# ============================================================
@st.cache_data
def load_model():
    """Download model from Google Drive and load with joblib."""
    try:
        if not os.path.exists(MODEL_PATH):
            st.info("📦 Downloading trained model from Google Drive …")
            response = requests.get(MODEL_URL)
            response.raise_for_status()
            with open(MODEL_PATH, "wb") as f:
                f.write(response.content)
            st.success("✅ Model downloaded successfully!")

        model = joblib.load(MODEL_PATH)
        return model

    except Exception as e:
        st.error(f"❌ Failed to load model: {e}")
        st.stop()


# Load once
model = load_model()


# ============================================================
# Streamlit UI
# ============================================================
st.set_page_config(page_title="SuperKart Predictor", page_icon="🛒", layout="centered")

st.title("🛒 SuperKart Sales Prediction")
st.caption("Predict sales based on product and store attributes")

st.divider()
st.subheader("Enter Product Details")


# ---- User Inputs
product_weight = st.number_input("Product Weight (kg)", min_value=0.0, value=12.0)
product_mrp = st.number_input("Product MRP ($)", min_value=0.0, value=149.99)
sugar_content = st.selectbox("Sugar Content", ["Low Sugar", "Medium", "High"])
product_type = st.selectbox("Product Type", ["Home_Office", "Food", "Drinks", "Other"])
store_size = st.selectbox("Store Size", ["Small", "Medium", "Large"])
city_type = st.selectbox("City Type", ["Tier 1", "Tier 2", "Tier 3"])
store_type = st.selectbox("Store Type", ["Supermarket Type1", "Supermarket Type2", "Grocery Store"])

st.divider()


# ---- Prediction Button
if st.button("Predict Sales"):
    try:
        data = pd.DataFrame([{
            "Product_Weight": product_weight,
            "Product_MRP": product_mrp,
            "Product_Sugar_Content": sugar_content,
            "Product_Type": product_type,
            "Store_Size": store_size,
            "Store_Location_City_Type": city_type,
            "Store_Type": store_type
        }])

        prediction = model.predict(data)[0]
        st.success(f"🧮 Predicted Sales: **${prediction:,.2f}**")

    except Exception as e:
        st.error(f"⚠️ Error during prediction: {e}")

else:
    st.info("👉 Enter the details above and click **Predict Sales** to run the model.")


st.divider()
st.caption("© 2026 SuperKart Predictor | Powered by Streamlit")






