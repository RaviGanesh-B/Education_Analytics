import streamlit as st
import pandas as pd
from connection.db_connection import get_connection

st.title("🧮 SQL Query Executor")

conn = get_connection()

queries = {

    "1. Top 5 countries with highest adult literacy in 2020":
    """
    SELECT entity, adult_literacy_rate
    FROM literacy_rates
    WHERE year = 2020
    ORDER BY adult_literacy_rate DESC
    LIMIT 5;
    """,

    "2. Countries where female youth literacy < 80%":
    """
    SELECT entity,
       year,
       youth_literacy_rate_female
    FROM literacy_rates
    WHERE youth_literacy_rate_female < 80
    ORDER BY youth_literacy_rate_female;
    """,

    "3. Average adult literacy per continent":
    """
    SELECT owid_region,
       ROUND(AVG(adult_literacy_rate), 2) AS avg_adult_literacy
    FROM literacy_rates
    GROUP BY owid_region
    ORDER BY avg_adult_literacy DESC;
    """,

    #literacy rates queries done

    "4. Countries with illiteracy % > 20% in 2000":
    """
    SELECT entity,
       illiteracy_pct
    FROM illiteracy_population
    WHERE year = 2000
    AND illiteracy_pct > 20
    ORDER BY illiteracy_pct DESC;
    """,

    "5. Trend of illiteracy % for India (2000–2020)":
    """
    SELECT year, illiteracy_pct
    FROM illiteracy_population
    WHERE entity = 'India'
    AND year BETWEEN 2000 AND 2020
    ORDER BY year;
    """,

    "6. Top 10 countries with largest illiteracy % in latest year":
    """
    SELECT entity,
       illiteracy_pct
    FROM illiteracy_population
    WHERE year = (
    SELECT MAX(year)
    FROM illiteracy_population
    )
    ORDER BY illiteracy_pct DESC
    LIMIT 10;
    """,

    #illiteraccy population

    "7. Schooling > 7 and GDP < 5000":
    """
    SELECT entity,
       year,
       average_years_of_education,
       gdp_percapita
    FROM gdp_schooling
    WHERE average_years_of_education > 7
    AND gdp_percapita < 5000
    ORDER BY average_years_of_education DESC;
    """,

    "8. GDP per schooling ranking (2020)":
    """
    SELECT entity,
       gdp_per_schooling_year,
       RANK() OVER(
           ORDER BY gdp_per_schooling_year DESC
       ) AS ranking
    FROM gdp_schooling
    WHERE year = 2020;
    """,

    "9. Global average schooling years per year":
    """
    SELECT year,
       ROUND(AVG(average_years_of_education),2)
       AS avg_schooling_years
    FROM gdp_schooling
    GROUP BY year
    ORDER BY year;
    """,

    #gdp schooling queries done

    "10. High GDP but schooling < 6":
    """
    SELECT entity,
       gdp_percapita,
       average_years_of_education
    FROM gdp_schooling
    WHERE year = 2020
    AND average_years_of_education < 6
    ORDER BY gdp_percapita DESC
    LIMIT 10;
    """,

    "11. High illiteracy despite >10 years schooling":
    """
    SELECT g.entity,
       g.year,
       g.average_years_of_education,
       i.illiteracy_pct
    FROM gdp_schooling g
    JOIN illiteracy_population i
    ON g.entity = i.entity
    AND g.year = i.year
    WHERE g.average_years_of_education > 10
    AND i.illiteracy_pct > 20
    ORDER BY i.illiteracy_pct DESC;
    """,

    "12. India literacy vs GDP trend":
    """
    SELECT year,
       literacy_pct,
       gdp_percapita
    FROM gdp_schooling
    WHERE entity = 'India'
    AND year BETWEEN 2000 AND 2020
    ORDER BY year;
    """,

    "13. Gender gap for GDP > 30000 (2020)":
    """
    SELECT l.entity,
       g.gdp_percapita,
       l.youth_literacy_rate_male,
       l.youth_literacy_rate_female,
       ABS(
           l.youth_literacy_rate_male -
           l.youth_literacy_rate_female
       ) AS literacy_gap
    FROM literacy_rates l
    JOIN gdp_schooling g
    ON l.entity = g.entity
    AND l.year = g.year
    WHERE g.year = 2020
    AND g.gdp_percapita > 30000
    ORDER BY literacy_gap DESC;
    """
    #join queries done
}

selected_query = st.selectbox(
    "Select Query",
    list(queries.keys())
)

if st.button("Execute Query"):

    df = pd.read_sql(
        queries[selected_query],
        conn
    )

    st.dataframe(
        df,
        use_container_width=True
    )