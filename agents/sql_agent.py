import duckdb
import pandas as pd
import re

from models.ollama_client import ask_llm
from memory.memory import AgentMemory


# ---------------------------------------------------
# MEMORY INITIALIZATION
# ---------------------------------------------------

memory = AgentMemory()


# ---------------------------------------------------
# SQL EXTRACTION
# ---------------------------------------------------

def extract_sql(text):

    if not text:
        return None

    text = text.strip()

    match = re.search(
        r"(SELECT .*?;)",
        text,
        re.IGNORECASE | re.DOTALL
    )

    if match:

        sql = match.group(1)

        sql = " ".join(sql.split())

        return sql

    return None


# ---------------------------------------------------
# COLUMN NORMALIZATION
# ---------------------------------------------------

def normalize_column_names(
    sql,
    columns
):

    sql_lower = sql.lower()

    for col in columns:

        normalized = col.replace("_", " ")

        sql_lower = sql_lower.replace(
            normalized,
            col
        )

    return sql_lower


# ---------------------------------------------------
# SQL VALIDATION
# ---------------------------------------------------

def validate_sql(sql):

    dangerous_keywords = [

        "drop",
        "delete",
        "truncate",
        "update",
        "insert",
        "alter"

    ]

    sql_lower = sql.lower()

    for keyword in dangerous_keywords:

        if keyword in sql_lower:

            return False

    return sql_lower.startswith("select")


# ---------------------------------------------------
# SQL AUTO CORRECTION
# ---------------------------------------------------

def auto_fix_sql(sql):

    sql = sql.replace(";;", ";")

    sql = sql.replace(
        "limit 10;",
        "limit 10"
    )

    return sql.strip()


# ---------------------------------------------------
# SCHEMA GENERATION
# ---------------------------------------------------

def generate_schema_context(df):

    schema = []

    for col in df.columns:

        dtype = str(df[col].dtype)

        schema.append(
            f"{col} ({dtype})"
        )

    return "\n".join(schema)


# ---------------------------------------------------
# FALLBACK QUERY SYSTEM
# ---------------------------------------------------

def fallback_query(user_query):

    user_query = user_query.lower()

    fallback_map = {

        "top customers": """
            SELECT customer_id,
            SUM(total_sale) AS total_sales
            FROM df
            GROUP BY customer_id
            ORDER BY total_sales DESC
            LIMIT 5;
        """,

        "top products": """
            SELECT product_id,
            SUM(quantity) AS total_quantity
            FROM df
            GROUP BY product_id
            ORDER BY total_quantity DESC
            LIMIT 5;
        """,

        "total revenue": """
            SELECT SUM(total_sale)
            AS total_revenue
            FROM df;
        """,

        "average price": """
            SELECT AVG(price_per_unit)
            AS avg_price
            FROM df;
        """
    }

    for key in fallback_map:

        if key in user_query:

            return fallback_map[key]

    return None


# ---------------------------------------------------
# SQL GENERATION AGENT
# ---------------------------------------------------

def generate_sql(
    user_query,
    schema_context
):

    prompt = f"""
You are an expert SQL analyst.

Generate SQL ONLY.

DATABASE:
DuckDB

TABLE NAME:
df

SCHEMA:
{schema_context}

RULES:
- Output ONLY SQL
- Use exact column names
- Use valid DuckDB SQL
- Never explain
- Never use markdown
- Only SELECT queries allowed

QUESTION:
{user_query}
"""

    response = ask_llm(prompt)

    sql = extract_sql(response)

    return sql


# ---------------------------------------------------
# SQL EXECUTION
# ---------------------------------------------------

def execute_sql(sql):

    result = duckdb.query(sql).to_df()

    return result


# ---------------------------------------------------
# MAIN SQL AGENT
# ---------------------------------------------------

def query_data(
    df,
    user_query
):

    columns = list(df.columns)

    # Store query in memory
    memory.store(
        "last_sql_query",
        user_query
    )

    # ---------------------------------------------------
    # GENERATE SCHEMA CONTEXT
    # ---------------------------------------------------

    schema_context = generate_schema_context(df)

    # ---------------------------------------------------
    # GENERATE SQL
    # ---------------------------------------------------

    sql = generate_sql(
        user_query,
        schema_context
    )

    # ---------------------------------------------------
    # FALLBACK IF SQL FAILS
    # ---------------------------------------------------

    if not sql:

        sql = fallback_query(user_query)

    if not sql:

        return {
            "status": "error",
            "message": "Unable to generate SQL query."
        }

    # ---------------------------------------------------
    # NORMALIZE SQL
    # ---------------------------------------------------

    sql = normalize_column_names(
        sql,
        columns
    )

    sql = auto_fix_sql(sql)

    # ---------------------------------------------------
    # VALIDATE SQL
    # ---------------------------------------------------

    if not validate_sql(sql):

        return {
            "status": "error",
            "message": "Unsafe SQL detected."
        }

    # Save SQL to memory
    memory.store(
        "generated_sql",
        sql
    )

    # ---------------------------------------------------
    # EXECUTE SQL
    # ---------------------------------------------------

    try:

        result = execute_sql(sql)

        memory.store(
            "last_sql_result",
            result.head().to_dict()
        )

        return {

            "status": "success",

            "sql": sql,

            "rows": len(result),

            "result": result
        }

    except Exception as e:

        # Retry using fallback
        fallback_sql = fallback_query(
            user_query
        )

        if fallback_sql:

            try:

                result = execute_sql(
                    fallback_sql
                )

                return {

                    "status": "fallback_success",

                    "sql": fallback_sql,

                    "rows": len(result),

                    "result": result
                }

            except Exception:

                pass

        return {

            "status": "error",

            "message": str(e)
        }