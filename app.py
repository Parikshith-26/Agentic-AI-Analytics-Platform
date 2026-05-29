
import streamlit as st

from orchestrator import run_pipeline

from agents.router import QueryRouter
from agents.sql_agent import query_data
from agents.feedback_agent import feedback_agent
from agents.forecast_agent import forecast_agent

from memory.memory import AgentMemory

from utils.visualizer import plot_charts
from models.ollama_client import ask_llm


# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(

    page_title="Agentic AI Analytics Platform",

    layout="wide"
)

st.title("🤖 Agentic AI Analytics Platform")


# ---------------------------------------------------
# SESSION MEMORY
# ---------------------------------------------------

if "memory" not in st.session_state:

    st.session_state.memory = AgentMemory()

if "workflow_history" not in st.session_state:

    st.session_state.workflow_history = []


memory = st.session_state.memory


# ---------------------------------------------------
# ROUTER
# ---------------------------------------------------

router = QueryRouter()


# ---------------------------------------------------
# FILE UPLOAD
# ---------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload Dataset (CSV / Excel)"
)


# ---------------------------------------------------
# MAIN PIPELINE
# ---------------------------------------------------

if uploaded_file:

    with st.spinner(
        "Running autonomous AI workflow..."
    ):

        results = run_pipeline(uploaded_file)

    # ---------------------------------------------------
    # ERROR HANDLING
    # ---------------------------------------------------

    if results.get("status") == "error":

        st.error(results["message"])

        st.stop()

    st.success(
        "AI analysis completed successfully!"
    )

    # ---------------------------------------------------
    # MEMORY STORAGE
    # ---------------------------------------------------

    memory.store(
        "analysis",
        results["analysis"]
    )

    memory.store(
        "dataset_columns",
        list(results["df"].columns)
    )

    # ---------------------------------------------------
    # INSIGHTS SECTION
    # ---------------------------------------------------

    st.header("📈 AI Insights")

    insights = results["insights"]

    # ---------------------------------------------------
    # EXECUTIVE SUMMARY
    # ---------------------------------------------------

    if insights.get("executive_summary"):

        st.subheader(
            "🧠 Executive Summary"
        )

        st.write(
            insights["executive_summary"]
        )

    # ---------------------------------------------------
    # TRENDS + ANOMALIES
    # ---------------------------------------------------

    col1, col2 = st.columns(2)

    # Trends
    with col1:

        st.subheader("📊 Trends")

        for trend in insights.get(
            "trends",
            []
        ):

            if isinstance(trend, dict):

                st.write(
                    f"""
• [{trend.get('severity', '').upper()}]
{trend.get('message', '')}
"""
                )

            else:

                st.write(f"• {trend}")

    # Anomalies
    with col2:

        st.subheader("⚠️ Anomalies")

        for anomaly in insights.get(
            "anomalies",
            []
        ):

            if isinstance(anomaly, dict):

                st.write(
                    f"""
• [{anomaly.get('severity', '').upper()}]
{anomaly.get('message', '')}
"""
                )

            else:

                st.write(f"• {anomaly}")

    # ---------------------------------------------------
    # RECOMMENDATIONS
    # ---------------------------------------------------

    st.header("💡 Recommendations")

    for rec in insights.get(
        "recommendations",
        []
    ):

        st.write(f"• {rec}")

    # ---------------------------------------------------
    # FEATURE ENGINEERING
    # ---------------------------------------------------

    st.header("🧩 Feature Suggestions")

    features = results["features"]

    if isinstance(features, dict):

        st.write(
            features.get(
                "recommendations",
                features
            )
        )

    else:

        st.write(features)

    # ---------------------------------------------------
    # DASHBOARD RECOMMENDATIONS
    # ---------------------------------------------------

    st.header(
        "📊 AI Dashboard Recommendations"
    )

    dashboard = results["dashboard"]

    if isinstance(dashboard, dict):

        st.subheader(
            dashboard.get(
                "dashboard_type",
                "Dashboard"
            )
        )

        st.write(
            dashboard.get(
                "recommendations",
                dashboard
            )
        )

    else:

        st.write(dashboard)

    # ---------------------------------------------------
    # DATA PREVIEW
    # ---------------------------------------------------

    st.header(
        "📂 Cleaned Dataset Preview"
    )

    st.dataframe(
        results["df"].head()
    )

    # ---------------------------------------------------
    # VISUALIZATIONS
    # ---------------------------------------------------

    st.header("📉 Auto Visualizations")

    charts = plot_charts(results["df"])

    for chart in charts:

        st.pyplot(chart["figure"])

        st.caption(
            f"""
Chart Type:
{chart['metadata']['type']}

Reason:
{chart['metadata']['reason']}
"""
        )

    # ---------------------------------------------------
    # DOWNLOAD BUTTON
    # ---------------------------------------------------

    st.download_button(

        label="⬇ Download Cleaned Dataset",

        data=results["df"].to_csv(
            index=False
        ),

        file_name="cleaned_data.csv",

        mime="text/csv"
    )

    # ---------------------------------------------------
    # AI QUERY SECTION
    # ---------------------------------------------------

    st.header(
        "🤖 Ask AI About Your Data"
    )

    user_query = st.text_input(
        "Ask analytical questions about your dataset"
    )

    # ---------------------------------------------------
    # QUERY EXECUTION
    # ---------------------------------------------------

    if user_query:

        memory.store(
            "latest_query",
            user_query
        )

        # ---------------------------------------------------
        # ROUTING
        # ---------------------------------------------------

        route_result = router.route_query(
            user_query
        )

        primary_intent = route_result[
            "primary_intent"
        ]

        confidence = route_result[
            "confidence"
        ]

        st.info(
            f"""
Intent:
{primary_intent.upper()}

Confidence:
{confidence}
"""
        )

        # ---------------------------------------------------
        # SQL AGENT
        # ---------------------------------------------------

        if primary_intent == "sql":

            st.subheader("📊 SQL Agent")

            sql_result = query_data(

                results["df"],

                user_query
            )

            # SUCCESS
            if sql_result["status"] == "success":

                st.success(
                    "SQL query executed successfully!"
                )

                # Show SQL query
                st.code(

                    sql_result["query"],

                    language="sql"
                )

                # Show result dataframe
                st.dataframe(
                    sql_result["result"]
                )

            # ERROR
            else:

                st.error(
                    sql_result["message"]
                )

                if "query" in sql_result:

                    st.code(

                        sql_result["query"],

                        language="sql"
                    )

        # ---------------------------------------------------
        # FEEDBACK AGENT
        # ---------------------------------------------------

        elif primary_intent == "feedback":

            st.subheader(
                "📌 Explanation Agent"
            )

            answer = feedback_agent(

                results["analysis"],

                user_query
            )

            st.write(answer)

        # ---------------------------------------------------
        # FORECAST AGENT
        # ---------------------------------------------------

        elif primary_intent == "forecast":

            st.subheader(
                "📈 Forecast Agent"
            )

            forecast_result = forecast_agent(
                results["df"]
            )

            st.write(forecast_result)

        # ---------------------------------------------------
        # DEFAULT AI AGENT
        # ---------------------------------------------------

        else:

            st.subheader(
                "🧠 AI Business Analyst"
            )

            prompt = f"""
You are an AI business analyst.

Dataset Summary:
{results['analysis']}

Previous Context:
{memory.get_recent_context()}

User Question:
{user_query}

Provide:
1. Business explanation
2. Insights
3. Risks
4. Recommendations
"""

            answer = ask_llm(prompt)

            st.write(answer)

        # ---------------------------------------------------
        # WORKFLOW HISTORY
        # ---------------------------------------------------

        st.session_state.workflow_history.append({

            "query": user_query,

            "intent": primary_intent,

            "confidence": confidence
        })

    # ---------------------------------------------------
    # WORKFLOW HISTORY
    # ---------------------------------------------------

    with st.expander(
        "🧾 Workflow History"
    ):

        st.write(
            st.session_state.workflow_history
        )

