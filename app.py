import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("🎬 Netflix Data Dashboard")

# Upload CSV
uploaded_file = st.file_uploader("netflix_titles", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("Dataset Preview")
    st.write(df.head())

    # --- CLEANING ---
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
    df['year_added'] = df['date_added'].dt.year

    df['duration_num'] = df['duration'].astype(str).str.extract(r'(\d+)').astype(float)

    # --- SIDEBAR FILTERS ---
    st.sidebar.header("Filters")

    type_filter = st.sidebar.multiselect("Select Type", df['type'].unique(), default=df['type'].unique())
    country_filter = st.sidebar.multiselect("Select Country", df['country'].dropna().unique())

    filtered_df = df[df['type'].isin(type_filter)]

    if country_filter:
        filtered_df = filtered_df[filtered_df['country'].isin(country_filter)]

    # --- KPI ---
    st.subheader("Key Metrics")
    col1, col2, col3 = st.columns(3)

    col1.metric("Total Titles", len(filtered_df))
    col2.metric("Movies", len(filtered_df[filtered_df['type'] == 'Movie']))
    col3.metric("TV Shows", len(filtered_df[filtered_df['type'] == 'TV Show']))

    # --- CHART 1: Movies vs TV Shows ---
    st.subheader("Movies vs TV Shows")
    fig1, ax1 = plt.subplots()
    filtered_df['type'].value_counts().plot(kind='bar', ax=ax1)
    st.pyplot(fig1)

    # --- CHART 2: Growth Over Time ---
    st.subheader("Content Growth Over Time")
    yearly = filtered_df['year_added'].value_counts().sort_index()

    fig2, ax2 = plt.subplots()
    yearly.plot(kind='line', ax=ax2)
    st.pyplot(fig2)

    # --- CHART 3: Top Countries ---
    st.subheader("Top Countries")
    top_countries = filtered_df['country'].value_counts().head(10)

    fig3, ax3 = plt.subplots()
    top_countries.plot(kind='bar', ax=ax3)
    st.pyplot(fig3)

    # --- CHART 4: Duration Distribution (Movies only) ---
    st.subheader("Movie Duration Distribution")
    movies = filtered_df[filtered_df['type'] == 'Movie']

    fig4, ax4 = plt.subplots()
    movies['duration_num'].dropna().plot(kind='hist', bins=20, ax=ax4)
    st.pyplot(fig4)