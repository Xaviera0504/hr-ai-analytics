# HR Insights AI

An AI-powered workforce analytics proof-of-concept that turns HR data into a plain-English report for non-technical managers. Upload an employee dataset matching the expected schema (see below) and get an instant summary of attrition risk, engagement trends, and recommended next steps — the kind of analysis a people analytics team would normally need days and a dashboard tool to produce.

**Live app:** [hr-ai-analytics-h94y7mdnzt2hzfk4t9paci.streamlit.app](https://hr-ai-analytics-h94y7mdnzt2hzfk4t9paci.streamlit.app)

**This is an MVP, not a general-purpose tool.** It was built and tested against one specific HR dataset schema. It recognizes a small set of column name variants for that schema (listed under [Expected data format](#expected-data-format)) — it is not designed to work with an arbitrary HR export. If a dataset's columns don't match, the corresponding section is skipped rather than guessed at.

## Why this exists

Most HR teams sit on employee data (attrition, engagement scores, training outcomes) but don't have a data analyst on hand to translate it into something actionable. This project explores whether an LLM can close that gap: take a spreadsheet export, do the basic aggregation a human analyst would do, and generate a business-ready narrative — risks, opportunities, and 30-day actions — without requiring the reader to know what a pivot table is.

It's built as a portfolio project to demonstrate applied people analytics and AI-assisted reporting on a defined dataset, not as a production or general-purpose HR system.

## Features

- Upload an HR dataset (matching the expected schema) as `.xlsx` or `.csv`
- Auto-generated workforce snapshot: headcount, active/departed counts, attrition rate, full status breakdown
- Engagement, satisfaction, and work-life balance scores broken out by department
- Training outcome distribution chart
- One-click AI report (via Claude) structured as: Workforce Overview, Top 3 Risks, Top 3 Opportunities, Recommended Next Steps
- Full audit trail — see exactly what data summary and prompt were sent to the model, so the output is explainable rather than a black box
- In-app reference of exactly which columns the app recognizes, so it's clear upfront whether a given file will work

## Tech stack

- [Streamlit](https://streamlit.io) — UI and app framework
- [Anthropic Claude API](https://www.anthropic.com) — report generation
- [pandas](https://pandas.pydata.org) — data processing
- Python 3.9+

## Running it locally

```bash
git clone https://github.com/Xaviera0504/hr-ai-analytics.git
cd hr-ai-analytics
pip install -r requirements.txt
```

Create a `.env` file in the project root with your own Anthropic API key:

```
ANTHROPIC_API_KEY=your-key-here
```

Then start the app:

```bash
streamlit run app.py
```

## Expected data format

This app is tailored to a specific dataset schema. For each metric below, it recognizes a small set of common column name variants (case-insensitive) — anything outside this list won't be picked up, and that section will simply be skipped.

| Metric | Recognized column names | Powers |
|---|---|---|
| Employment status | `EmployeeStatus`, `Status`, `Employment Status`, `Employment_Status` | Active/departed counts, attrition rate, status breakdown. Anything other than `Active` (Resigned, Terminated, Retired, etc.) counts as departed. |
| Department | `DepartmentType`, `Department`, `Dept`, `Department_Name` | Department-level breakdowns, departures by department |
| Engagement score | `Engagement Score`, `EngagementScore`, `Engagement_Score` | Engagement health table |
| Satisfaction score | `Satisfaction Score`, `SatisfactionScore`, `Satisfaction_Score` | Engagement health table |
| Work-life balance score | `Work-Life Balance Score`, `WorkLifeBalanceScore`, `Work_Life_Balance_Score` | Engagement health table |
| Training outcome | `Training Outcome`, `TrainingOutcome`, `Training_Outcome` | Training outcomes chart |
| Training program name | `Training Program Name`, `TrainingProgramName`, `Training_Program_Name` | Top training programs in the AI summary |
| Performance | `Performance Score`, `Performance`, `PerformanceRating`, `Performance_Rating` | Performance distribution in the AI summary |
| Gender | `GenderCode`, `Gender`, `Gender_Code` | Gender distribution in the AI summary |

If none of a dataset's columns match this list, the app will still load the file and show a headcount, but won't have enough signal to generate a meaningful AI report — this is intentional (the app won't fabricate insights from missing data). The app also shows this same column reference in an expander above the file uploader, so it's clear before uploading whether a given file will work. A dataset matching this schema (e.g. a synthetic/public HR dataset from Kaggle formatted to match) works best for testing.

## Project structure

```
hr-ai-analytics/
├── app.py           # Streamlit UI: file upload, metrics, charts
├── analyzer.py       # Claude API call + prompt template for the AI report
├── requirements.txt
└── .gitignore
```

## Built with AI assistance

The prompt design and parts of this app were developed with help from Claude (Anthropic). Credited here rather than left unstated, since GitHub's contributor graph only tracks accounts with commit access.

## License

MIT — see [LICENSE](LICENSE).

## Author

**Xiaowen (Xaviera) Xu**
[GitHub @Xaviera0504](https://github.com/Xaviera0504)
