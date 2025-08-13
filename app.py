# HCP Dashboard Streamlit UI
# This file contains the Streamlit frontend for the HCP Targeting Optimization MVP

import streamlit as st
import pandas as pd
from hcp_utils import generate_hcp_data, rank_hcps, segment_hcps, channel_affinity

st.set_page_config(page_title="HCP Targeting Optimization Dashboard", layout="wide")

st.title("HCP Targeting Optimization MVP Dashboard")
st.markdown(
    """
    ### Welcome to the HCP Targeting Optimization Dashboard
    This app helps you identify, segment, and prioritize high-value Healthcare Professionals (HCPs) for marketing and sales outreach.\
    **Goal:** Focus your salesforce on top influencers and optimize channel strategy (email or in-person).
    
    **How it works:**
    - You can upload your own HCP Excel file (with columns: NPI Id, speciality, rx value, state_code, writing_behavior), or use the synthetic demo data provided.
    - The dashboard will automatically rank, segment, and analyze HCPs for you.
    """
)

# File uploader for user Excel file
st.sidebar.markdown(
    """
    **Upload your own HCP data:**
    - Upload an Excel file with columns: NPI Id, speciality, rx value, state_code, writing_behavior.
    - If you don't upload a file, demo data will be used.
    """
)
uploaded_file = st.sidebar.file_uploader("Upload HCP Excel File", type=["xlsx"])

if uploaded_file is not None:
    data = pd.read_excel(uploaded_file)
    st.success("Using your uploaded HCP data!")
else:
    data = generate_hcp_data()
    st.info("Using demo (synthetic) HCP data.")

# Rank and segment HCPs
data_ranked = rank_hcps(data)
data_segmented = segment_hcps(data_ranked)

affinity = channel_affinity(data_segmented)

# Show HCP data and provide download option
st.header("Current HCP Data")
st.markdown(
    """
    Below is the **active HCP data** being analyzed. You can download this table as an Excel file for your records or further analysis.
    """
)
st.dataframe(data, use_container_width=True)

# Download button
import io
output = io.BytesIO()
data.to_excel(output, index=False, engine='openpyxl')
st.download_button(
    label="Download HCP Data as Excel",
    data=output.getvalue(),
    file_name="hcp_data.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# =============================
# Analytics & Visualizations
# =============================
st.header("Analytics & Visualizations")
st.markdown(
    """
    Explore the distribution of HCPs by segmentation, specialty, state, and channel affinity. Use the search and filter options in the sidebar to drill down into specific HCPs or specialties.
    """
)

import plotly.express as px

# HCP Segmentation Distribution
st.markdown(
    """
    **HCP Segmentation Distribution**
    
    This bar chart shows how all HCPs are distributed across the three priority segments:
    - **Top 20%**: The most valuable HCPs based on prescription value and writing behavior.
    - **Middle 30%**: Moderately valuable HCPs.
    - **Bottom 50%**: Lower value HCPs.
    
    Use this chart to quickly see where most of your HCPs fall in terms of priority.
    """
)
seg_counts = data_segmented['segment'].value_counts().sort_index()
fig_seg = px.bar(x=seg_counts.index, y=seg_counts.values, labels={'x':'Segment', 'y':'Number of HCPs'}, title='HCP Segmentation Distribution')
st.plotly_chart(fig_seg, use_container_width=True)

# Specialty Distribution
st.markdown(
    """
    **Specialty Distribution**
    
    This pie chart displays the proportion of HCPs in each medical specialty. It helps you understand which specialties are most represented in your data and where your outreach may be most concentrated.
    """
)
spec_counts = data_segmented['speciality'].value_counts()
fig_spec = px.pie(names=spec_counts.index, values=spec_counts.values, title='Specialty Distribution')
st.plotly_chart(fig_spec, use_container_width=True)

# State-wise HCP Count
st.markdown(
    """
    **State-wise HCP Count**
    
    This bar chart shows the number of HCPs in each state. Use this to identify geographic concentrations and potential regional opportunities or gaps.
    """
)
state_counts = data_segmented['state_code'].value_counts()
fig_state = px.bar(x=state_counts.index, y=state_counts.values, labels={'x':'State', 'y':'Number of HCPs'}, title='State-wise HCP Count')
st.plotly_chart(fig_state, use_container_width=True)

# Channel Affinity Distribution
st.markdown(
    """
    **Channel Affinity Distribution**
    
    This bar chart shows how many HCPs are best reached via email versus in-person interactions. This helps you tailor your marketing and sales approach to match HCP preferences and maximize engagement.
    """
)
aff_counts = affinity['channel_affinity'].value_counts()
fig_aff = px.bar(x=aff_counts.index, y=aff_counts.values, labels={'x':'Channel', 'y':'Number of HCPs'}, title='Channel Affinity Distribution')
st.plotly_chart(fig_aff, use_container_width=True)

# Sidebar filters
st.sidebar.header("Filters & Search")

# Interactive search by NPI Id
search_npi = st.sidebar.text_input("Search by NPI Id")

# Specialty search
search_specialty = st.sidebar.text_input("Search by Specialty (type to filter)")

states = st.sidebar.multiselect("Select State(s)", options=data_segmented['state_code'].unique(), default=list(data_segmented['state_code'].unique()))
specialties = st.sidebar.multiselect("Select Speciality(ies)", options=data_segmented['speciality'].unique(), default=list(data_segmented['speciality'].unique()))

filtered_data = data_segmented[
    (data_segmented['state_code'].isin(states)) &
    (data_segmented['speciality'].isin(specialties))
]

if search_npi:
    filtered_data = filtered_data[filtered_data['NPI Id'].str.contains(search_npi, case=False, na=False)]
if search_specialty:
    filtered_data = filtered_data[filtered_data['speciality'].str.contains(search_specialty, case=False, na=False)]

st.header("HCP Segmentation and Priority List")
st.markdown(
    """
    **What is this?**
    - HCPs are ranked by their prescription value and writing behavior.
    - Segmentation tiers:
        - **Top 20%:** Highest value HCPs (focus for in-person outreach)
        - **Middle 30%:** Moderate value
        - **Bottom 50%:** Lower value (may focus on digital channels)
    - Use the filters on the left to refine the list by state or specialty.
    """
)
st.dataframe(filtered_data, use_container_width=True)

st.header("Channel Affinity (Email vs In-person)")
st.markdown(
    """
    **What is this?**
    - Based on specialty and writing behavior, each HCP is assigned a preferred marketing channel.
    - **In-person:** High-value or specialty-driven HCPs (e.g., Cardiology, Oncology, or high writers)
    - **Email:** Others, for efficient digital engagement.
    """
)
st.dataframe(affinity, use_container_width=True)
