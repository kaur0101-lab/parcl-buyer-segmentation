import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Setup
st.set_page_config(page_title="Parcl Real Estate Intelligence", layout="wide")

st.title("Real Estate Buyer Intelligence & Profiling Dashboard")
st.markdown("### Market Intelligence Dashboard | **Unified Mentor × Parcl Co. Limited**")

# 2. Load Processed Dataset
@st.cache_data
def load_data():
    return pd.read_csv("processed_buyer_clusters.csv")

try:
    df = load_data()
except Exception as e:
    st.error("Processed file 'processed_buyer_clusters.csv' not found. Please run your data cleaning and clustering cells first!")
    st.stop()

# 3. User Controls (Sidebar Filters)
st.sidebar.header("Dashboard Filters")
selected_country = st.sidebar.multiselect("Select Country", options=df['country'].unique(), default=df['country'].unique())
selected_region = st.sidebar.multiselect("Select Region", options=df['region'].unique(), default=df['region'].unique())
selected_purpose = st.sidebar.multiselect("Acquisition Purpose", options=df['acquisition_purpose'].unique(), default=df['acquisition_purpose'].unique())
selected_type = st.sidebar.multiselect("Client Type", options=df['client_type'].unique(), default=df['client_type'].unique())

# Apply Filters
filtered_df = df[
    (df['country'].isin(selected_country)) &
    (df['region'].isin(selected_region)) &
    (df['acquisition_purpose'].isin(selected_purpose)) &
    (df['client_type'].isin(selected_type))
]

# 4. Dashboard Modules
col1, col2 = st.columns(2)

with col1:
    st.subheader("Buyer Segmentation Overview")
    fig_pie = px.pie(filtered_df, names='segment_name', hole=0.4, title="Cluster Share Distribution", color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    st.subheader("Investor Behavior Dashboard")
    fig_loan = px.histogram(filtered_df, x='segment_name', color='loan_applied', barmode='group', title="Loan Applications across Segments")
    st.plotly_chart(fig_loan, use_container_width=True)

st.subheader("Geographic Buyer Analysis")
top_10_regions = df['region'].value_counts().nlargest(10).index
filtered_region_df = df[df['region'].isin(top_10_regions)]

fig_region = px.histogram(
    filtered_region_df,
    y="region",
    color="segment_name",
    title="Top 10 Regions by Buyer Segment",
    orientation='h'
)

fig_region.update_layout(
    yaxis={'categoryorder': 'total ascending'},
    xaxis_title="Number of Buyers",
    yaxis_title="Region",
    legend_title="Segment",
    template="plotly_dark"
)

st.plotly_chart(fig_region, use_container_width=True)

st.subheader("Segment Insights Panel")
insights = filtered_df.groupby('segment_name').agg(
    Total_Clients=('client_id', 'count'),
    Average_Age=('age', 'mean'),
    Avg_Satisfaction=('satisfaction_score', 'mean')
).reset_index()

st.dataframe(insights.style.highlight_max(axis=0), use_container_width=True)
