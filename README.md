# 🛍️ Online Retail — Customer Segmentation (RFM) & Product Recommendation System

End-to-end ML project on **541,909 UK e-commerce transactions** (Dec 2010–Dec 2011): customers are segmented via **RFM + KMeans clustering**, and a **product recommendation engine** is built with item-based collaborative filtering — both deployed in an interactive **Streamlit app**.

---

## 📊 Dataset Summary

| Metric | Raw | After Cleaning |
|---|---|---|
| Rows | 541,909 | 392,692 |
| Unique customers | — | 4,338 |
| Unique products | — | ~3,900 |
| Countries | 38 | 37 |
| Date range | Dec 2010 – Dec 2011 | same |

**Cleaning steps applied:** dropped rows with missing `CustomerID`, removed cancelled invoices (`InvoiceNo` starting with 'C'), removed non-positive `Quantity`/`UnitPrice`, dropped duplicates.

---

## 🧠 Methodology

1. **EDA** — transaction volume by country, top-selling products, monthly revenue trend, monetary distribution per transaction/customer.
2. **RFM Feature Engineering** — Recency (days since last purchase), Frequency (# orders), Monetary (total spend) per customer, log-transformed to handle right-skew, then standardized.
3. **Cluster selection** — Elbow Method + Silhouette Score tested for k = 2–8. k=4 chosen as the best trade-off between statistical fit and **business-interpretable segments**.
4. **KMeans clustering** (k=4) → segments labeled by RFM averages: **Champions, Loyal/Regular, Occasional/New, At-Risk/Lost**.
5. **Item-based Collaborative Filtering** — cosine similarity on a Customer×Product purchase matrix → top-5 similar products for any input product.
6. **Model export** — clustering model + scaler + product similarity matrix saved as `.pkl` for Streamlit.

---

## 🏆 Customer Segment Results

| Segment | Avg Recency | Avg Frequency | Avg Monetary | % of Customers |
|---|---|---|---|---|
| **Champions (High-Value)** | 12 days | 13.8 orders | £8,088 | 16.4% |
| **Loyal / Regular** | 72 days | 4.1 orders | £1,802 | 26.9% |
| **Occasional / New** | 18 days | 2.2 orders | £557 | 19.3% |
| **At-Risk / Lost** | 182 days | 1.3 orders | £341 | 37.4% |

**Silhouette score (k=4): 0.337** — meaningful, well-separated segments suitable for differentiated marketing.

---

## 🎯 Recommendation System

- **Approach:** Item-based collaborative filtering, cosine similarity over a 4,338 × 3,289 customer–product purchase matrix
- **Example:** Querying *"WHITE HANGING HEART T-LIGHT HOLDER"* returns thematically and behaviorally related products (other hanging decor, gift-shop items) — confirming the model captures real co-purchase patterns, not noise

---

## 📱 Streamlit App

Two modules, exactly as specified in the brief:

| Module | Function |
|---|---|
| 🎯 Product Recommendation | Enter a product name → get top 5 similar products with similarity scores |
| 👥 Customer Segmentation | Enter Recency/Frequency/Monetary → instantly predict the customer's segment with tailored action advice |

### Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## 💡 Business Insights

1. **Revenue is highly concentrated.** Champions are only 16.4% of customers but represent the highest-value segment by a wide margin — a classic 80/20 pattern. Losing even a handful of these customers has outsized revenue impact.
2. **At-Risk/Lost is the *largest* segment (37.4%)** — over a third of the customer base has gone quiet (avg. 182 days since last purchase) after typically just one order. This is the biggest single source of revenue leakage in the dataset.
3. **The UK dominates transaction volume** (~89% of transactions), while Germany, France, and EIRE trail far behind — international markets are comparatively under-penetrated relative to their potential.
4. **Customer value is extremely right-skewed** (mean spend £2,049 vs. median £669) — a small number of bulk/wholesale buyers inflate averages. Segment medians, not the overall mean, should drive planning and forecasting.
5. **Product similarity clusters by theme** (decor with decor, novelty with novelty) — validating that the recommender can be trusted for cross-sell logic rather than producing arbitrary pairings.

---

## 🚀 What the Business Should Do to Grow From Here

| Priority | Action | Target Segment |
|---|---|---|
| **1 — Stop the bleeding** | Launch an automated win-back email/SMS flow (time-limited discount + "we miss you" messaging) triggered the moment a customer crosses ~90 days of inactivity — before they fully churn into the At-Risk bucket | At-Risk / Lost (37.4%) |
| **2 — Protect the core** | Build a VIP/loyalty tier for Champions (early access to new stock, free shipping threshold, dedicated support) — the cost of losing them is far higher than the cost of retaining them | Champions (16.4%) |
| **3 — Convert the middle** | Use the recommendation engine to power "customers who bought this also bought…" cross-sell prompts at checkout and in post-purchase emails, aimed at moving Loyal/Regular customers toward Champion-level frequency | Loyal / Regular (26.9%) |
| **4 — Build the habit early** | For Occasional/New customers, trigger a structured onboarding sequence (welcome offer → 2nd-purchase nudge → 3rd-purchase reward) in the first 30–60 days — the highest-leverage window before they convert to Loyal or fade to At-Risk | Occasional / New (19.3%) |
| **5 — Expand internationally** | Since the UK is saturated relative to other markets, run targeted acquisition campaigns in Germany, France, and Ireland where transaction share is disproportionately low compared to overall EU e-commerce demand | New customer acquisition |
| **6 — Operationalize the recommender** | Embed the product recommendation logic directly into the live storefront (product pages, cart, abandoned-cart emails) — not just as a standalone tool. This is where collaborative filtering converts to actual incremental revenue | All segments |
| **7 — Monitor, don't just snapshot** | Re-run RFM scoring monthly and track segment migration (e.g., what % of Loyal customers slip into At-Risk each month) — turns a one-time analysis into an early-warning system | All segments |

---

## 🛠️ Tech Stack

Python · Pandas · NumPy · Scikit-learn (KMeans, StandardScaler, cosine_similarity) · Matplotlib · Seaborn · Streamlit · Joblib

---

## 📁 Project Structure

```
online-retail-rfm-recommendation/
├── Online_Retail_RFM_Recommendation.ipynb   # Full notebook: EDA → RFM → Clustering → CF Recommender
├── app.py                                   # Streamlit app (2 modules)
├── rfm_kmeans_model.pkl                     # Saved KMeans model + scaler + segment labels
├── item_similarity_matrix.pkl               # Saved product-product cosine similarity matrix
├── rfm_customer_segments.csv                # Final customer-level RFM + segment table
├── clean_retail.csv                         # Cleaned transaction-level dataset
├── requirements.txt
└── README.md
```
