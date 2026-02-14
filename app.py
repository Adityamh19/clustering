import streamlit as st
import pandas as pd
import joblib
import numpy as np

# --- 1. Load ALL Models (Clustering + Prediction) ---
try:
    kmeans_model = joblib.load('kmeans_model.pkl')
    scaler = joblib.load('scaler.pkl')
    prediction_model = joblib.load('response_prediction_model.pkl')
except FileNotFoundError:
    st.error("🚨 Critical Error: Models not found! Make sure you saved 'kmeans_model.pkl', 'scaler.pkl', and 'response_prediction_model.pkl'.")
    st.stop()

# --- 2. Manual Labeling (Based on your Truth Table) ---
# We use this instead of auto-detection to guarantee 100% accuracy
def get_manual_cluster_name(cluster_id):
    mapping = {
        2: ("VIP Elite", "🏆"),         # High Income ($75k)
        3: ("Average User", "⚖️"),      # Middle Income ($55k)
        0: ("Budget Family", "📉"),     # Low Income ($29k)
        1: ("At-Risk Customer", "⚠️")   # High Recency (74 days)
    }
    return mapping.get(cluster_id, ("Unknown Segment", "❓"))

# --- 3. App UI ---
st.set_page_config(page_title="Customer AI Dashboard", page_icon="🛍️", layout="centered")

st.title("🛍️ Customer Intelligence AI")
st.markdown("Enter details to reveal **Marketing Segment** & **Buying Probability**.")

# --- 4. Input Form ---
with st.form("my_form"):
    col1, col2 = st.columns(2)
    with col1:
        income = st.number_input("Annual Income ($)", value=50000, step=1000)
        spend = st.number_input("Total Spent ($)", value=500, step=10)
        age = st.number_input("Age", value=35, step=1)
    with col2:
        family = st.number_input("Family Size", value=2, step=1)
        recency = st.number_input("Days Since Last Visit", value=30, step=1)
        
    submitted = st.form_submit_button("🔮 Analyze Customer")

# --- 5. Logic Execution ---
if submitted:
    # --- PART A: CLUSTERING (Who are they?) ---
    # 1. Scale Data for KMeans
    raw_data_for_scaler = np.array([[income, spend, age, family, recency]])
    scaled_data = scaler.transform(raw_data_for_scaler)
    
    # 2. Predict Cluster
    cluster_id = kmeans_model.predict(scaled_data)[0]
    
    # 3. Get Human-Readable Name (Using the fixed mapping)
    persona_name, emoji = get_manual_cluster_name(cluster_id)

    # --- PART B: PREDICTION (Will they buy?) ---
    # Prepare data for Random Forest (It needs Raw Data + Cluster ID)
    input_for_prediction = pd.DataFrame([[income, spend, age, family, recency, cluster_id]], 
                                        columns=['Income', 'Total_Spent', 'Age', 'Family_Size', 'Recency', 'Cluster'])
    
    # Predict (1 = Yes, 0 = No)
    will_buy = prediction_model.predict(input_for_prediction)[0]
    
    # --- 6. DISPLAY RESULTS (Layout Matches Your Request) ---
    
    # --- RESULT 1: SEGMENTATION ---
    st.divider()
    st.markdown(f"""
        <div style="text-align: center;">
            <p style="font-size: 20px; margin-bottom: 0px;">Customer Belongs to Cluster</p>
            <h1 style="font-size: 80px; margin-top: 0px; margin-bottom: 10px; color: #4CAF50;">{cluster_id}</h1>
            <h3 style="margin-top: 0px;">{emoji} {persona_name}</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # --- RESULT 2: BUYING PREDICTION ---
    st.write("") # Spacer
    st.subheader("📢 Campaign Prediction")
    
    if will_buy == 1:
        st.success("✅ **Prediction: LIKELY to Accept Offer!**")
        st.write("💡 **Action:** Send the campaign immediately. High conversion chance.")
    else:
        st.error("❌ **Prediction: Unlikely to Accept**")
        st.write("💡 **Action:** Don't waste marketing budget. Nurture them with free content first.")

    # --- Detailed Strategy Box ---
    with st.expander("View Detailed Strategy Strategy"):
        if persona_name == "VIP Elite":
            st.write("👉 **Strategy:** Offer exclusive premium rewards (No discounts).")
        elif persona_name == "Budget Family":
            st.write("👉 **Strategy:** Offer budget deals and family combos.")
        elif persona_name == "At-Risk Customer":
            st.write("👉 **Strategy:** **URGENT!** Send 'We Miss You' coupons immediately.")
        else:
            st.write("👉 **Strategy:** Encourage them to join the loyalty program.")