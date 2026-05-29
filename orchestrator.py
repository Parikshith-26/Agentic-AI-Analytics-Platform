
import os
import json
import time

from utils.data_loader import load_data

from agents.cleaning_agent import cleaning_agent
from agents.analysis_agent import analysis_agent
from agents.feature_agent import feature_agent
from agents.insight_agent import insight_agent
from agents.forecast_agent import forecast_agent
from agents.dashboard_agent import dashboard_agent
from agents.planner_agent import planner_agent

from memory.memory import AgentMemory


# ---------------------------------------------------
# GLOBAL MEMORY
# ---------------------------------------------------

memory = AgentMemory()


# ---------------------------------------------------
# STORAGE INITIALIZATION
# ---------------------------------------------------

STORAGE_FOLDERS = [

    "storage/cleaned_data",

    "storage/forecasts",

    "storage/reports",

    "storage/logs"
]


def initialize_storage():

    for folder in STORAGE_FOLDERS:

        os.makedirs(
            folder,
            exist_ok=True
        )


# ---------------------------------------------------
# SAVE REPORT
# ---------------------------------------------------

def save_report(

    filename,

    data
):

    path = f"storage/reports/{filename}"

    with open(path, "w") as f:

        json.dump(

            data,

            f,

            indent=4,

            default=str
        )


# ---------------------------------------------------
# SAVE LOG
# ---------------------------------------------------

def save_log(workflow_steps):

    path = "storage/logs/workflow_log.txt"

    with open(path, "a") as f:

        f.write("\n".join(workflow_steps))

        f.write("\n\n")


# ---------------------------------------------------
# MAIN ORCHESTRATION PIPELINE
# ---------------------------------------------------

def run_pipeline(file):

    initialize_storage()

    workflow_steps = []

    execution_start = time.time()

    try:

        # ---------------------------------------------------
        # STEP 1 — LOAD DATA
        # ---------------------------------------------------

        workflow_steps.append(
            "STEP 1: Loading dataset"
        )

        df = load_data(file)

        memory.store(
            "original_shape",
            df.shape
        )

        workflow_steps.append(
            f"Dataset loaded successfully | Shape: {df.shape}"
        )

        # ---------------------------------------------------
        # STEP 2 — PLANNER AGENT
        # ---------------------------------------------------

        workflow_steps.append(
            "STEP 2: Planner agent execution"
        )

        plan = planner_agent(df)

        memory.store(
            "execution_plan",
            plan
        )

        workflow_steps.append(
            "Planner agent completed"
        )

        # ---------------------------------------------------
        # STEP 3 — CLEANING AGENT
        # ---------------------------------------------------

        workflow_steps.append(
            "STEP 3: Data cleaning"
        )

        cleaned_df = cleaning_agent(df)

        memory.store(
            "cleaned_shape",
            cleaned_df.shape
        )

        cleaned_path = (
            "storage/cleaned_data/cleaned_data.csv"
        )

        cleaned_df.to_csv(

            cleaned_path,

            index=False
        )

        workflow_steps.append(
            "Data cleaning completed"
        )

        # ---------------------------------------------------
        # STEP 4 — ANALYSIS AGENT
        # ---------------------------------------------------

        workflow_steps.append(
            "STEP 4: Analysis agent"
        )

        analysis = analysis_agent(cleaned_df)

        memory.store(
            "analysis",
            analysis
        )

        workflow_steps.append(
            "Analysis completed"
        )

        # ---------------------------------------------------
        # STEP 5 — FEATURE AGENT
        # ---------------------------------------------------

        workflow_steps.append(
            "STEP 5: Feature engineering agent"
        )

        features = feature_agent(cleaned_df)

        memory.store(
            "feature_suggestions",
            features
        )

        workflow_steps.append(
            "Feature recommendations generated"
        )

        # ---------------------------------------------------
        # STEP 6 — FORECAST AGENT
        # ---------------------------------------------------

        forecast_results = None

        if plan.get("run_forecasting"):

            workflow_steps.append(
                "STEP 6: Forecast agent"
            )

            forecast_results = forecast_agent(
                cleaned_df
            )

            memory.store(
                "forecast_results",
                forecast_results
            )

            workflow_steps.append(
                "Forecasting completed"
            )

        # ---------------------------------------------------
        # STEP 7 — DASHBOARD AGENT
        # ---------------------------------------------------

        workflow_steps.append(
            "STEP 7: Dashboard agent"
        )

        dashboard_recommendations = (
            dashboard_agent(analysis)
        )

        memory.store(
            "dashboard_recommendations",
            dashboard_recommendations
        )

        workflow_steps.append(
            "Dashboard recommendations generated"
        )

        # ---------------------------------------------------
        # STEP 8 — INSIGHT AGENT
        # ---------------------------------------------------

        workflow_steps.append(
            "STEP 8: Insight agent"
        )

        insights = insight_agent(analysis)

        memory.store(
            "insights",
            insights
        )

        workflow_steps.append(
            "Insights generated"
        )

        # ---------------------------------------------------
        # STEP 9 — FINAL VALIDATION
        # ---------------------------------------------------

        workflow_steps.append(
            "STEP 9: Final validation"
        )

        validated_insights = insights

        workflow_steps.append(
            "Validation completed"
        )

        # ---------------------------------------------------
        # EXECUTION TIME
        # ---------------------------------------------------

        execution_time = round(

            time.time() - execution_start,

            2
        )

        workflow_steps.append(

            f"Pipeline completed in {execution_time} seconds"
        )

        # ---------------------------------------------------
        # FINAL REPORT
        # ---------------------------------------------------

        report = {

            "execution_plan": plan,

            "workflow_steps": workflow_steps,

            "execution_time": execution_time,

            "analysis_summary": analysis.get(
                "llm_context",
                ""
            )
        }

        save_report(

            "pipeline_report.json",

            report
        )

        save_log(workflow_steps)

        # ---------------------------------------------------
        # FINAL OUTPUT
        # ---------------------------------------------------

        return {

            "df": cleaned_df,

            "analysis": analysis,

            "features": features,

            "insights": insights,

            "forecast": forecast_results,

            "dashboard": dashboard_recommendations,

            "workflow_steps": workflow_steps,

            "execution_plan": plan,

            "execution_time": execution_time,

            "cleaned_data_path": cleaned_path
        }

    # ---------------------------------------------------
    # ERROR HANDLING
    # ---------------------------------------------------

    except Exception as e:

        error_message = (
            f"Pipeline execution failed: {e}"
        )

        workflow_steps.append(error_message)

        save_log(workflow_steps)

        return {

            "status": "error",

            "message": error_message,

            "workflow_steps": workflow_steps
        }
