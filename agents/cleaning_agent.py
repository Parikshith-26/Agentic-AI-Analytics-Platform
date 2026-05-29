import pandas as pd
import numpy as np

from memory.memory import AgentMemory


# ---------------------------------------------------
# MEMORY INITIALIZATION
# ---------------------------------------------------

memory = AgentMemory()


# ---------------------------------------------------
# COLUMN STANDARDIZATION
# ---------------------------------------------------

def standardize_columns(df):

    df.columns = (

        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    return df


# ---------------------------------------------------
# SAFE TYPE CONVERSION
# ---------------------------------------------------

def convert_numeric_columns(df):

    conversion_report = {}

    for col in df.columns:

        original_nulls = df[col].isnull().sum()

        try:

            cleaned = (
                df[col]
                .astype(str)
                .str.replace(",", "")
                .str.strip()
            )

            converted = pd.to_numeric(
                cleaned,
                errors="coerce"
            )

            # Convert only if enough values valid
            valid_ratio = (
                converted.notna().sum()
                / len(df)
            )

            if valid_ratio > 0.6:

                df[col] = converted

                conversion_report[col] = (
                    "numeric"
                )

        except Exception:

            conversion_report[col] = (
                "unchanged"
            )

    return df, conversion_report


# ---------------------------------------------------
# HANDLE MISSING VALUES
# ---------------------------------------------------

def handle_missing_values(df):

    missing_report = {}

    for col in df.columns:

        missing_before = (
            df[col].isnull().sum()
        )

        # Numeric columns
        if pd.api.types.is_numeric_dtype(df[col]):

            median_value = df[col].median()

            df[col] = df[col].fillna(
                median_value
            )

            strategy = "median"

        # Categorical columns
        else:

            if df[col].mode().empty:

                fill_value = "Unknown"

            else:

                fill_value = (
                    df[col].mode()[0]
                )

            df[col] = df[col].fillna(
                fill_value
            )

            strategy = "mode"

        missing_after = (
            df[col].isnull().sum()
        )

        missing_report[col] = {

            "before": int(missing_before),

            "after": int(missing_after),

            "strategy": strategy
        }

    return df, missing_report


# ---------------------------------------------------
# OUTLIER DETECTION
# ---------------------------------------------------

def detect_outliers(df):

    outlier_report = {}

    numeric_cols = df.select_dtypes(
        include=["number"]
    ).columns

    for col in numeric_cols:

        q1 = df[col].quantile(0.25)

        q3 = df[col].quantile(0.75)

        iqr = q3 - q1

        lower = q1 - 1.5 * iqr

        upper = q3 + 1.5 * iqr

        outliers = df[
            (
                df[col] < lower
            )
            |
            (
                df[col] > upper
            )
        ]

        outlier_report[col] = {

            "count": int(len(outliers)),

            "lower_bound": float(lower),

            "upper_bound": float(upper)
        }

    return outlier_report


# ---------------------------------------------------
# OPTIONAL OUTLIER REMOVAL
# ---------------------------------------------------

def remove_outliers(df):

    numeric_cols = df.select_dtypes(
        include=["number"]
    ).columns

    cleaned_df = df.copy()

    for col in numeric_cols:

        q1 = cleaned_df[col].quantile(0.25)

        q3 = cleaned_df[col].quantile(0.75)

        iqr = q3 - q1

        lower = q1 - 1.5 * iqr

        upper = q3 + 1.5 * iqr

        cleaned_df = cleaned_df[
            (
                cleaned_df[col] >= lower
            )
            &
            (
                cleaned_df[col] <= upper
            )
        ]

    return cleaned_df


# ---------------------------------------------------
# DATA QUALITY SCORE
# ---------------------------------------------------

def calculate_quality_score(df):

    missing_ratio = (
        df.isnull().mean().mean()
    )

    duplicate_ratio = (
        df.duplicated().mean()
    )

    score = (

        100
        - (missing_ratio * 50)
        - (duplicate_ratio * 50)
    )

    return round(score, 2)


# ---------------------------------------------------
# MAIN CLEANING AGENT
# ---------------------------------------------------

def cleaning_agent(

    df,

    remove_outlier_rows=False

):

    cleaning_log = {}

    original_shape = df.shape

    # ---------------------------------------------------
    # REMOVE DUPLICATES
    # ---------------------------------------------------

    duplicate_count = int(
        df.duplicated().sum()
    )

    df = df.drop_duplicates()

    cleaning_log["duplicates_removed"] = (
        duplicate_count
    )

    # ---------------------------------------------------
    # STANDARDIZE COLUMNS
    # ---------------------------------------------------

    df = standardize_columns(df)

    # ---------------------------------------------------
    # TYPE CONVERSION
    # ---------------------------------------------------

    df, conversion_report = (

        convert_numeric_columns(df)
    )

    cleaning_log["type_conversion"] = (
        conversion_report
    )

    # ---------------------------------------------------
    # HANDLE MISSING VALUES
    # ---------------------------------------------------

    df, missing_report = (
        handle_missing_values(df)
    )

    cleaning_log["missing_values"] = (
        missing_report
    )

    # ---------------------------------------------------
    # OUTLIER DETECTION
    # ---------------------------------------------------

    outlier_report = detect_outliers(df)

    cleaning_log["outliers"] = (
        outlier_report
    )

    # ---------------------------------------------------
    # OPTIONAL OUTLIER REMOVAL
    # ---------------------------------------------------

    if remove_outlier_rows:

        df = remove_outliers(df)

        cleaning_log[
            "outlier_rows_removed"
        ] = True

    else:

        cleaning_log[
            "outlier_rows_removed"
        ] = False

    # ---------------------------------------------------
    # QUALITY SCORE
    # ---------------------------------------------------

    quality_score = calculate_quality_score(
        df
    )

    cleaning_log["quality_score"] = (
        quality_score
    )

    # ---------------------------------------------------
    # FINAL REPORT
    # ---------------------------------------------------

    cleaning_log["original_shape"] = (
        original_shape
    )

    cleaning_log["final_shape"] = (
        df.shape
    )

    # ---------------------------------------------------
    # MEMORY STORAGE
    # ---------------------------------------------------

    memory.store(
        "cleaning_log",
        cleaning_log
    )

    return df