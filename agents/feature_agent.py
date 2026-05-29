from models.ollama_client import ask_llm
from memory.memory import AgentMemory


# ---------------------------------------------------
# MEMORY INITIALIZATION
# ---------------------------------------------------

memory = AgentMemory()


# ---------------------------------------------------
# DETECT DATASET TYPE
# ---------------------------------------------------

def detect_dataset_type(columns):

    columns_lower = [

        col.lower()

        for col in columns
    ]

    if (
        "customer_id" in columns_lower
        or "total_sale" in columns_lower
    ):

        return "Retail / Sales Analytics"

    if (
        "date" in str(columns_lower)
    ):

        return "Time Series Analytics"

    return "General Business Dataset"


# ---------------------------------------------------
# BUILD FEATURE CONTEXT
# ---------------------------------------------------

def build_feature_context(df):

    columns = list(df.columns)

    numeric_columns = list(

        df.select_dtypes(
            include=["number"]
        ).columns
    )

    categorical_columns = list(

        df.select_dtypes(
            exclude=["number"]
        ).columns
    )

    return {

        "columns": columns,

        "numeric_columns": numeric_columns,

        "categorical_columns": categorical_columns,

        "shape": df.shape
    }


# ---------------------------------------------------
# GENERATE FEATURE PROMPT
# ---------------------------------------------------

def generate_prompt(

    feature_context,

    dataset_type
):

    prompt = f"""
You are an AI feature engineering expert.

DATASET TYPE:
{dataset_type}

DATASET INFO:
{feature_context}

TASK:
Suggest 5 intelligent new features.

For each feature provide:

1. Feature Name
2. Feature Type
3. Business Purpose
4. How It Can Improve Analytics or ML
5. Suggested Formula or Logic

RULES:
- Use existing columns only
- Focus on business intelligence
- Focus on predictive analytics
- Keep explanations concise
"""

    return prompt


# ---------------------------------------------------
# MAIN FEATURE AGENT
# ---------------------------------------------------

def feature_agent(df):

    # ---------------------------------------------------
    # BUILD FEATURE CONTEXT
    # ---------------------------------------------------

    feature_context = build_feature_context(
        df
    )

    # ---------------------------------------------------
    # DETECT DATASET TYPE
    # ---------------------------------------------------

    dataset_type = detect_dataset_type(

        feature_context["columns"]
    )

    # ---------------------------------------------------
    # BUILD PROMPT
    # ---------------------------------------------------

    prompt = generate_prompt(

        feature_context,

        dataset_type
    )

    # ---------------------------------------------------
    # LLM GENERATION
    # ---------------------------------------------------

    response = ask_llm(

        prompt,

        task_type="business_analyst"
    )

    # ---------------------------------------------------
    # MEMORY STORAGE
    # ---------------------------------------------------

    memory.store(
        "feature_recommendations",
        response
    )

    # ---------------------------------------------------
    # STRUCTURED OUTPUT
    # ---------------------------------------------------

    return {

        "dataset_type": dataset_type,

        "feature_context": feature_context,

        "recommendations": response
    }