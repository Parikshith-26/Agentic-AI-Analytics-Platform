
import pandas as pd

from memory.memory import AgentMemory


memory = AgentMemory()


# ---------------------------------------------------
# DETECT FILE TYPE
# ---------------------------------------------------

def detect_file_type(filename):

    filename = filename.lower()

    if filename.endswith(".csv"):

        return "csv"

    if (
        filename.endswith(".xlsx")
        or filename.endswith(".xls")
    ):

        return "excel"

    return "unknown"


# ---------------------------------------------------
# SAFE CSV LOADER
# ---------------------------------------------------

def load_csv(file):

    encodings = [

        "utf-8",

        "latin1",

        "ISO-8859-1"
    ]

    separators = [

        ",",

        "\t",

        ";"
    ]

    for encoding in encodings:

        for sep in separators:

            try:

                if hasattr(file, "seek"):

                    file.seek(0)

                df = pd.read_csv(

                    file,

                    encoding=encoding,

                    sep=sep
                )

                if df.shape[1] > 1:

                    return df

            except Exception:

                continue

    raise Exception(
        "Unable to parse CSV file."
    )


# ---------------------------------------------------
# SAFE EXCEL LOADER
# ---------------------------------------------------

def load_excel(file):

    try:

        if hasattr(file, "seek"):

            file.seek(0)

        df = pd.read_excel(file)

        return df

    except Exception as e:

        raise Exception(
            f"Excel parsing failed: {e}"
        )


# ---------------------------------------------------
# GENERATE PROFILE
# ---------------------------------------------------

def generate_data_profile(df):

    profile = {

        "rows": int(df.shape[0]),

        "columns": int(df.shape[1]),

        "column_names": list(df.columns),

        "missing_values": int(
            df.isnull().sum().sum()
        ),

        "duplicate_rows": int(
            df.duplicated().sum()
        ),

        "numeric_columns": list(

            df.select_dtypes(
                include=["number"]
            ).columns
        ),

        "categorical_columns": list(

            df.select_dtypes(
                exclude=["number"]
            ).columns
        )
    }

    return profile


# ---------------------------------------------------
# MAIN LOADER
# ---------------------------------------------------

def load_data(file):

    filename = (

        file.name

        if hasattr(file, "name")

        else str(file)
    )

    file_type = detect_file_type(
        filename
    )

    try:

        # CSV
        if file_type == "csv":

            df = load_csv(file)

        # EXCEL
        elif file_type == "excel":

            df = load_excel(file)

        else:

            raise Exception(
                "Unsupported file format."
            )

    except Exception as e:

        raise Exception(
            f"Data loading failed: {e}"
        )

    # ---------------------------------------------------
    # CLEAN EMPTY ROWS/COLUMNS
    # ---------------------------------------------------

    df = df.dropna(
        how="all"
    )

    df = df.dropna(
        axis=1,
        how="all"
    )

    # ---------------------------------------------------
    # PROFILE
    # ---------------------------------------------------

    profile = generate_data_profile(df)

    memory.store(
        "data_profile",
        profile
    )

    return df
