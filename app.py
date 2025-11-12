import streamlit as st
import pandas as pd
import plotly.express as px

# === Page Setup ===
st.set_page_config(page_title="AI Talent Success Dashboard", layout="wide")
st.title("💡 AI Talent Success Dashboard")

# === Input Section ===
st.header("1️⃣ Role Information")
role_name = st.text_input("Role Name", placeholder="e.g. Data Analyst Intern")
job_level = st.selectbox("Job Level", ["Intern", "Junior", "Mid", "Senior", "Manager", "Director"])
role_purpose = st.text_area("Role Purpose", placeholder="Describe the purpose of the role here...")

benchmark_ids = st.multiselect("Select Benchmark Employee IDs", ["E001","E002","E003","E004","E005"])

if st.button("Generate Success Analysis"):
    # === Load Data ===
    profiles_url = "https://docs.google.com/spreadsheets/d/1BuOG4dbw8zy6z36W41qyhOblG3UkscPFSehcRQjOtC4/export?format=csv&gid=711778799"
    performance_url = "https://docs.google.com/spreadsheets/d/1BuOG4dbw8zy6z36W41qyhOblG3UkscPFSehcRQjOtC4/export?format=csv&gid=422937119"
    
    profiles = pd.read_csv(profiles_url)
    performance = pd.read_csv(performance_url)
    
    # === Compute New Benchmark ===
    benchmark = profiles[profiles["employee_id"].isin(benchmark_ids)].mean(numeric_only=True)
    profiles["cognitive_match"] = 1 - abs(profiles["iq"] - benchmark["iq"]) / benchmark["iq"]
    profiles["gtq_match"] = 1 - abs(profiles["gtq"] - benchmark["gtq"]) / benchmark["gtq"]
    profiles["success_score"] = 0.5 * profiles["cognitive_match"] + 0.5 * profiles["gtq_match"]

    # === Visualizations ===
    st.subheader("2️⃣ Success Score Distribution")
    fig = px.histogram(profiles, x="success_score", nbins=15, color_discrete_sequence=['#2563EB'])
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("3️⃣ Top 10 Employees by Success Score")
    top10 = profiles.sort_values("success_score", ascending=False).head(10)
    st.dataframe(top10[["employee_id", "iq", "gtq", "success_score"]])

    st.subheader("4️⃣ Narrative Insight")
    top3 = top10.head(3)
    st.markdown(f"For the role **{role_name} ({job_level})**, top-aligned employees are:")
    for _, row in top3.iterrows():
        st.markdown(f"- `{row['employee_id']}` — SuccessScore: **{row['success_score']:.3f}**")
