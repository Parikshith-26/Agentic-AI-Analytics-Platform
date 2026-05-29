from models.ollama_client import ask_llm
from memory.memory import AgentMemory


# ---------------------------------------------------
# MEMORY INITIALIZATION
# ---------------------------------------------------

memory = AgentMemory()


# ---------------------------------------------------
# BUILD ANALYSIS CONTEXT
# ---------------------------------------------------

def build_context(analysis):

    metrics = analysis.get(
        "metrics",
        {}
    )

    trends = analysis.get(
        "trends",
        []
    )

    quality_score = analysis.get(
        "data_quality_score",
        "Unknown"
    )

    columns = analysis.get(
        "columns",
        []
    )

    context = f"""

DATASET OVERVIEW
----------------
Columns:
{columns}

Business Metrics:
{metrics}

Detected Trends:
{trends}

Data Quality Score:
{quality_score}

"""

    return context


# ---------------------------------------------------
# MAIN FEEDBACK AGENT
# ---------------------------------------------------

def feedback_agent(

    analysis,

    question
):

    # ---------------------------------------------------
    # BUILD CONTEXT
    # ---------------------------------------------------

    context = build_context(
        analysis
    )

    # ---------------------------------------------------
    # RETRIEVE MEMORY CONTEXT
    # ---------------------------------------------------

    previous_context = (
        memory.get_recent_context()
    )

    # ---------------------------------------------------
    # BUILD PROMPT
    # ---------------------------------------------------

    prompt = f"""
You are a senior AI business analyst.

Your role:
- explain WHY something is happening
- provide business reasoning
- identify possible causes
- suggest strategic improvements
- avoid technical jargon

CURRENT DATA CONTEXT:
{context}

PREVIOUS CONVERSATION CONTEXT:
{previous_context}

USER QUESTION:
{question}

INSTRUCTIONS:
1. Explain clearly
2. Use business-friendly language
3. Give root-cause reasoning
4. Mention possible risks
5. Suggest actionable improvements
6. Keep response concise
"""

    # ---------------------------------------------------
    # LLM RESPONSE
    # ---------------------------------------------------

    response = ask_llm(

        prompt,

        task_type="business_analyst"
    )

    # ---------------------------------------------------
    # STORE MEMORY
    # ---------------------------------------------------

    memory.store(
        "last_feedback_question",
        question
    )

    memory.store(
        "last_feedback_response",
        response
    )

    # ---------------------------------------------------
    # RETURN STRUCTURED OUTPUT
    # ---------------------------------------------------

    return {

        "question": question,

        "response": response,

        "response_type": "business_explanation"
    }