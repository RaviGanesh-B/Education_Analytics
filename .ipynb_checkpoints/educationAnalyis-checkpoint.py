import streamlit as st
import pandas as pd
import pymysql
from streamlit_option_menu import option_menu
import seaborn as sns
import matplotlib.pyplot as plt

#connection

def get_connection():
    conn = pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password="goku",
        database="education_analysis"
    )

    return conn

#home page

st.set_page_config(
    page_title="Global Literacy Analytics",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Global Literacy Analytics Dashboard")

st.markdown("""
### Welcome

This dashboard analyzes:

- Literacy Rates
- Illiteracy Rates
- GDP Per Capita
- Education Index
- Schooling Years

using Python, MySQL and Streamlit.
""")

