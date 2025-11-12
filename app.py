import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime

st.set_page_config(page_title="AI Talent Success Dashboard", layout="wide")
st.title("💡 AI Talent Success Dashboard")

# === Input Section ===
st.header("1️⃣ Role Information")
role_name = st.text_input("Role Name", placeholder="e.g. Data Analyst")
job_level = st.selectbox("Job Level", ["Intern", "Junior", "Mid", "Senior", "Manager"])
role_purpose = st.text_area("Role Purpose", placeholder="Briefly describe this role’s goal...")
benchmark_ids = st.multiselect("Select Benchmark Employee IDs", ["E001","E002","E003","E004","E005"])

if st.button("Generate Job Profile & Dashboard"):

    # 1️⃣ Simulate job_vacancy_id
    job_vacancy_id = int(datetime.now().timestamp())
    st.success(f"📄 Job Vacancy ID: {job_vacancy_id}")

    # 2️⃣ Load data
    profiles_url = "https://docs.google.com/spreadsheets/d/1BuOG4dbw8zy6z36W41qyhOblG3UkscPFSehcRQjOtC4/export?format=csv&gid=711778799"
    performance_url = "https://docs.google.com/spreadsheets/d/1BuOG4dbw8zy6z36W41qyhOblG3UkscPFSehcRQjOtC4/export?format=csv&gid=422937119"

    profiles = pd.read_csv(profiles_url)
    performance = pd.read_csv(performance_url)

    # 3️⃣ Compute Benchmark
    benchmark = profiles[profiles["employee_id"].isin(benchmark_ids)].mean(numeric_only=True)
    profiles["cognitive_match"] = 1 - abs(profiles["iq"] - benchmark["iq"]) / benchmark["iq"]
    profiles["gtq_match"] = 1 - abs(profiles["gtq"] - benchmark["gtq"]) / benchmark["gtq"]
    profiles["success_score"] = 0.5 * profiles["cognitive_match"] + 0.5 * profiles["gtq_match"]

    # 4️⃣ AI-Generated Job Profile (LLM simulation)
    st.subheader("🤖 AI-Generated Job Profile")
    st.markdown(f"**Role Name:** {role_name}  \n**Job Level:** {job_level}")
    st.write(f"**Role Purpose:** {role_purpose}")
    st.markdown("""
    **Key Requirements:**
    - Strong analytical and problem-solving skills  
    - Proficiency in data visualization and storytelling  
    - Ability to derive actionable insights from complex datasets  
    - Excellent communication and stakeholder management skills
    """)

    # 5️⃣ Dashboard Visualizations
    st.subheader("📊 Dashboard Visualization")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Success Score Distribution**")
        fig = px.histogram(profiles, x="success_score", nbins=15,
                           title="Success Score Distribution",
                           color_discrete_sequence=["#2563EB"])
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.write("**Top 10 Employees by Success Score**")
        top10 = profiles.sort_values("success_score", ascending=False).head(10)
        st.dataframe(top10[["employee_id", "iq", "gtq", "success_score"]])

    # 6️⃣ Narrative Summary
    st.subheader("🧠 Summary Insight")
    top3 = top10.head(3)
    st.markdown(f"For the role **{role_name} ({job_level})**, top aligned employees are:")
    for _, row in top3.iterrows():
        st.markdown(f"- `{row['employee_id']}` — SuccessScore: **{row['success_score']:.3f}**")

    avg_score = profiles["success_score"].mean()
    st.info(f"Average SuccessScore across all employees: **{avg_score:.3f}**")

    st.markdown("""
    **Interpretation:**  
    Employees achieving higher SuccessScore show stronger alignment with benchmarked competencies.  
    Use this dashboard to identify potential role fits, development needs, or leadership pipeline candidates.
    """)
