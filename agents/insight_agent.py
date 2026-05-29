from models.ollama_client import ask_llm
from memory.memory import AgentMemory


# ---------------------------------------------------
# MEMORY INITIALIZATION
# ---------------------------------------------------

memory = AgentMemory()


# ---------------------------------------------------
# RULE-BASED TREND DETECTION
# ---------------------------------------------------

def detect_trends(metrics, analysis):

    trends = []

    # Revenue trends
    if metrics.get("total_revenue", 0) > 100000:

        trends.append({
            "type": "Revenue Growth",
            "severity": "high",
            "message": "Revenue performance is strong and supports business expansion."
        })

    # Quantity trends
    if metrics.get("total_quantity", 0) > 3000:

        trends.append({
            "type": "Sales Volume",
            "severity": "medium",
            "message": "High sales volume detected across transactions."
        })

    # Category trends
    if metrics.get("top_category"):

        trends.append({
            "type": "Category Dominance",
            "severity": "medium",
            "message": f"{metrics['top_category']} is the dominant category."
        })

    # Customer behavior
    if metrics.get("avg_order_value", 0) > 200:

        trends.append({
            "type": "Customer Spending",
            "severity": "medium",
            "message": "Customers demonstrate strong spending behavior."
        })

    # Dataset complexity
    if len(analysis.get("columns", [])) >= 5:

        trends.append({
            "type": "Dataset Richness",
            "severity": "low",
            "message": "Dataset supports multidimensional analysis."
        })

    return trends


# ---------------------------------------------------
# ANOMALY DETECTION
# ---------------------------------------------------

def detect_anomalies(metrics, analysis):

    anomalies = []

    # Pricing anomaly
    if metrics.get("avg_price", 0) > 120:

        anomalies.append({
            "type": "Pricing Anomaly",
            "severity": "medium",
            "message": "Average product pricing is unusually high."
        })

    # Transaction anomaly
    if metrics.get("total_quantity", 0) > 4000:

        anomalies.append({
            "type": "Volume Spike",
            "severity": "high",
            "message": "Transaction volume exceeds expected threshold."
        })

    # Outlier detection
    outliers = analysis.get("outliers", {})

    for col, count in outliers.items():

        if count > 10:

            anomalies.append({
                "type": "Outlier Detection",
                "severity": "medium",
                "message": f"{col} contains significant outliers."
            })

    return anomalies


# ---------------------------------------------------
# BUSINESS RECOMMENDATIONS
# ---------------------------------------------------

def generate_business_recommendations(metrics):

    recommendations = []

    if metrics.get("top_category"):

        recommendations.append(
            f"Increase marketing investment in {metrics['top_category']} category."
        )

    if metrics.get("avg_order_value", 0) > 200:

        recommendations.append(
            "Target high-value customers using loyalty campaigns."
        )

    if metrics.get("avg_price", 0) > 120:

        recommendations.append(
            "Review pricing strategy to improve competitiveness."
        )

    recommendations.append(
        "Monitor operational KPIs continuously using AI dashboards."
    )

    return recommendations


# ---------------------------------------------------
# AI EXECUTIVE SUMMARY
# ---------------------------------------------------

def generate_ai_summary(analysis):

    prompt = f"""
You are a senior AI business analyst.

Analyze the following dataset summary and provide:

1. Executive summary
2. Major trends
3. Risks
4. Business opportunities
5. Recommended actions

DATASET ANALYSIS:
{analysis}

Provide concise business insights.
"""

    try:

        response = ask_llm(prompt)

        return response

    except Exception as e:

        return f"AI summary generation failed: {e}"


# ---------------------------------------------------
# MAIN INSIGHT AGENT
# ---------------------------------------------------

def insight_agent(analysis):

    metrics = analysis.get("metrics", {})

    # ---------------------------------------------------
    # DETECT TRENDS
    # ---------------------------------------------------

    trends = detect_trends(
        metrics,
        analysis
    )

    # ---------------------------------------------------
    # DETECT ANOMALIES
    # ---------------------------------------------------

    anomalies = detect_anomalies(
        metrics,
        analysis
    )

    # ---------------------------------------------------
    # GENERATE BUSINESS RECOMMENDATIONS
    # ---------------------------------------------------

    recommendations = generate_business_recommendations(
        metrics
    )

    # ---------------------------------------------------
    # AI GENERATED EXECUTIVE SUMMARY
    # ---------------------------------------------------

    ai_summary = generate_ai_summary(
        analysis.get("llm_context", analysis)
    )

    # ---------------------------------------------------
    # FALLBACKS
    # ---------------------------------------------------

    if not trends:

        trends.append({

            "type": "General",

            "severity": "low",

            "message": "No major trends detected."
        })

    if not anomalies:

        anomalies.append({

            "type": "General",

            "severity": "low",

            "message": "No significant anomalies detected."
        })

    # ---------------------------------------------------
    # MEMORY STORAGE
    # ---------------------------------------------------

    memory.store(
        "latest_trends",
        trends
    )

    memory.store(
        "latest_anomalies",
        anomalies
    )

    memory.store(
        "latest_ai_summary",
        ai_summary
    )

    # ---------------------------------------------------
    # FINAL OUTPUT
    # ---------------------------------------------------

    return {

        "trends": trends[:5],

        "anomalies": anomalies[:5],

        "recommendations": recommendations[:5],

        "executive_summary": ai_summary
    }