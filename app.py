from typing import List, Optional

import streamlit as st
import pandas as pd
from analyzer import generate_hr_insights

st.set_page_config(page_title="HR Insights AI", page_icon="📊", layout="wide")
st.title("📊 HR Insights AI")
st.caption("Upload your HR data and get instant AI-powered insights — no data science background required.")


# --- Flexible column matching -----------------------------------------
# Real-world HR exports name columns differently (e.g. "Status" vs
# "EmployeeStatus", "Department" vs "DepartmentType"). Instead of requiring
# an exact match, we look for any of a few common variants, case-insensitive.

COLUMN_CANDIDATES = {
    "status": ["EmployeeStatus", "Status", "Employment Status", "Employment_Status"],
    "department": ["DepartmentType", "Department", "Dept", "Department_Name"],
    "engagement": ["Engagement Score", "EngagementScore", "Engagement_Score"],
    "satisfaction": ["Satisfaction Score", "SatisfactionScore", "Satisfaction_Score"],
    "work_life_balance": ["Work-Life Balance Score", "WorkLifeBalanceScore", "Work_Life_Balance_Score"],
    "training_outcome": ["Training Outcome", "TrainingOutcome", "Training_Outcome"],
    "training_program": ["Training Program Name", "TrainingProgramName", "Training_Program_Name"],
    "performance": ["Performance Score", "Performance", "PerformanceRating", "Performance_Rating"],
    "gender": ["GenderCode", "Gender", "Gender_Code"],
}


def find_column(df: pd.DataFrame, candidates: List[str]) -> Optional[str]:
    """Return the actual column name in df matching one of the candidates (case-insensitive), or None."""
    lookup = {c.lower(): c for c in df.columns}
    for candidate in candidates:
        if candidate.lower() in lookup:
            return lookup[candidate.lower()]
    return None


st.caption(
    "⚠️ This is a proof-of-concept built for a specific HR data schema — it won't fully work on just any HR export. "
    "See below for the exact column names it recognizes."
)
with st.expander("Which columns does this app recognize?"):
    st.markdown(
        "This tool looks for the following column names (case-insensitive; a few common variants are "
        "supported for each). If your file doesn't include a matching column for a metric, that section "
        "is simply skipped rather than guessed at.\n\n"
        "- **Employment status:** `EmployeeStatus`, `Status`, `Employment Status`, `Employment_Status` "
        "— anything other than `Active` (e.g. Resigned, Terminated, Retired) counts as departed.\n"
        "- **Department:** `DepartmentType`, `Department`, `Dept`, `Department_Name`\n"
        "- **Engagement score:** `Engagement Score`, `EngagementScore`, `Engagement_Score`\n"
        "- **Satisfaction score:** `Satisfaction Score`, `SatisfactionScore`, `Satisfaction_Score`\n"
        "- **Work-life balance score:** `Work-Life Balance Score`, `WorkLifeBalanceScore`, `Work_Life_Balance_Score`\n"
        "- **Training outcome:** `Training Outcome`, `TrainingOutcome`, `Training_Outcome`\n"
        "- **Training program name:** `Training Program Name`, `TrainingProgramName`, `Training_Program_Name`\n"
        "- **Performance:** `Performance Score`, `Performance`, `PerformanceRating`, `Performance_Rating`\n"
        "- **Gender:** `GenderCode`, `Gender`, `Gender_Code`"
    )

uploaded_file = st.file_uploader("Upload your HR Excel or CSV file", type=["xlsx", "csv"])

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success(f"✅ Loaded {len(df):,} employee records")

    with st.expander("Preview your data"):
        st.dataframe(df.head(10))

    # Resolve actual column names present in this dataset
    status_col = find_column(df, COLUMN_CANDIDATES["status"])
    department_col = find_column(df, COLUMN_CANDIDATES["department"])
    engagement_col = find_column(df, COLUMN_CANDIDATES["engagement"])
    satisfaction_col = find_column(df, COLUMN_CANDIDATES["satisfaction"])
    wlb_col = find_column(df, COLUMN_CANDIDATES["work_life_balance"])
    training_outcome_col = find_column(df, COLUMN_CANDIDATES["training_outcome"])
    training_program_col = find_column(df, COLUMN_CANDIDATES["training_program"])
    performance_col = find_column(df, COLUMN_CANDIDATES["performance"])
    gender_col = find_column(df, COLUMN_CANDIDATES["gender"])

    st.subheader("Workforce Snapshot")
    total = len(df)

    active, departed, attrition_rate = 0, 0, 0
    status_counts = None

    if status_col:
        # Treat "Active" (any casing/whitespace) as active; everything else
        # (Resigned, Terminated, Retired, etc.) counts as departed.
        normalized_status = df[status_col].astype(str).str.strip().str.lower()
        active_mask = normalized_status == "active"
        active = int(active_mask.sum())
        departed = total - active
        attrition_rate = round((departed / total) * 100, 1) if total else 0
        status_counts = df[status_col].value_counts()

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Employees", f"{total:,}")
        col2.metric("Active", f"{active:,}")
        col3.metric("Departed (all other statuses)", f"{departed:,}")
        col4.metric("Attrition Rate", f"{attrition_rate}%")

        with st.expander("Status breakdown"):
            st.dataframe(status_counts)
    else:
        st.metric("Total Employees", f"{total:,}")
        st.caption("No employee status column detected — attrition metrics unavailable for this file.")

    score_cols = [c for c in [engagement_col, satisfaction_col, wlb_col] if c]
    if score_cols and department_col:
        st.subheader("Engagement Health by Department")
        st.dataframe(df.groupby(department_col)[score_cols].mean().round(2))

    if training_outcome_col:
        st.subheader("Training Outcomes")
        st.bar_chart(df[training_outcome_col].value_counts())

    st.divider()
    st.subheader("🤖 AI-Generated Insight Report")
    st.caption("Powered by Claude — built for HR leaders, not data scientists.")

    if st.button("Generate AI Insights", type="primary"):
        with st.spinner("Analyzing your workforce data..."):
            summary_parts = [f"Total employees: {total}"]

            if status_col:
                summary_parts.append(
                    f"Active: {active}, Departed (all non-active statuses): {departed}, "
                    f"Attrition rate: {attrition_rate}%"
                )
                summary_parts.append(f"Status breakdown: {status_counts.to_dict()}")

                if department_col:
                    departed_mask = df[status_col].astype(str).str.strip().str.lower() != "active"
                    dept_attrition = df[departed_mask][department_col].value_counts()
                    summary_parts.append(f"Departures by department: {dept_attrition.to_dict()}")

            if training_outcome_col:
                summary_parts.append(f"Training outcomes: {df[training_outcome_col].value_counts().to_dict()}")

            if training_program_col:
                summary_parts.append(
                    f"Top training programs: {df[training_program_col].value_counts().head(5).to_dict()}"
                )

            if engagement_col:
                summary_parts.append(f"Average engagement score: {round(df[engagement_col].mean(), 2)}/5")

            if satisfaction_col:
                summary_parts.append(f"Average satisfaction score: {round(df[satisfaction_col].mean(), 2)}/5")

            if wlb_col:
                summary_parts.append(f"Average work-life balance score: {round(df[wlb_col].mean(), 2)}/5")

            if performance_col:
                summary_parts.append(f"Performance distribution: {df[performance_col].value_counts().to_dict()}")

            if gender_col:
                summary_parts.append(f"Gender distribution: {df[gender_col].value_counts().to_dict()}")

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
