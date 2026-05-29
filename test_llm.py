from orchestrator import run_pipeline


# ---------------------------------------------------
# TEST FILE PATH
# ---------------------------------------------------

FILE_PATH = r"c:\Users\user\Desktop\Retail-Sales-Analysis-SQL-Project--P1\SQL - Retail Sales Analysis_utf .csv"


# ---------------------------------------------------
# RUN PIPELINE
# ---------------------------------------------------

results = run_pipeline(FILE_PATH)


# ---------------------------------------------------
# CHECK ERRORS
# ---------------------------------------------------

if results.get("status") == "error":

    print("\nPIPELINE FAILED")
    print(results["message"])

else:

    # ---------------------------------------------------
    # WORKFLOW STEPS
    # ---------------------------------------------------

    print("\n========== WORKFLOW ==========")

    for step in results["workflow_steps"]:

        print(f"• {step}")

    # ---------------------------------------------------
    # ANALYSIS SUMMARY
    # ---------------------------------------------------

    print("\n========== ANALYSIS ==========")

    analysis = results["analysis"]

    print("\nDataset Shape:")
    print(analysis.get("shape"))

    print("\nBusiness Metrics:")
    print(analysis.get("metrics"))

    print("\nData Quality Score:")
    print(analysis.get("data_quality_score"))

    # ---------------------------------------------------
    # INSIGHTS
    # ---------------------------------------------------

    print("\n========== INSIGHTS ==========")

    insights = results["insights"]

    print("\nExecutive Summary:")
    print(
        insights.get(
            "executive_summary",
            "No summary available"
        )
    )

    print("\nTrends:")

    for trend in insights.get("trends", []):

        print(
            f"""
- [{trend['severity'].upper()}]
{trend['message']}
"""
        )

    print("\nAnomalies:")

    for anomaly in insights.get("anomalies", []):

        print(
            f"""
- [{anomaly['severity'].upper()}]
{anomaly['message']}
"""
        )

    # ---------------------------------------------------
    # FEATURE RECOMMENDATIONS
    # ---------------------------------------------------

    print("\n========== FEATURE ENGINEERING ==========")

    features = results["features"]

    print(
        features.get(
            "recommendations",
            "No recommendations"
        )
    )

    # ---------------------------------------------------
    # DASHBOARD RECOMMENDATIONS
    # ---------------------------------------------------

    print("\n========== DASHBOARD ==========")

    dashboard = results["dashboard"]

    print("\nDashboard Type:")
    print(
        dashboard.get(
            "dashboard_type"
        )
    )

    print("\nKPIs:")
    print(
        dashboard.get(
            "kpis"
        )
    )

    print("\nRecommendations:")
    print(
        dashboard.get(
            "recommendations"
        )
    )

    # ---------------------------------------------------
    # FORECAST RESULTS
    # ---------------------------------------------------

    if results.get("forecast"):

        print("\n========== FORECAST ==========")

        print(
            results["forecast"]
        )

    # ---------------------------------------------------
    # EXECUTION TIME
    # ---------------------------------------------------

    print("\n========== EXECUTION ==========")

    print(
        f"""
Execution Time:
{results['execution_time']} seconds
"""
    )