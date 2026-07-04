# 🛍️ Online Retail — Customer Segmentation & Product Recommendation

> End-to-end machine learning project on **541,909 UK e-commerce transactions** (Dec 2010 – Dec 2011): customers segmented via **RFM + K-Means clustering**, paired with an **item-based collaborative filtering** recommendation engine — both deployed in an interactive **Streamlit app**.

---

## 🚀 Live App

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](YOUR_STREAMLIT_LINK_HERE)

---

## 📊 Dataset Summary

| Metric | Raw | After Cleaning |
|--------|-----|----------------|
| Rows | 541,909 | 392,692 |
| Unique Customers | — | 4,338 |
| Unique Products | — | 3,866 |
| Countries | 38 | 37 |
| Date Range | Dec 2010 – Dec 2011 | same |

---

## 🧠 Methodology

1. **Data Cleaning** — Dropped missing CustomerIDs, removed cancellations, non-positive quantities/prices, and duplicates
2. **EDA** — Transaction volume by country, top-selling products, revenue distribution
3. **RFM Feature Engineering** — Recency, Frequency, Monetary per customer — log-transformed and standardized
4. **Cluster Selection** — Silhouette score tested for k = 2–8 → **k=4 chosen** (score: 0.3375)
5. **K-Means Clustering** → 4 segments labeled by RFM averages
6. **Item-Based Collaborative Filtering** — Cosine similarity on a 4,338 × 3,289 customer-product matrix

---

## 🏆 Customer Segment Results

| Segment | Avg Recency | Avg Frequency | Avg Monetary | % of Customers |
|---------|-------------|---------------|--------------|----------------|
| **Champions (High-Value)** | 12 days | 13.8 orders | £8,088 | 16.4% |
| **Loyal / Regular** | 72 days | 4.1 orders | £1,802 | 26.9% |
| **Occasional / New** | 18 days | 2.2 orders | £557 | 19.3% |
| **At-Risk / Lost** | 182 days | 1.3 orders | £341 | 37.4% |

---

## 🎯 Recommendation System

- **Approach:** Item-based collaborative filtering, cosine similarity
- **Matrix:** 4,338 customers × 3,289 products (products with ≥5 purchases)
- **Example:** Querying *"WHITE HANGING HEART T-LIGHT HOLDER"* returns:
  1. GIN + TONIC DIET METAL SIGN — 0.750
  2. RED HANGING HEART T-LIGHT HOLDER — 0.659
  3. WASHROOM METAL SIGN — 0.644
  4. LAUNDRY 15C METAL SIGN — 0.642
  5. GREEN VINTAGE SPOT BEAKER — 0.631

---

## 📱 Streamlit App — Two Modules

| Module | Function |
|--------|----------|
| 🎯 Product Recommendation | Enter a product name → get top 5 similar products with similarity scores |
| 👥 Customer Segmentation | Enter Recency / Frequency / Monetary → predict customer segment with action advice |

### Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## 💡 Key Business Insights

1. **Champions are only 16.4%** of customers but spend 14× more than At-Risk customers on average
2. **At-Risk/Lost is the largest segment (37.4%)** — over a third of customers have gone quiet
3. **UK dominates (~89% of transactions)** — Germany, France, Ireland are under-penetrated
4. **Mean spend £2,049 vs median £669** — a small number of bulk buyers inflate the average

---

## 🚀 7-Point Growth Roadmap

| Priority | Action | Target |
|----------|--------|--------|
| 1 | Automated win-back flow at 90 days inactivity | At-Risk / Lost |
| 2 | VIP loyalty tier — early access, free shipping | Champions |
| 3 | Cross-sell prompts at checkout using recommender | Loyal / Regular |
| 4 | Onboarding sequence in first 30–60 days | Occasional / New |
| 5 | Targeted acquisition in Germany, France, Ireland | New Markets |
| 6 | Embed recommender in live storefront + emails | All Segments |
| 7 | Re-run RFM monthly — track segment migration | All Segments |

---

## 📁 Project Structure

```
online-retail-rfm-recommendation/
├── app.py                                   # Streamlit app
├── rfm_kmeans_model.pkl                     # KMeans model + scaler + labels
├── item_similarity_matrix.pkl               # Product-product similarity matrix
├── rfm_customer_segments.csv               # Customer RFM + segment table
├── Online_Retail_RFM_Recommendation.ipynb  # Full analysis notebook
├── Retail_Intelligence_Pro.pptx            # Project presentation
├── requirements.txt
└── README.md
```

---

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-F7931E?style=flat&logo=scikit-learn&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=flat&logo=jupyter&logoColor=white)

**Libraries:** Pandas · NumPy · Scikit-learn · Matplotlib · Seaborn · Streamlit · Joblib
