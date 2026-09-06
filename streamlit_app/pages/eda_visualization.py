import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from connection.db_connection import get_connection

st.title("📊 EDA Visualizations")

conn = get_connection()

literacy_df = pd.read_sql(
    "SELECT * FROM literacy_rates",
    conn
)

illiterate_population_Data = pd.read_sql(
    "SELECT * FROM illiteracy_population",
    conn
)

gdp_schooling_df = pd.read_sql(
    "SELECT * FROM gdp_schooling",
    conn
)

#eda visualization

st.subheader("📈 Literacy vs Illiteracy Trend")

trend_df = (
    illiterate_population_Data
    .groupby("year")[["literacy_pct", "illiteracy_pct"]]
    .mean()
    .reset_index()
)

fig, ax = plt.subplots(figsize=(10,5))

sns.lineplot(
    data=trend_df,
    x="year",
    y="literacy_pct",
    label="Literacy %",
    ax=ax
)

sns.lineplot(
    data=trend_df,
    x="year",
    y="illiteracy_pct",
    label="Illiteracy %",
    ax=ax
)

st.pyplot(fig) #Literacy vs Illiteracy Trend

st.subheader("👨‍🎓 Adult vs Youth Literacy")

compare_df = literacy_df.copy()

fig, ax = plt.subplots(figsize=(8,5))

sns.scatterplot(
    data=compare_df,
    x="adult_literacy_rate",
    y="young_literacy_average",
    ax=ax
)

st.pyplot(fig) #Adult vs Youth Literacy Gap

st.subheader("⚖️ Male vs Female Youth Literacy")

fig, ax = plt.subplots(figsize=(8,5))

sns.scatterplot(
    data=literacy_df,
    x="youth_literacy_rate_male",
    y="youth_literacy_rate_female",
    ax=ax
)

st.pyplot(fig) #Gender Disparities in Literacy

st.subheader("💰 Literacy vs GDP Per Capita")

fig, ax = plt.subplots(figsize=(8,5))

sns.scatterplot(
    data=gdp_schooling_df,
    x="gdp_percapita",
    y="literacy_pct",
    ax=ax
)

st.pyplot(fig) #Literacy vs GDP Per Capita

st.subheader("📚 Schooling Years vs Literacy")

fig, ax = plt.subplots(figsize=(8,5))

sns.scatterplot(
    data=gdp_schooling_df,
    x="average_years_of_education",
    y="literacy_pct",
    ax=ax
)

st.pyplot(fig) #Schooling Years vs Literacy

st.subheader("🏆 Top 10 Literacy Countries")

top10 = literacy_df.nlargest(
    10,
    "adult_literacy_rate"
)

fig, ax = plt.subplots(figsize=(10,5))

sns.barplot(
    data=top10,
    x="entity",
    y="adult_literacy_rate",
    ax=ax
)

plt.xticks(rotation=45)

st.pyplot(fig) #Top & Bottom Literacy Countries

st.subheader("📉 Bottom 10 Literacy Countries")

bottom10 = literacy_df.nsmallest(
    10,
    "adult_literacy_rate"
)

fig, ax = plt.subplots(figsize=(10,5))

sns.barplot(
    data=bottom10,
    x="entity",
    y="adult_literacy_rate",
    ax=ax
)

plt.xticks(rotation=45)

st.pyplot(fig) #Top & Bottom Literacy Countries

st.subheader("🌍 Literacy by Region")

region_df = (
    literacy_df
    .groupby("owid_region")["adult_literacy_rate"]
    .mean()
    .reset_index()
)

fig, ax = plt.subplots(figsize=(10,5))

sns.barplot(
    data=region_df,
    x="owid_region",
    y="adult_literacy_rate",
    ax=ax
)

plt.xticks(rotation=45)

st.pyplot(fig) #Regional Literacy Patterns

st.subheader("👥 Illiteracy vs Population")

fig, ax = plt.subplots(figsize=(8,5))

sns.scatterplot(
    data=gdp_schooling_df,
    x="population_historical",
    y="literacy_pct",
    ax=ax
)

st.pyplot(fig) #Illiteracy vs Population Size

st.subheader("🔥 Correlation Heatmap")

corr_df = gdp_schooling_df[
    [
        "gdp_percapita",
        "average_years_of_education",
        "literacy_pct",
        "gdp_per_schooling_year",
        "education_index"
    ]
]

fig, ax = plt.subplots(figsize=(8,5))

sns.heatmap(
    corr_df.corr(),
    annot=True,
    ax=ax
)

st.pyplot(fig) #Correlation Heatmap (Bonus)