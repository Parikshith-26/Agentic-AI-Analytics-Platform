from models.ollama_client import ask_llm


# ---------------------------------------------------
# CRITIC AGENT
# ---------------------------------------------------

def critic_agent(content):

    prompt = f"""
You are an AI critic agent.

Review the following output.

TASKS:
- improve clarity
- remove hallucinations
- improve business relevance
- improve readability
- keep concise

CONTENT:
{content}
"""

    try:

        reviewed = ask_llm(

            prompt,

            task_type="critic"
        )

        return reviewed

    except Exception:

        return content