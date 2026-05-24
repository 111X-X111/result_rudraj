import streamlit as st
import pandas as pd
from supabase import create_client

# 🔑 SUPABASE CONFIG

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# 📥 FETCH DATA
def fetch_data():
    response = supabase.table("results").select("*").execute()
    data = response.data
    return pd.DataFrame(data)


# 🎯 MAIN APP
st.set_page_config(page_title="📊 Dashboard", layout="wide")

st.title("📊 Test Performance Dashboard")

df = fetch_data()

if df.empty:
    st.warning("⚠️ No data found")
else:
    st.success("✅ Data Loaded from Supabase")

    # 📋 SHOW TABLE
    st.subheader("📋 All Test Data")
    st.dataframe(df, use_container_width=True)

    # 📈 BASIC STATS
    st.subheader("📈 Overall Performance")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Tests", len(df))
    col2.metric("Avg Accuracy", round(df["total_accuracy"].mean(), 2))
    col3.metric("Best Score", df["total_correct"].max())

    # 📊 GRAPH
    st.subheader("📊 Accuracy Trend")

    df_sorted = df.sort_values("test_no")

    st.line_chart(df_sorted.set_index("test_no")["total_accuracy"])

    # 🧪 SUBJECT ANALYSIS
    st.subheader("📚 Subject Analysis")

    subject = st.selectbox("Select Subject", ["Physics", "Chemistry", "Maths"])

    if subject == "Physics":
        st.line_chart(df_sorted.set_index("test_no")["phy_accuracy"])
    elif subject == "Chemistry":
        st.line_chart(df_sorted.set_index("test_no")["chem_accuracy"])
    else:
        st.line_chart(df_sorted.set_index("test_no")["math_accuracy"])