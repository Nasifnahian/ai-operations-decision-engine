import re
import streamlit as st
import pandas as pd
import plotly.express as px
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def normalize_text(value: str) -> str:
    return re.sub(r"[^a-z]", "", str(value).lower())


def find_column(df, possible_names):
    normalized_targets = [normalize_text(name) for name in possible_names]

    for col in df.columns:
        col_clean = normalize_text(col)
        for target in normalized_targets:
            if target in col_clean or col_clean in target:
                return col
    return None


st.set_page_config(
    page_title="AI Operations Decision Engine",
    page_icon="⚡",
    layout="wide"
)

st.markdown("""
<style>

/* Main background */
.stApp {
    background-color: #0b0f19;
    color: #f8fafc;
}

/* Page spacing */
.block-container {
    padding-top: 2.5rem;
    padding-left: 3rem;
    padding-right: 3rem;
}

/* Headings */
h1, h2, h3 {
    color: #ffffff !important;
    font-family: 'Inter', sans-serif;
    font-weight: 700;
}

/* General text */
p, label, span, div {
    color: #e5e7eb;
}

/* Divider */
hr {
    border-color: #1f2937;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: linear-gradient(145deg, #111827, #0f172a);
    border: 1px solid #1f2937;
    padding: 24px;
    border-radius: 20px;
    box-shadow: 0 12px 30px rgba(0,0,0,0.28);
}

[data-testid="stMetricLabel"] {
    color: #9ca3af !important;
    font-size: 14px;
}

[data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-size: 34px;
    font-weight: 700;
}

/* Main buttons */
.stButton > button {
    background-color: #2563eb !important;
    color: #ffffff !important;
    border-radius: 999px;
    padding: 10px 24px;
    border: none !important;
    font-weight: 700;
    transition: 0.2s ease;
}

.stButton > button:hover {
    background-color: #1d4ed8 !important;
    color: #ffffff !important;
    transform: translateY(-1px);
}

/* File uploader outer box */
[data-testid="stFileUploader"] {
    background: #111827;
    border: 1px solid #1f2937;
    border-radius: 18px;
    padding: 18px;
}

/* File uploader drop area */
[data-testid="stFileUploader"] section {
    background: #0f172a !important;
    border: 1px dashed #334155 !important;
    border-radius: 16px !important;
}

/* File uploader text */
[data-testid="stFileUploader"] label,
[data-testid="stFileUploader"] small,
[data-testid="stFileUploader"] span,
[data-testid="stFileUploader"] div,
[data-testid="stFileUploader"] p {
    color: #f8fafc !important;
}

/* Upload button inside uploader */
[data-testid="stFileUploader"] button {
    background-color: #2563eb !important;
    color: #ffffff !important;
    border-radius: 10px !important;
    border: none !important;
    font-weight: 600 !important;
}

[data-testid="stFileUploader"] button:hover {
    background-color: #1d4ed8 !important;
    color: #ffffff !important;
}

/* Alerts */
div[data-testid="stAlert"] {
    border-radius: 16px;
    border: 1px solid #1f2937;
}

/* Dataframe container */
.stDataFrame {
    background: #111827;
    border-radius: 18px;
    padding: 10px;
    border: 1px solid #1f2937;
}

/* Expander */
.streamlit-expanderHeader {
    background: #111827;
    border-radius: 12px;
    color: #ffffff !important;
}

/* Code badges */
code {
    background: #0f172a !important;
    color: #38bdf8 !important;
    border-radius: 6px;
    padding: 3px 6px;
}

/* Reduce vertical gaps */
[data-testid="stVerticalBlock"] {
    gap: 1rem;
}
/* Force uploaded file chip text readable */
[data-testid="stFileUploader"] [data-testid="stFileUploaderFile"] * {
    color: #111827 !important;
    opacity: 1 !important;
}

[data-testid="stFileUploader"] [data-testid="stFileUploaderFileName"] {
    color: #111827 !important;
    opacity: 1 !important;
    font-weight: 700 !important;
}

[data-testid="stFileUploader"] [data-testid="stFileUploaderFile"] {
    background-color: #f8fafc !important;
}     


</style>
""", unsafe_allow_html=True)



# Title
st.title("AI Operations Decision Engine")
st.markdown("Turn raw data into actionable insights.")

st.divider()

# Upload Section
st.subheader("Upload Your Data")

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Smart column detection
    store_col = find_column(df, [
        "store", "location", "branch", "site", "store_name", "branch_name"
    ])

    transactions_col = find_column(df, [
        "transactions", "sales", "orders", "volume", "salescount",
        "transactioncount", "sales_count", "order_count"
    ])

    downtime_col = find_column(df, [
        "downtime", "delay", "outage", "delayminutes", "downtimeminutes",
        "downtime_minutes", "delay_minutes", "outage_minutes"
    ])

    errors_col = find_column(df, [
        "errors", "issues", "failures", "incident", "incidents",
        "issuecount", "errorcount", "issue_count", "error_count"
    ])

    # Manual mapping fallback only if auto-detection fails
    if not all([store_col, transactions_col, downtime_col, errors_col]):
        st.warning("Auto-detection could not fully identify the required columns. Please map them manually.")

        all_columns = df.columns.tolist()

        store_col = st.selectbox("Select Store / Location column", all_columns)
        transactions_col = st.selectbox("Select Transactions / Sales column", all_columns)
        downtime_col = st.selectbox("Select Downtime / Delay column", all_columns)
        errors_col = st.selectbox("Select Errors / Issues column", all_columns)

    # Convert important columns to numeric safely
    df[transactions_col] = pd.to_numeric(df[transactions_col], errors="coerce")
    df[downtime_col] = pd.to_numeric(df[downtime_col], errors="coerce")
    df[errors_col] = pd.to_numeric(df[errors_col], errors="coerce")

    # Drop rows where key numeric values are missing
    df = df.dropna(subset=[transactions_col, downtime_col, errors_col])

    if df.empty:
        st.error("No usable numeric data found after cleaning the CSV.")
        st.stop()

    st.success("File uploaded successfully!")

    # Show detected mappings
    st.subheader("Detected Column Mapping")
    st.write(f"Store/Location column: `{store_col}`")
    st.write(f"Transactions column: `{transactions_col}`")
    st.write(f"Downtime column: `{downtime_col}`")
    st.write(f"Errors column: `{errors_col}`")

    # Data Preview
    st.subheader("Data Preview")
    st.dataframe(df)

    # Chart
# Chart
if uploaded_file is not None:

    st.subheader("Downtime by Store")

    fig = px.bar(df, x=store_col, y=downtime_col, color=store_col)

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0b0f19",
        plot_bgcolor="#0b0f19",
        font_color="white",
        title_font_color="white",
        legend_font_color="white",
        margin=dict(l=40, r=40, t=60, b=40)
    )

    st.plotly_chart(fig, use_container_width=True)



# Key Metrics
st.subheader("Key Metrics")

if uploaded_file is not None:

    total_transactions = df[transactions_col].sum()
    avg_downtime = df[downtime_col].mean()
    total_errors = df[errors_col].sum()

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Transactions", int(total_transactions))
    col2.metric("Avg Downtime", round(avg_downtime, 2))
    col3.metric("Total Errors", int(total_errors))

    # Operations Triage Engine
    st.subheader("Operations Triage Engine")

    triage_results = []

    avg_transactions = df[transactions_col].mean()

    for index, row in df.iterrows():
        location = row[store_col]
        transactions = row[transactions_col]
        downtime = row[downtime_col]
        errors = row[errors_col]

        if downtime >= avg_downtime and transactions < avg_transactions:
            severity = "Critical"
            root_cause = "Possible system outage or operational disruption"
            recommendation = "Dispatch technician or investigate system performance immediately"

        elif errors >= df[errors_col].mean() and transactions >= avg_transactions:
            severity = "Watchlist"
            root_cause = "Possible training, process, or device reliability issue"
            recommendation = "Review staff workflow and check device error patterns"

        elif transactions < avg_transactions and errors <= df[errors_col].mean():
            severity = "Monitor"
            root_cause = "Possible low demand or location-level activity issue"
            recommendation = "Monitor trend and compare with historical performance"

        else:
            severity = "Stable"
            root_cause = "No major operational risk detected"
            recommendation = "Continue normal monitoring"

        triage_results.append({
            "Location": location,
            "Transactions": transactions,
            "Downtime": downtime,
            "Errors": errors,
            "Severity": severity,
            "Likely Root Cause": root_cause,
            "Recommended Action": recommendation
        })

    triage_df = pd.DataFrame(triage_results)

    severity_order = {
        "Critical": 1,
        "Watchlist": 2,
        "Monitor": 3,
        "Stable": 4
    }

    triage_df["Severity Rank"] = triage_df["Severity"].map(severity_order)
    triage_df = triage_df.sort_values("Severity Rank").drop(columns=["Severity Rank"])

    st.dataframe(triage_df, use_container_width=True)

    # Highlight top risk
    top_risk = triage_df.iloc[0]

    if top_risk["Severity"] == "Critical":
        st.error(
            f"Top Priority: {top_risk['Location']} is marked Critical. "
            f"Likely cause: {top_risk['Likely Root Cause']}. "
            f"Action: {top_risk['Recommended Action']}."
        )
    elif top_risk["Severity"] == "Watchlist":
        st.warning(
            f"Top Priority: {top_risk['Location']} is on the Watchlist. "
            f"Likely cause: {top_risk['Likely Root Cause']}. "
            f"Action: {top_risk['Recommended Action']}."
        )
    else:
        st.success("No critical operational risk detected in this dataset.")

    # AI Summary
    st.subheader("AI Executive Summary")

    if st.button("Generate AI Executive Summary", key="ai_summary_button"):

        prompt = f"""
You are a business operations analyst.

Here is the operational triage table:

{triage_df.to_string(index=False)}

Write a short executive summary for an operations manager.

Include:
- Top operational risk
- Likely root cause
- Recommended action
- Best performing location if visible

Keep it concise, professional, and action-oriented.
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a business operations analyst."},
                {"role": "user", "content": prompt}
            ]
        )

        ai_summary = response.choices[0].message.content
        st.info(ai_summary)

else:
    st.info("Upload a CSV file to begin analysis.")