import streamlit as st
import requests
import json




# Page configuration
st.set_page_config(
    page_title="SuperKart Sales Predictor",
    page_icon="🛒",
    layout="centered"
)

# Title and description
st.title("🛒 SuperKart Sales Predictor")
st.markdown("Predict product sales using your tuned Random Forest model. Enter details below!")

# Input fields matching SuperKart dataset
col1, col2 = st.columns(2)

with col1:
    st.subheader("Product Information")
    product_weight = st.number_input("Product Weight", min_value=0.0, max_value=50.0, value=12.0, step=0.1, key="weight")
    product_mrp = st.number_input("Product MRP ($)", min_value=0.0, max_value=10000.0, value=150.0, step=0.01, key="mrp")
    product_sugar = st.selectbox("Product Sugar Content", ['Low Fat', 'Regular', 'Low Sugar', 'LF'], key="sugar")
    product_type = st.selectbox("Product Type",
                               ['Dairy', 'Soft Drinks', 'Meat', 'Fruits and Vegetables', 'Household',
                                'Baking Goods', 'Snack Foods', 'Frozen Foods', 'Breakfast',
                                'Health and Hygiene', 'Hard Drinks', 'Canned', 'Breads',
                                'Starchy Foods', 'Others'], key="type")

with col2:
    st.subheader("Store Information")
    store_size = st.selectbox("Store Size", ['Small', 'Medium', 'High'], key="size")
    store_location = st.selectbox("Store Location Type", ['Tier 1', 'Tier 2', 'Tier 3'], key="location")
    store_type = st.selectbox("Store Type",
                             ['Grocery Store', 'Supermarket Type1', 'Supermarket Type2', 'Supermarket Type3'], key="store_type")

# Prediction button
if st.button("Predict Sales", key="predict_button"):
    # Prepare data for your backend API
    data = {
        "Product_Weight": product_weight,
        "Product_MRP": product_mrp,
        "Product_Sugar_Content": product_sugar,
        "Product_Type": product_type,
        "Store_Size": store_size,
        "Store_Location_City_Type": store_location,
        "Store_Type": store_type
    }

    # DEBUG: Show what data is being sent
    st.write("### Debug: Data Being Sent to API")
    st.json(data)

    # Call your deployed backend API
    api_url = "https://toddmattingly-superkart-backend.hf.space/predict"

    try:
        response = requests.post(api_url, json=data, timeout=10)

        # DEBUG: Show response details
        st.write(f"### Debug: API Response Status: {response.status_code}")
        
        if response.status_code == 200:
            # API returns a list directly
            predictions = response.json()
            
            # DEBUG: Show raw API response
            st.write("### Debug: Raw API Response")
            st.json(predictions)
            
            prediction = predictions[0] if isinstance(predictions, list) and len(predictions) > 0 else 0

            st.success(f"🎯 Predicted Sales Total: ${prediction:,.2f}")
            st.info(f"📊 Based on: {product_type} at ${product_mrp:,.2f} MRP in a {store_type}")
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")

    except requests.exceptions.RequestException as e:
        st.error(f"Connection Error: {str(e)}")
    except Exception as e:
        st.error(f"Unexpected Error: {str(e)}")

# Footer
st.markdown("---")
st.markdown("*Powered by Streamlit Cloud & Hugging Face Spaces*")
st.markdown("*Using your tuned Random Forest model*")

# Additional debug info
st.markdown("### Session Info")
st.write(f"Session ID: {st.session_state}")
