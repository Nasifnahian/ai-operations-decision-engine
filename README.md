# AI Operations Decision Engine

AI-powered operational intelligence dashboard designed to transform raw store-level performance data into prioritized business insights, operational risk alerts, and executive-ready recommendations.

## Overview

The AI Operations Decision Engine helps operations teams quickly identify performance issues across multiple locations by combining automated KPI analysis, operational triage logic, visualization, and AI-generated executive summaries.

Built as a modern operations decision-support prototype inspired by real-world field operations and multi-location support workflows.

---

## Core Features

### Operational Triage Engine
Automatically classifies locations into categories such as:
- Critical
- Watchlist
- Stable
- Monitor

Based on operational indicators including:
- Transactions
- Downtime
- Errors

---

### AI Executive Summary
Uses OpenAI API integration to generate:
- Executive-level operational summaries
- Risk explanations
- Recommended actions
- Performance observations

---

### Smart Operational Logic
Detects patterns such as:
- High downtime + low transactions
- High errors + high activity
- Low demand vs operational disruption

And converts them into actionable recommendations.

---

### Interactive Dashboard
Includes:
- Modern dark-mode UI
- KPI cards
- Downtime visualizations
- Operational risk table
- AI-generated insights

---

## Tech Stack

- Python
- Streamlit
- Pandas
- Plotly
- OpenAI API

---

## Example Workflow

1. Upload operational CSV data
2. Automatically detect operational columns
3. Generate KPIs and visualizations
4. Identify operational risks
5. Produce AI executive summary and recommendations

---

## Sample Operational Metrics

The system analyzes data such as:
- Store / Location
- Transactions
- Downtime
- Errors / Failures

---

## Use Case

Designed for:
- Operations teams
- Regional managers
- Product operations
- Field support environments
- Multi-location business monitoring

---

## Future Enhancements

- Risk scoring engine
- Trend analysis
- Historical performance tracking
- PDF executive reports
- Real-time operational monitoring
- Advanced anomaly detection

---

## Run Locally

```bash
streamlit run app.py
