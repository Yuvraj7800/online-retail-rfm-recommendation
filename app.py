"""
Online Retail — Customer Segmentation & Product Recommendation
Streamlit App
"""
import streamlit as st
import pandas as pd
import numpy as np
import joblib

st.set_page_config(page_title="Retail Customer Intelligence", page_icon="🛍️", layout="wide")

st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
        padding: 1.5rem 2rem; border-radius: 12px; margin-bottom: 1.5rem; color: white;
    }
    .rec-card {
        background: #f8f9fa; border-left: 4px solid #2575fc;
        padding: 0.8rem 1rem; border-radius: 8px; margin: 0.4rem 0;
    }
    .segment-badge {
        display: inline-block; padding: 0.4rem 1rem; border-radius: 20px;
        font-weight: 700; font-size: 1.1rem; color: white;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class='main-header'>
    <h1 style='margin:0'>🛍️ Retail Customer Intelligence App</h1>
    <p style='margin:0.3rem 0 0 0; opacity:0.9'>RFM Customer Segmentation · Product Recommendations</p>
</div>
""", unsafe_allow_html=True)


@st.cache_resource(show_spinner=False)
def load_artifacts():
    rfm_bundle = joblib.load("rfm_kmeans_model.pkl")
    item_sim_df = joblib.load("item_similarity_matrix.pkl")
    return rfm_bundle, item_sim_df


try:
    rfm_bundle, item_sim_df = load_artifacts()
    model = rfm_bundle["model"]
    scaler = rfm_bundle["scaler"]
    label_map = rfm_bundle["label_map"]
    LOADED = True
except Exception as e:
    LOADED = False
    st.error(f"Could not load model files: {e}")
    st.info("Make sure `rfm_kmeans_model.pkl` and `item_similarity_matrix.pkl` are in the same folder as app.py.")
    st.stop()

SEGMENT_COLORS = {
    "Champions (High-Value)": "#2ca02c",
    "Loyal / Regular": "#1f77b4",
    "Occasional / New": "#ff7f0e",
    "At-Risk / Lost": "#d62728",
}

SEGMENT_ADVICE = {
    "Champions (High-Value)": "Your most valuable customers. Reward with VIP perks, early access, and loyalty tiers — protect this revenue base.",
    "Loyal / Regular": "Consistent buyers with growth potential. Use cross-sell and upsell campaigns to move them toward Champion status.",
    "Occasional / New": "Recent but infrequent buyers. Nurture with onboarding offers and personalized follow-ups to build the habit.",
    "At-Risk / Lost": "Haven't purchased in a long time. Launch win-back campaigns with discounts or re-engagement emails before they're gone for good.",
}

tab1, tab2 = st.tabs(["🎯 Product Recommendation", "👥 Customer Segmentation"])

# ──────────────────────────────────────────────────────────────────
# MODULE 1 — Product Recommendation
# ──────────────────────────────────────────────────────────────────
with tab1:
    st.markdown("### Find Similar Products")
    st.markdown("Enter a product name and get the **top 5 similar products** based on collaborative filtering (cosine similarity on customer purchase patterns).")

    product_input = st.text_input("Product Name", placeholder="e.g. WHITE HANGING HEART T-LIGHT HOLDER")
    get_rec = st.button("🔍 Get Recommendations", type="primary")

    if get_rec:
        if not product_input.strip():
            st.warning("Please enter a product name.")
        else:
            query = product_input.strip().upper()
            matches = [p for p in item_sim_df.columns if query in p]
            if not matches:
                st.warning(f"No product found matching '{product_input}'. Try a shorter keyword (e.g. 'HEART', 'MUG', 'BAG').")
            else:
                target = matches[0]
                sims = item_sim_df[target].drop(target).sort_values(ascending=False).head(5)
                st.success(f"Showing recommendations based on: **{target}**")
                for i, (prod, score) in enumerate(sims.items(), 1):
                    st.markdown(
                        f"<div class='rec-card'><b>{i}. {prod}</b><br>"
                        f"Similarity score: {score:.3f}</div>",
                        unsafe_allow_html=True,
                    )

# ──────────────────────────────────────────────────────────────────
# MODULE 2 — Customer Segmentation
# ──────────────────────────────────────────────────────────────────
with tab2:
    st.markdown("### Predict Customer Segment")
    st.markdown("Enter a customer's RFM values to predict which segment they belong to.")

    c1, c2, c3 = st.columns(3)
    recency = c1.number_input("Recency (days since last purchase)", min_value=0, value=30, step=1)
    frequency = c2.number_input("Frequency (number of past purchases)", min_value=1, value=3, step=1)
    monetary = c3.number_input("Monetary (total amount spent, £)", min_value=0.0, value=500.0, step=10.0)

    predict_btn = st.button("🎯 Predict Cluster", type="primary")

    if predict_btn:
        r_log = np.log1p(recency)
        f_log = np.log1p(frequency)
        m_log = np.log1p(monetary)
        X_new = scaler.transform([[r_log, f_log, m_log]])
        cluster_id = model.predict(X_new)[0]
        segment = label_map[cluster_id]
        color = SEGMENT_COLORS.get(segment, "#555")

        st.markdown(
            f"<span class='segment-badge' style='background:{color}'>{segment}</span>",
            unsafe_allow_html=True,
        )
        st.markdown("")
        st.info(SEGMENT_ADVICE.get(segment, ""))

        st.markdown("#### Input Summary")
        m1, m2, m3 = st.columns(3)
        m1.metric("Recency", f"{recency} days")
        m2.metric("Frequency", f"{frequency} orders")
        m3.metric("Monetary", f"£{monetary:,.2f}")

st.markdown("---")
st.caption("Built with Streamlit · KMeans Clustering (RFM) · Item-Based Collaborative Filtering")
