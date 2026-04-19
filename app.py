import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="AI Operations Decision Engine", layout="wide")

# Title
st.title("AI Operations Decision Engine")
st.markdown("Turn raw data into actionable insights.")

st.divider()

# Upload Section
st.subheader("Upload Your Data")

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.success("File uploaded successfully!")

    # Data Preview
    st.subheader("Data Preview")
    st.dataframe(df)

    # Chart
    st.subheader("Downtime by Store")
    fig = px.bar(df, x="Store", y="Downtime", color="Store")
    st.plotly_chart(fig, use_container_width=True)

    # Key Metrics
    st.subheader("Key Metrics")

    total_transactions = df["Transactions"].sum()
    avg_downtime = df["Downtime"].mean()
    total_errors = df["Errors"].sum()

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Transactions", total_transactions)
    col2.metric("Avg Downtime", round(avg_downtime, 2))
    col3.metric("Total Errors", total_errors)

    # Generate Insights Button
    if st.button("Generate Insights"):

        st.subheader("AI Insights")

        insights = []

        # Downtime issue (HIGH IMPACT)
        worst_downtime = df.loc[df["Downtime"].idxmax()]
        insights.append({
            "priority": worst_downtime["Downtime"],
            "message": f"[HIGH IMPACT] Store {worst_downtime['Store']} has the highest downtime ({worst_downtime['Downtime']} mins). Recommended action: Investigate system performance and staffing.",
            "type": "warning"
        })

        # Error issue (MEDIUM IMPACT)
        worst_errors = df.loc[df["Errors"].idxmax()]
        insights.append({
            "priority": worst_errors["Errors"],
            "message": f"[MEDIUM IMPACT] Store {worst_errors['Store']} has the highest errors ({worst_errors['Errors']} issues). Recommended action: Check device reliability and training.",
            "type": "error"
        })

        # Best performer (LOW IMPACT)
        best_store = df.loc[df["Transactions"].idxmax()]
        insights.append({
            "priority": 0,
            "message": f"[LOW IMPACT] Store {best_store['Store']} is the best performing with highest transactions ({best_store['Transactions']}).",
            "type": "success"
        })

        # Sort insights
        insights = sorted(insights, key=lambda x: x["priority"], reverse=True)

        # Display insights
        for insight in insights:
            if insight["type"] == "warning":
                st.warning(insight["message"])
            elif insight["type"] == "error":
                st.error(insight["message"])
            else:
                st.success(insight["message"])

        # AI Summary
        st.subheader("AI Summary")

        summary = f"""
Overall, Store {worst_downtime['Store']} is experiencing the most operational issues due to high downtime and errors.
This could significantly impact performance and revenue.

Immediate attention is recommended for this location, focusing on system stability and staff efficiency.

Meanwhile, Store {best_store['Store']} is performing well and can be used as a benchmark for best practices.
"""
        st.info(summary)