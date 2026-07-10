import streamlit as st
import pandas as pd
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

def generate_hr_insights(data_summary: str):
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    prompt = f"""You are an expert HR analyst. Below is a summary of workforce data from an organization.

Write a clear, plain-English report for a non-technical HR manager or business leader.
Structure your response exactly like this:

## Workforce Overview
2-3 sentences summarizing the overall workforce health.

## Top 3 Risks
For each risk: what it is, why it matters, and which department or group is most affected.

## Top 3 Opportunities
For each opportunity: what it is and what action could improve outcomes.

## Recommended Next Steps
3 concrete actions the HR team should take in the next 30 days.

Keep the language simple. No jargon. Every insight should connect to a business outcome.

Here is the workforce data summary:
{data_summary}"""
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text, prompt


st.set_page_config(page_title="HR Insights AI", page_icon="📊", layout="wide")
st.title("📊 HR Insights AI")
st.caption("Upload your HR data and get instant AI-powered insights — no data science background required.")

uploaded_file = st.file_uploader("Upload your HR Excel or CSV file", type=["xlsx", "csv"])

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success(f"✅ Loaded {len(df):,} employee records")

    with st.expander("Preview your data"):
        st.dataframe(df.head(10))

    st.subheader("Workforce Snapshot")
    total = len(df)

    if "EmployeeStatus" in df.columns:
        active = len(df[df["EmployeeStatus"] == "Active"])
        terminated = len(df[df["EmployeeStatus"] == "Terminated"])
        attrition_rate = round((terminated / total) * 100, 1)
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Employees", f"{total:,}")
        col2.metric("Active", f"{active:,}")
        col3.metric("Terminated", f"{terminated:,}")
        col4.metric("Attrition Rate", f"{attrition_rate}%")
    else:
        active, terminated, attrition_rate = 0, 0, 0
        st.metric("Total Employees", f"{total:,}")

    score_cols = ["Engagement Score", "Satisfaction Score", "Work-Life Balance Score"]
    if all(c in df.columns for c in score_cols) and "DepartmentType" in df.columns:
        st.subheader("Engagement Health by Department")
        st.dataframe(df.groupby("DepartmentType")[score_cols].mean().round(2))

    if "Training Outcome" in df.columns:
        st.subheader("Training Outcomes")
        st.bar_chart(df["Training Outcome"].value_counts())

    st.divider()
    st.subheader("🤖 AI-Generated Insight Report")
    st.caption("Powered by Claude — built for HR leaders, not data scientists.")

    if st.button("Generate AI Insights", type="primary"):
        with st.spinner("Analyzing your workforce data..."):
            summary_parts = [f"Total employees: {total}"]

            if "EmployeeStatus" in df.columns:
                summary_parts.append(f"Active: {active}, Terminated: {terminated}, Attrition rate: {attrition_rate}%")
                if "DepartmentType" in df.columns:
                    dept_attrition = df[df["EmployeeStatus"] == "Terminated"]["DepartmentType"].value_counts()
                    summary_parts.append(f"Terminations by department: {dept_attrition.to_dict()}")

            if "Training Outcome" in df.columns:
                summary_parts.append(f"Training outcomes: {df['Training Outcome'].value_counts().to_dict()}")

            if "Training Program Name" in df.columns:
                summary_parts.append(f"Top training programs: {df['Training Program Name'].value_counts().head(5).to_dict()}")

            if "Engagement Score" in df.columns:
                summary_parts.append(f"Average engagement score: {round(df['Engagement Score'].mean(), 2)}/5")

            if "Satisfaction Score" in df.columns:
                summary_parts.append(f"Average satisfaction score: {round(df['Satisfaction Score'].mean(), 2)}/5")

            if "Work-Life Balance Score" in df.columns:
                summary_parts.append(f"Average work-life balance score: {round(df['Work-Life Balance Score'].mean(), 2)}/5")

            if "Performance Score" in df.columns:
                summary_parts.append(f"Performance distribution: {df['Performance Score'].value_counts().to_dict()}")

            if "GenderCode" in df.columns:
                summary_parts.append(f"Gender distribution: {df['GenderCode'].value_counts().to_dict()}")

            data_summary = "\n".join(summary_parts)
            insights, prompt_used = generate_hr_insights(data_summary)

            st.markdown(insights)

            st.divider()
            with st.expander("🔍 Audit Trail — See exactly what was sent to AI"):
                st.subheader("Data Summary Sent to Claude")
                st.text(data_summary)
                st.subheader("Prompt Used")
                st.text(prompt_used)
                st.caption("This audit trail ensures the analysis is transparent, repeatable, and trustworthy.")