import pandas as pd
import joblib
import numpy as np

print("🔌 Loading Models...")
try:
    kmeans_model = joblib.load('kmeans_model.pkl')
    scaler = joblib.load('scaler.pkl')
    prediction_model = joblib.load('response_prediction_model.pkl')
    print("✅ Models Loaded Successfully!\n")
except FileNotFoundError:
    print("🚨 Error: .pkl files not found.")
    exit()

# --- HARD CODED LOGIC (Must match App) ---
def get_cluster_name(cluster_id):
    mapping = {
        2: "VIP Elite",
        3: "Average User",
        0: "Budget Family",
        1: "At-Risk Customer"
    }
    return mapping.get(cluster_id, "Unknown")

# --- TEST CASES ---
test_cases = [
    {
        "Name": "Test Case A: The VIP",
        "Input": [90000, 1800, 45, 1, 10], 
        "Expected_Segment": "VIP Elite"
    },
    {
        "Name": "Test Case B: The Budget Shopper",
        "Input": [25000, 50, 30, 3, 20],
        "Expected_Segment": "Budget Family"
    },
    {
        "Name": "Test Case C: The At-Risk Customer",
        "Input": [48000, 300, 40, 3, 90], # Adjusted to match Cluster 1 centroid (Income ~45k, Recency ~74)
        "Expected_Segment": "At-Risk Customer"
    },
    {
        "Name": "Test Case D: The Average User",
        "Input": [55000, 540, 38, 2, 22], # Matches Cluster 3 centroid exactly
        "Expected_Segment": "Average User"
    }
]

print("==========================================")
print("🚀 STARTING AUTOMATED SYSTEM TEST")
print("==========================================\n")

for test in test_cases:
    print(f"🔹 Running: {test['Name']}")
    
    # Segment
    raw_data = np.array([test['Input']])
    scaled_data = scaler.transform(raw_data)
    cluster_id = kmeans_model.predict(scaled_data)[0]
    predicted_segment = get_cluster_name(cluster_id)
    
    # Report
    print(f"   Input: Income=${test['Input'][0]}, Recency={test['Input'][4]}")
    if predicted_segment == test['Expected_Segment']:
        print(f"   ✅ Segment Check: PASSED (Got '{predicted_segment}' - Cluster {cluster_id})")
    else:
        print(f"   ❌ Segment Check: FAILED (Expected '{test['Expected_Segment']}', Got '{predicted_segment}' - Cluster {cluster_id})")
    print("-" * 40)

print("\n🎉 Test Complete.")