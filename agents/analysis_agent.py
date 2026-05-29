import pandas as pd
import numpy as np

from memory.memory import AgentMemory


# ---------------------------------------------------
# MEMORY INITIALIZATION
# ---------------------------------------------------

memory = AgentMemory()


# ---------------------------------------------------
# MAIN ANALYSIS AGENT
# ---------------------------------------------------

def analysis_agent(df):

    analysis = {}

    # ---------------------------------------------------
    # COLUMN STANDARDIZATION
    # ---------------------------------------------------

    if "quantiy" in df.columns:

        df = df.rename(
            columns={"quantiy": "quantity"}
        )

    # ---------------------------------------------------
    # BASIC DATASET INFO
    # ---------------------------------------------------

    analysis["shape"] = df.shape

    analysis["columns"] = list(df.columns)

    analysis["dtypes"] = (
        df.dtypes.astype(str).to_dict()
    )

    # ---------------------------------------------------
    # MISSING VALUE ANALYSIS
    # ---------------------------------------------------

    missing_values = (
        df.isnull().sum()
        .sort_values(ascending=False)
    )

    analysis["missing_values"] = (
        missing_values.to_dict()
    )

    analysis["missing_percentage"] = (

        (
            df.isnull().mean() * 100
        ).round(2).to_dict()
    )

    # ---------------------------------------------------
    # DUPLICATE ANALYSIS
    # ---------------------------------------------------

    analysis["duplicate_rows"] = int(
        df.duplicated().sum()
    )

    # ---------------------------------------------------
    # NUMERIC ANALYSIS
    # ---------------------------------------------------

    numeric_df = df.select_dtypes(
        include=["number"]
    )

    if not numeric_df.empty:

        analysis["summary_statistics"] = (

            numeric_df.describe()
            .round(2)
            .to_dict()
        )

    else:

        analysis["summary_statistics"] = {}

    # ---------------------------------------------------
    # CORRELATION ANALYSIS
    # ---------------------------------------------------

    if len(numeric_df.columns) >= 2:

        corr_matrix = numeric_df.corr()

        strong_corr = {}

        for col in corr_matrix.columns:

            correlations = corr_matrix[col]

            filtered = correlations[
                (correlations > 0.5)
                | (correlations < -0.5)
            ]

            strong_corr[col] = (
                filtered.round(2).to_dict()
            )

        analysis["strong_correlations"] = (
            strong_corr
        )

    else:

        analysis["strong_correlations"] = {}

    # ---------------------------------------------------
    # OUTLIER DETECTION
    # ---------------------------------------------------

    outliers = {}

    for col in numeric_df.columns:

        q1 = numeric_df[col].quantile(0.25)
        q3 = numeric_df[col].quantile(0.75)

        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        count = numeric_df[
            (
                numeric_df[col] < lower
            )
            |
            (
                numeric_df[col] > upper
            )
        ].shape[0]

        outliers[col] = int(count)

    analysis["outliers"] = outliers

    # ---------------------------------------------------
    # BUSINESS METRICS
    # ---------------------------------------------------

    metrics = {}

    # Revenue metrics
    if "total_sale" in df.columns:

        metrics["total_revenue"] = round(
            float(df["total_sale"].sum()),
            2
        )

        metrics["avg_order_value"] = round(
            float(df["total_sale"].mean()),
            2
        )

        metrics["max_sale"] = round(
            float(df["total_sale"].max()),
            2
        )

    # Quantity metrics
    if "quantity" in df.columns:

        metrics["total_quantity"] = int(
            df["quantity"].sum()
        )

    # Price metrics
    if "price_per_unit" in df.columns:

        metrics["avg_price"] = round(
            float(df["price_per_unit"].mean()),
            2
        )

    # Category metrics
    if "category" in df.columns:

        metrics["top_category"] = (
            df["category"]
            .mode()[0]
        )

        metrics["category_count"] = int(
            df["category"].nunique()
        )

    # Customer metrics
    if "customer_id" in df.columns:

        metrics["unique_customers"] = int(
            df["customer_id"].nunique()
        )

    analysis["metrics"] = metrics

    # ---------------------------------------------------
    # TREND DETECTION
    # ---------------------------------------------------

    trends = []

    if "total_sale" in df.columns:

        avg_sale = df["total_sale"].mean()

        max_sale = df["total_sale"].max()

        if max_sale > avg_sale * 3:

            trends.append(
                "High-value transactions detected."
            )

    if "quantity" in df.columns:

        if df["quantity"].mean() > 5:

            trends.append(
                "Large order quantities observed."
            )

    analysis["trends"] = trends

    # ---------------------------------------------------
    # DATA QUALITY SCORE
    # ---------------------------------------------------

    missing_ratio = df.isnull().mean().mean()

    duplicate_ratio = (
        df.duplicated().mean()
    )

    quality_score = (

        100
        - (missing_ratio * 50)
        - (duplicate_ratio * 50)

    )

    analysis["data_quality_score"] = round(
        quality_score,
        2
    )

    # ---------------------------------------------------
    # AI READY CONTEXT
    # ---------------------------------------------------

    analysis["llm_context"] = f"""

Dataset Shape:
{df.shape}

Columns:
{list(df.columns)}

Business Metrics:
{metrics}

Trends:
{trends}

Data Quality Score:
{quality_score}
"""

    # ---------------------------------------------------
    # MEMORY STORAGE
    # ---------------------------------------------------

    memory.store(
        "analysis_summary",
        analysis["llm_context"]
    )

    return analysis