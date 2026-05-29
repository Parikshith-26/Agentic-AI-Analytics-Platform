import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

from memory.memory import AgentMemory


memory = AgentMemory()


# ---------------------------------------------------
# DETECT DATE COLUMN
# ---------------------------------------------------

def detect_date_column(df):

    for col in df.columns:

        try:

            converted = pd.to_datetime(
                df[col],
                errors="coerce"
            )

            if converted.notna().sum() > 0.7 * len(df):

                return col

        except Exception:

            pass

    return None


# ---------------------------------------------------
# DETECT TARGET COLUMN
# ---------------------------------------------------

def detect_target_column(df):

    priority_columns = [

        "total_sale",

        "sales",

        "revenue",

        "profit"
    ]

    for col in priority_columns:

        if col in df.columns:

            return col

    numeric_cols = list(

        df.select_dtypes(
            include=["number"]
        ).columns
    )

    if numeric_cols:

        return numeric_cols[0]

    return None


# ---------------------------------------------------
# FORECAST AGENT
# ---------------------------------------------------

def forecast_agent(df):

    date_col = detect_date_column(df)

    target_col = detect_target_column(df)

    if not date_col or not target_col:

        return {

            "status": "error",

            "message": "Forecasting requires date and numeric columns."
        }

    # ---------------------------------------------------
    # PREPARE DATA
    # ---------------------------------------------------

    temp_df = df[[date_col, target_col]].copy()

    temp_df[date_col] = pd.to_datetime(
        temp_df[date_col]
    )

    temp_df = temp_df.sort_values(
        by=date_col
    )

    temp_df["time_index"] = range(
        len(temp_df)
    )

    X = temp_df[["time_index"]]

    y = temp_df[target_col]

    # ---------------------------------------------------
    # TRAIN MODEL
    # ---------------------------------------------------

    model = LinearRegression()

    model.fit(X, y)

    # ---------------------------------------------------
    # FUTURE PREDICTIONS
    # ---------------------------------------------------

    future_indices = np.array(

        range(
            len(temp_df),
            len(temp_df) + 7
        )

    ).reshape(-1, 1)

    predictions = model.predict(
        future_indices
    )

    forecast_results = {

        "forecast_column": target_col,

        "future_predictions": [

            round(float(pred), 2)

            for pred in predictions
        ]
    }

    # ---------------------------------------------------
    # MEMORY STORAGE
    # ---------------------------------------------------

    memory.store(
        "forecast_results",
        forecast_results
    )

    return forecast_results