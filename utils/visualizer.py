import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from memory.memory import AgentMemory


memory = AgentMemory()


# ---------------------------------------------------
# DETECT COLUMN TYPES
# ---------------------------------------------------

def detect_columns(df):

    numeric_cols = list(
        df.select_dtypes(include=["number"]).columns
    )

    categorical_cols = list(
        df.select_dtypes(exclude=["number"]).columns
    )

    datetime_cols = []

    for col in df.columns:

        try:

            converted = pd.to_datetime(
                df[col],
                errors="coerce"
            )

            if converted.notna().sum() > 0.7 * len(df):

                datetime_cols.append(col)

        except Exception:

            pass

    return {

        "numeric": numeric_cols,

        "categorical": categorical_cols,

        "datetime": datetime_cols
    }


# ---------------------------------------------------
# GENERATE CHART PLAN
# ---------------------------------------------------

def generate_chart_plan(df):

    cols = detect_columns(df)

    numeric_cols = cols["numeric"]

    categorical_cols = cols["categorical"]

    datetime_cols = cols["datetime"]

    chart_plan = []

    # ---------------------------------------------------
    # TIME SERIES
    # ---------------------------------------------------

    if datetime_cols and numeric_cols:

        chart_plan.append({

            "type": "line",

            "x": datetime_cols[0],

            "y": numeric_cols[0],

            "reason": "Trend analysis over time"
        })

    # ---------------------------------------------------
    # CATEGORY VS KPI
    # ---------------------------------------------------

    for cat_col in categorical_cols:

        unique_count = df[cat_col].nunique()

        # Avoid high-cardinality charts
        if unique_count <= 10 and numeric_cols:

            chart_plan.append({

                "type": "bar",

                "x": cat_col,

                "y": numeric_cols[0],

                "reason": "Compare metrics across categories"
            })

    # ---------------------------------------------------
    # NUMERIC DISTRIBUTION
    # ---------------------------------------------------

    for num_col in numeric_cols[:2]:

        chart_plan.append({

            "type": "histogram",

            "x": num_col,

            "reason": "Analyze value distribution"
        })

    # ---------------------------------------------------
    # CORRELATION / RELATIONSHIP
    # ---------------------------------------------------

    if len(numeric_cols) >= 2:

        chart_plan.append({

            "type": "scatter",

            "x": numeric_cols[0],

            "y": numeric_cols[1],

            "reason": "Identify relationships and correlations"
        })

    return chart_plan[:5]


# ---------------------------------------------------
# CREATE CHARTS
# ---------------------------------------------------

def create_chart(df, plan):

    chart_type = plan["type"]

    fig = plt.figure(figsize=(8, 5))

    # ---------------------------------------------------
    # BAR CHART
    # ---------------------------------------------------

    if chart_type == "bar":

        df.groupby(plan["x"])[plan["y"]] \
            .sum() \
            .plot(kind="bar")

        plt.xlabel(plan["x"])

        plt.ylabel(plan["y"])

    # ---------------------------------------------------
    # LINE CHART
    # ---------------------------------------------------

    elif chart_type == "line":

        df.groupby(plan["x"])[plan["y"]] \
            .sum() \
            .plot(kind="line")

        plt.xlabel(plan["x"])

        plt.ylabel(plan["y"])

    # ---------------------------------------------------
    # HISTOGRAM
    # ---------------------------------------------------

    elif chart_type == "histogram":

        df[plan["x"]].plot(
            kind="hist",
            bins=20
        )

        plt.xlabel(plan["x"])

    # ---------------------------------------------------
    # SCATTER PLOT
    # ---------------------------------------------------

    elif chart_type == "scatter":

        plt.scatter(

            df[plan["x"]],

            df[plan["y"]]
        )

        plt.xlabel(plan["x"])

        plt.ylabel(plan["y"])

    plt.title(plan["reason"])

    plt.tight_layout()

    return fig


# ---------------------------------------------------
# MAIN VISUALIZATION ENGINE
# ---------------------------------------------------

def plot_charts(df):

    chart_plan = generate_chart_plan(df)

    charts = []

    for plan in chart_plan:

        try:

            fig = create_chart(df, plan)

            charts.append({

                "figure": fig,

                "metadata": plan
            })

        except Exception as e:

            print(
                f"Chart generation failed: {e}"
            )

    # ---------------------------------------------------
    # MEMORY STORAGE
    # ---------------------------------------------------

    memory.store(

        "chart_plan",

        chart_plan
    )

    return charts