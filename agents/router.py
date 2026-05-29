from typing import Dict, List
import re
import json

from models.ollama_client import ask_llm
from memory.memory import AgentMemory


# ---------------------------------------------------
# MEMORY INITIALIZATION
# ---------------------------------------------------

memory = AgentMemory()


# ---------------------------------------------------
# QUERY ROUTER
# ---------------------------------------------------

class QueryRouter:

    def __init__(self):

        self.available_agents = {

            "sql": "Structured data querying",

            "forecast": "Predictive analytics",

            "visualization": "Dashboard and chart generation",

            "insight": "Business intelligence insights",

            "feedback": "Root-cause explanations",

            "rag": "Document retrieval and contextual QA",

            "llm": "General AI assistant"
        }

    # ---------------------------------------------------
    # PREPROCESS QUERY
    # ---------------------------------------------------

    def preprocess_query(
        self,
        query: str
    ) -> str:

        query = query.lower()

        query = re.sub(
            r"[^a-zA-Z0-9\s]",
            "",
            query
        )

        return query.strip()

    # ---------------------------------------------------
    # BUILD ROUTING PROMPT
    # ---------------------------------------------------

    def build_router_prompt(
        self,
        query: str
    ):

        prompt = f"""
You are an AI routing agent.

Your job:
Determine which AI agent should handle the query.

AVAILABLE AGENTS:
{self.available_agents}

USER QUERY:
{query}

INSTRUCTIONS:
- Detect primary intent
- Detect secondary intents
- Estimate confidence score
- Return ONLY JSON

FORMAT:
{{
    "primary_intent": "",
    "secondary_intents": [],
    "confidence": 0.0,
    "reason": ""
}}
"""

        return prompt

    # ---------------------------------------------------
    # FALLBACK RULE-BASED ROUTING
    # ---------------------------------------------------

    def fallback_route(
        self,
        query: str
    ):

        query = query.lower()

        if any(
            word in query
            for word in [
                "top",
                "sum",
                "average",
                "count",
                "revenue",
                "sales"
            ]
        ):

            return "sql"

        if any(
            word in query
            for word in [
                "forecast",
                "predict",
                "future"
            ]
        ):

            return "forecast"

        if any(
            word in query
            for word in [
                "dashboard",
                "chart",
                "graph"
            ]
        ):

            return "visualization"

        if any(
            word in query
            for word in [
                "why",
                "reason",
                "cause"
            ]
        ):

            return "feedback"

        return "llm"

    # ---------------------------------------------------
    # PARSE LLM OUTPUT
    # ---------------------------------------------------

    def parse_response(
        self,
        response
    ):

        try:

            json_match = re.search(
                r"\{.*\}",
                response,
                re.DOTALL
            )

            if json_match:

                parsed = json.loads(
                    json_match.group()
                )

                return parsed

        except Exception:

            pass

        return None

    # ---------------------------------------------------
    # MAIN ROUTING FUNCTION
    # ---------------------------------------------------

    def route_query(
        self,
        query: str
    ) -> Dict:

        cleaned_query = self.preprocess_query(
            query
        )

        # ---------------------------------------------------
        # MEMORY CONTEXT
        # ---------------------------------------------------

        previous_context = (
            memory.get_recent_context()
        )

        # ---------------------------------------------------
        # BUILD PROMPT
        # ---------------------------------------------------

        prompt = self.build_router_prompt(

            f"""
CURRENT QUERY:
{cleaned_query}

PREVIOUS CONTEXT:
{previous_context}
"""
        )

        # ---------------------------------------------------
        # LLM ROUTING
        # ---------------------------------------------------

        try:

            response = ask_llm(

                prompt,

                task_type="business_analyst"
            )

            parsed = self.parse_response(
                response
            )

            if parsed:

                result = {

                    "primary_intent": parsed.get(
                        "primary_intent",
                        "llm"
                    ),

                    "secondary_intents": parsed.get(
                        "secondary_intents",
                        []
                    ),

                    "confidence": parsed.get(
                        "confidence",
                        0.5
                    ),

                    "reason": parsed.get(
                        "reason",
                        "LLM-based routing"
                    ),

                    "routing_method": "llm"
                }

                memory.store(
                    "last_route",
                    result
                )

                return result

        except Exception as e:

            print(
                f"LLM routing failed: {e}"
            )

        # ---------------------------------------------------
        # FALLBACK ROUTING
        # ---------------------------------------------------

        fallback_intent = self.fallback_route(
            cleaned_query
        )

        fallback_result = {

            "primary_intent": fallback_intent,

            "secondary_intents": [],

            "confidence": 0.6,

            "reason": "Fallback keyword routing",

            "routing_method": "fallback"
        }

        memory.store(
            "last_route",
            fallback_result
        )

        return fallback_result


# ---------------------------------------------------
# TESTING
# ---------------------------------------------------

if __name__ == "__main__":

    router = QueryRouter()

    queries = [

        "Show top 5 products by revenue",

        "Why are profits decreasing?",

        "Predict next month sales",

        "Create dashboard for customer analysis"
    ]

    for query in queries:

        result = router.route_query(query)

        print("\nQuery:", query)

        print("Result:", result)