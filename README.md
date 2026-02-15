# 🛍️ Customer Personality Analysis & Prediction

An end-to-end Machine Learning project that utilizes **Unsupervised Learning (Clustering)** to segment customers and **Supervised Learning (Classification)** to predict marketing campaign responses.

## 🚀 Project Overview
This project addresses the challenge of optimizing marketing budgets by identifying distinct customer personalities. By first using **K-Means Clustering** to group customers (e.g., VIPs, Budget Shoppers), and then training a **Random Forest Classifier**, the system not only understands *who* the customer is but also predicts *if* they will accept a campaign offer. This dual approach maximizes ROI by targeting the right message to the right persona.

## 🛠️ Tech Stack
* **Python:** Core language for data processing
* **K-Means Clustering:** Unsupervised learning for customer segmentation
* **Random Forest Classifier:** Supervised learning for campaign response prediction
* **Scikit-Learn:** Machine Learning pipeline (StandardScaler, GridSearch, Evaluation)
* **Pandas & Seaborn:** Data Cleaning, Feature Engineering, and Exploratory Data Analysis (EDA)
* **Streamlit:** Web App Deployment for real-time customer analysis

## 📊 Key Features
* **Smart Segmentation:** Automatically groups customers into 4 distinct personas: **VIP Elite**, **Average User**, **Budget Family**, and **At-Risk Customer**.
* **Predictive Intelligence:** Forecasts "Likely to Buy" or "Unlikely to Buy" with high accuracy using historical campaign data.
* **Strategic Insights:** Provides actionable marketing strategies (e.g., "Send Exclusive Rewards" vs. "Send Discount Coupons") based on the predicted cluster.
* **Live Dashboard:** An interactive Streamlit app that visualizes customer segments and predictions in real-time.

## 🗺️ Project Pipeline

---

```mermaid
graph TD
    %% Global Styles
    classDef process fill:#e1f5fe,stroke:#01579b,stroke-width:2px;
    classDef model fill:#fff9c4,stroke:#fbc02d,stroke-width:2px;
    classDef result fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px;
    classDef input fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px;

    subgraph "Phase 1: Model Training (Jupyter Notebook)"
        A[📂 Load Dataset]:::input --> B[🧹 Data Cleaning & Feature Engineering]:::process
        B --> C{Split Path}
        
        %% Unsupervised Path
        C -- "Unsupervised Learning" --> D[📏 Standard Scaler]:::process
        D --> E[📉 Elbow Method]:::process
        E --> F[🤖 K-Means Clustering K=4]:::model
        F --> G[🏷️ Assign Cluster IDs]:::result
        
        %% Supervised Path
        C -- "Supervised Learning" --> H[✂️ Train/Test Split]:::process
        G --> I[Use Cluster ID as Feature]:::process
        I --> J[🌲 Train Random Forest Classifier]:::model
        H --> J
        J --> K[📊 Evaluate F1-Score]:::result
        
        %% Saving
        G --> L[💾 Save .pkl Models]:::input
        K --> L
    end

    subgraph "Phase 2: Deployment (Streamlit App)"
        M[👤 User Input: Income, Age, Spend]:::input --> N[📥 Load Saved Models]:::process
        N --> O[🔍 Step 1: Predict Cluster]:::model
        O --> P[🏆 Identify Segment: VIP/Budget/etc.]:::result
        
        N --> Q[🔮 Step 2: Predict Buying Probability]:::model
        P --> Q
        Q --> R{Will they Buy?}
        
        R -- "Yes (1)" --> S[✅ Display: Likely to Accept]:::result
        R -- "No (0)" --> T[❌ Display: Unlikely to Accept]:::result
        
        S --> U[💡 Show Marketing Strategy]:::process
        T --> U
    end

    L -.-> N
