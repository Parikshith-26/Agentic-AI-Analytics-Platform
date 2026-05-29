from models.ollama_client import ask_llm
from memory.memory import AgentMemory


# ---------------------------------------------------
# MEMORY INITIALIZATION
# ---------------------------------------------------

memory = AgentMemory()


# ---------------------------------------------------
# DETECT KPI COLUMNS
# ---------------------------------------------------

def detect_kpis(metrics):

    kpis = []

    if "total_revenue" in metrics:

        kpis.append("Revenue")

    if "avg_order_value" in metrics:

        kpis.append("Average Order Value")

    if "total_quantity" in metrics:

        kpis.append("Sales Quantity")

    if "avg_price" in metrics:

        kpis.append("Average Price")

    return kpis


# ---------------------------------------------------
# DETECT DASHBOARD TYPE
# ---------------------------------------------------

def recommend_dashboard_type(columns):

    columns_lower = [
        col.lower()
        for col in columns
    ]

    if any(
        "date" in col
        or "time" in col
        for col in columns_lower
    ):

        return "Executive Time-Series Dashboard"

    if "customer_id" in columns_lower:

        return "Customer Analytics Dashboard"

    if "category" in columns_lower:

        return "Sales Performance Dashboard"

    return "General Business Intelligence Dashboard"


# ---------------------------------------------------
# GENERATE AI DASHBOARD PLAN
# ---------------------------------------------------

def generate_dashboard_prompt(

    columns,

    metrics,

    dashboard_type,

    kpis
):

    prompt = f"""
You are an AI BI dashboard architect.

AVAILABLE COLUMNS:
{columns}

BUSINESS METRICS:
{metrics}

DETECTED KPIs:
{kpis}

DASHBOARD TYPE:
{dashboard_type}

TASK:
Design an intelligent business dashboard.

INSTRUCTIONS:
- Suggest EXACTLY 5 visualizations
- Use ONLY available columns
- Recommend the BEST chart type
- Include KPI cards if relevant
- Explain WHY each visualization matters
- Focus on executive-level analytics

FORMAT:

1. Visualization:
2. Chart Type:
3. Columns Used:
4. Business Purpose:
5. Priority:
"""

    return prompt


# ---------------------------------------------------
# MAIN DASHBOARD AGENT
# ---------------------------------------------------

def dashboard_agent(analysis):

    columns = analysis.get(
        "columns",
        []
    )

    metrics = analysis.get(
        "metrics",
        {}
    )

    # ---------------------------------------------------
    # KPI DETECTION
    # ---------------------------------------------------

    kpis = detect_kpis(metrics)

    # ---------------------------------------------------
    # DASHBOARD TYPE
    # ---------------------------------------------------

    dashboard_type = recommend_dashboard_type(
        columns
    )

    # ---------------------------------------------------
    # GENERATE PROMPT
    # ---------------------------------------------------

    prompt = generate_dashboard_prompt(

        columns,

        metrics,

        dashboard_type,

        kpis
    )

    # ---------------------------------------------------
    # GENERATE AI RESPONSE
    # ---------------------------------------------------

    response = ask_llm(

        prompt,

        task_type="business_analyst"
    )

    # ---------------------------------------------------
    # MEMORY STORAGE
    # ---------------------------------------------------

    memory.store(
        "dashboard_type",
        dashboard_type
    )

    memory.store(
        "dashboard_recommendations",
        response
    )

    # ---------------------------------------------------
    # STRUCTURED OUTPUT
    # ---------------------------------------------------

    return {

        "dashboard_type": dashboard_type,

        "kpis": kpis,

        "recommendations": response
    }