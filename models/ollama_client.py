from groq import Groq
import os
from dotenv import load_dotenv

from memory.memory import AgentMemory


# ---------------------------------------------------
# LOAD ENV VARIABLES
# ---------------------------------------------------

load_dotenv()


# ---------------------------------------------------
# MEMORY
# ---------------------------------------------------

memory = AgentMemory()


# ---------------------------------------------------
# GROQ CLIENT
# ---------------------------------------------------

client = Groq(

    api_key=os.getenv(
        "GROQ_API_KEY"
    )
)


# ---------------------------------------------------
# MODEL CONFIG
# ---------------------------------------------------

PRIMARY_MODEL = "llama-3.1-8b-instant"

TEMPERATURE = 0.3


# ---------------------------------------------------
# SYSTEM PROMPTS
# ---------------------------------------------------

SYSTEM_PROMPTS = {

    "business_analyst": """
You are an expert AI business analyst.

Provide:
- concise analysis
- business insights
- strategic recommendations
- executive-level clarity
""",

    "critic": """
You are an AI critic agent.

Improve:
- clarity
- business relevance
- readability
"""
}


# ---------------------------------------------------
# MAIN LLM FUNCTION
# ---------------------------------------------------

def ask_llm(

    prompt,

    task_type="business_analyst"
):

    system_prompt = SYSTEM_PROMPTS.get(

        task_type,

        SYSTEM_PROMPTS[
            "business_analyst"
        ]
    )

    try:

        response = client.chat.completions.create(

            model=PRIMARY_MODEL,

            messages=[

                {
                    "role": "system",

                    "content": system_prompt
                },

                {
                    "role": "user",

                    "content": prompt
                }
            ],

            temperature=TEMPERATURE
        )

        answer = (
            response
            .choices[0]
            .message
            .content
        )

        # ---------------------------------------------------
        # MEMORY STORAGE
        # ---------------------------------------------------

        memory.store(
            "latest_prompt",
            prompt
        )

        memory.store(
            "latest_response",
            answer
        )

        return answer

    except Exception as e:

        return f"""
Groq API Error:

{str(e)}
"""