# HR Insights AI

An AI-powered workforce analytics tool that turns raw HR data into a plain-English report for non-technical managers. Upload an employee dataset and get an instant summary of attrition risk, engagement trends, and recommended next steps — the kind of analysis a people analytics team would normally need days and a dashboard tool to produce.

**Live app:** [hr-ai-analytics-h94y7mdnzt2hzfk4t9paci.streamlit.app](https://hr-ai-analytics-h94y7mdnzt2hzfk4t9paci.streamlit.app)

## Why this exists

Most HR teams sit on employee data (attrition, engagement scores, training outcomes) but don't have a data analyst on hand to translate it into something actionable. This project explores whether an LLM can close that gap: take a spreadsheet export, do the basic aggregation a human analyst would do, and generate a business-ready narrative — risks, opportunities, and 30-day actions — without requiring the reader to know what a pivot table is.

It's built as a portfolio project to demonstrate applied people analytics and AI-assisted reporting, not as a production HR system.

## Features

- Upload any HR dataset as `.xlsx` or `.csv`
- Auto-generated workforce snapshot: headcount, active/terminated counts, attrition rate
- Engagement, satisfaction, and work-life balance scores broken out by department
- Training outcome distribution chart
- One-click AI report (via Claude) structured as: Workforce Overview, Top 3 Risks, Top 3 Opportunities, Recommended Next Steps
- Full audit trail — see exactly what data summary and prompt were sent to the model, so the output is explainable rather than a black box

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

The app adapts to whatever columns are present, but it looks for these to unlock specific views:

| Column | Powers |
|---|---|
| `EmployeeStatus` | Active/terminated counts, attrition rate |
| `DepartmentType` | Department-level breakdowns, termination-by-department |
| `Engagement Score`, `Satisfaction Score`, `Work-Life Balance Score` | Engagement health table |
| `Training Outcome`, `Training Program Name` | Training outcomes chart |
| `Performance Score` | Performance distribution in the AI summary |
| `GenderCode` | Gender distribution in the AI summary |

No dataset with all of these columns? The app just skips the sections it can't build and still runs on whatever you upload. A sample public HR dataset (e.g. from Kaggle) works well for testing.

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
