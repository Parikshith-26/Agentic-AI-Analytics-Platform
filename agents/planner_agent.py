import pandas as pd


# ---------------------------------------------------
# PLANNER AGENT
# ---------------------------------------------------

def planner_agent(df):

    plan = {

        "run_cleaning": True,

        "run_analysis": True,

        "run_dashboard": True,

        "run_forecasting": False,

        "run_feature_engineering": True
    }

    # ---------------------------------------------------
    # DETECT DATETIME COLUMNS
    # ---------------------------------------------------

    datetime_detected = False

    for col in df.columns:

        try:

            converted = pd.to_datetime(
                df[col],
                errors="coerce"
            )

            if converted.notna().sum() > 0.7 * len(df):

                datetime_detected = True

                break

        except Exception:

            pass

    # ---------------------------------------------------
    # ENABLE FORECASTING
    # ---------------------------------------------------

    numeric_cols = df.select_dtypes(
        include=["number"]
    ).columns

    if datetime_detected and len(numeric_cols) > 0:

        plan["run_forecasting"] = True

    # ---------------------------------------------------
    # DATA QUALITY CHECK
    # ---------------------------------------------------

    missing_ratio = (
        df.isnull().mean().mean()
    )

    if missing_ratio < 0.01:

        plan["run_cleaning"] = False

    return plan