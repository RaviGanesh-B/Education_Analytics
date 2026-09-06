import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from connection.db_connection import get_connection

st.set_page_config(
    page_title="Country Profile",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Country Profile")

# Database Connection

conn = get_connection()

# Load Data

literacy_df = pd.read_sql(
    "SELECT * FROM literacy_rates",
    conn
)

gdp_schooling_df = pd.read_sql(
    "SELECT * FROM gdp_schooling",
    conn
)

illiterate_population_Data = pd.read_sql(
    "SELECT * FROM illiteracy_population",
    conn
)

# Data Cleaning

literacy_df["entity"] = literacy_df["entity"].astype(str).str.strip()
gdp_schooling_df["entity"] = gdp_schooling_df["entity"].astype(str).str.strip()
illiterate_population_Data["entity"] = illiterate_population_Data["entity"].astype(str).str.strip()

literacy_df["year"] = pd.to_numeric(
    literacy_df["year"],
    errors="coerce"
)

gdp_schooling_df["year"] = pd.to_numeric(
    gdp_schooling_df["year"],
    errors="coerce"
)

illiterate_population_Data["year"] = pd.to_numeric(
    illiterate_population_Data["year"],
    errors="coerce"
)

# Helper Function

def get_value(df, column):

    if df.empty:
        return "N/A"

    if column not in df.columns:
        return "N/A"

    value = df[column].iloc[0]

    if pd.isna(value):
        return "N/A"

    try:
        return round(float(value), 2)
    except:
        return value
        
# Country Selection

common_countries = sorted(
    list(
        set(literacy_df["entity"])
        & set(gdp_schooling_df["entity"])
        & set(illiterate_population_Data["entity"])
    )
)

if len(common_countries) == 0:
    st.error("No common countries found.")
    st.stop()

selected_country = st.selectbox(
    "🌍 Select Country",
    common_countries
)

# Year Selection

literacy_years = set(
    literacy_df[
        literacy_df["entity"] == selected_country
    ]["year"]
)

gdp_years = set(
    gdp_schooling_df[
        gdp_schooling_df["entity"] == selected_country
    ]["year"]
)

illiteracy_years = set(
    illiterate_population_Data[
        illiterate_population_Data["entity"] == selected_country
    ]["year"]
)

common_years = sorted(
    list(
        literacy_years
        & gdp_years
        & illiteracy_years
    )
)

if len(common_years) == 0:
    st.warning(
        f"No common year data available for {selected_country}"
    )
    st.stop()

selected_year = st.selectbox(
    "📅 Select Year",
    common_years
)

# Selected Records

literacy_row = literacy_df[
    (literacy_df["entity"] == selected_country)
    &
    (literacy_df["year"] == selected_year)
]

gdp_row = gdp_schooling_df[
    (gdp_schooling_df["entity"] == selected_country)
    &
    (gdp_schooling_df["year"] == selected_year)
]

illiteracy_row = illiterate_population_Data[
    (illiterate_population_Data["entity"] == selected_country)
    &
    (illiterate_population_Data["year"] == selected_year)
]

# KPI Section

st.subheader("📊 Key Indicators")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "📚 Adult Literacy",
        get_value(
            literacy_row,
            "adult_literacy_rate"
        )
    )

with col2:
    st.metric(
        "👨‍🎓 Youth Literacy Avg",
        get_value(
            literacy_row,
            "young_literacy_average"
        )
    )

with col3:
    st.metric(
        "⚖️ Gender Gap",
        get_value(
            literacy_row,
            "young_literacy_gender_gap"
        )
    )

col4, col5, col6 = st.columns(3)

with col4:
    st.metric(
        "💰 GDP Per Capita",
        get_value(
            gdp_row,
            "gdp_percapita"
        )
    )

with col5:
    st.metric(
        "🎓 Schooling Years",
        get_value(
            gdp_row,
            "average_years_of_education"
        )
    )

with col6:
    st.metric(
        "📈 Education Index",
        get_value(
            gdp_row,
            "education_index"
        )
    )

col7, col8 = st.columns(2)

with col7:
    st.metric(
        "✅ Literacy %",
        get_value(
            illiteracy_row,
            "literacy_pct"
        )
    )

with col8:
    st.metric(
        "❌ Illiteracy %",
        get_value(
            illiteracy_row,
            "illiteracy_pct"
        )
    )

# ----------------------------
# Historical Data
# ----------------------------

country_literacy = literacy_df[
    literacy_df["entity"] == selected_country
]

country_gdp = gdp_schooling_df[
    gdp_schooling_df["entity"] == selected_country
]

# Adult Literacy Trend

if not country_literacy.empty:

    st.subheader("📈 Adult Literacy Trend")

    fig, ax = plt.subplots(figsize=(10, 5))

    sns.lineplot(
        data=country_literacy,
        x="year",
        y="adult_literacy_rate",
        marker="o",
        ax=ax
    )

    ax.set_title(
        f"Adult Literacy Trend - {selected_country}"
    )

    st.pyplot(fig)
    
# GDP Trend

if not country_gdp.empty:

    st.subheader("💰 GDP Per Capita Trend")

    fig, ax = plt.subplots(figsize=(10, 5))

    sns.lineplot(
        data=country_gdp,
        x="year",
        y="gdp_percapita",
        marker="o",
        ax=ax
    )

    ax.set_title(
        f"GDP Per Capita Trend - {selected_country}"
    )

    st.pyplot(fig)

# Schooling Trend

if not country_gdp.empty:

    st.subheader("🎓 Schooling Years Trend")

    fig, ax = plt.subplots(figsize=(10, 5))

    sns.lineplot(
        data=country_gdp,
        x="year",
        y="average_years_of_education",
        marker="o",
        ax=ax
    )

    ax.set_title(
        f"Schooling Years Trend - {selected_country}"
    )

    st.pyplot(fig)

# Male vs Female Literacy

if not country_literacy.empty:

    st.subheader("⚖️ Male vs Female Youth Literacy")

    fig, ax = plt.subplots(figsize=(10, 5))

    sns.lineplot(
        data=country_literacy,
        x="year",
        y="youth_literacy_rate_male",
        marker="o",
        label="Male",
        ax=ax
    )

    sns.lineplot(
        data=country_literacy,
        x="year",
        y="youth_literacy_rate_female",
        marker="o",
        label="Female",
        ax=ax
    )

    ax.set_title(
        f"Youth Literacy Comparison - {selected_country}"
    )

    st.pyplot(fig)

# Education Index Trend

if not country_gdp.empty:

    st.subheader("📚 Education Index Trend")

    fig, ax = plt.subplots(figsize=(10, 5))

    sns.lineplot(
        data=country_gdp,
        x="year",
        y="education_index",
        marker="o",
        ax=ax
    )

    ax.set_title(
        f"Education Index Trend - {selected_country}"
    )

    st.pyplot(fig)