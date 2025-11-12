
import streamlit as st
import pandas as pd

# Load data
industries = pd.read_csv("industries.csv")

st.set_page_config(page_title="Invoice Finance Suitability", layout="wide")
st.title("Invoice Finance Industry Suitability")

# Sidebar filters
st.sidebar.header("Filters")
search_query = st.sidebar.text_input("Search Industry")

level1_options = sorted(industries['Level1'].dropna().unique())
selected_level1 = st.sidebar.selectbox("Select Level 1", ["All"] + level1_options)

filtered = industries.copy()
if selected_level1 != "All":
    filtered = filtered[filtered['Level1'] == selected_level1]

level2_options = sorted(filtered['Level2'].dropna().unique())
selected_level2 = st.sidebar.selectbox("Select Level 2", ["All"] + level2_options)
if selected_level2 != "All":
    filtered = filtered[filtered['Level2'] == selected_level2]

level3_options = sorted(filtered['Description'].dropna().unique())
selected_level3 = st.sidebar.selectbox("Select Level 3", ["All"] + level3_options)
if selected_level3 != "All":
    filtered = filtered[filtered['Description'] == selected_level3]

# Apply search filter
if search_query:
    filtered = filtered[filtered['Description'].str.contains(search_query, case=False, na=False)]

# Reset button
if st.sidebar.button("Reset Filters"):
    filtered = industries.copy()

# Summary counts
st.subheader("Summary of Suitability")
st.write(filtered['Suitability'].value_counts())

# Display table with color-coded badges
st.subheader("Industry List")
for idx, row in filtered.iterrows():
    color = "green" if row['Suitability'] == "Green" else "orange" if row['Suitability'] == "Amber" else "red"
    st.markdown(f"<div style='padding:10px;border:1px solid #ccc;margin-bottom:5px;'>"
                f"<b>{row['Description']}</b> | Level1: {row['Level1']} | Level2: {row['Level2']} "
                f"<span style='color:{color};font-weight:bold;'>[{row['Suitability']}]</span></div>", unsafe_allow_html=True)

# Download filtered results
st.download_button("Download Filtered Results", filtered.to_csv(index=False), "filtered_industries.csv")
