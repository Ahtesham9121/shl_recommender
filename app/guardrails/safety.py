

class SafetyGuard:

    


 def detect_prompt_injection(self, query):

    print("QUERY RECEIVED IN SAFETY:")
    print(query)

    query_lower = query.lower()

    injection_patterns = [
        "ignore previous instructions",
        "act as",
        "system prompt",
        "override",
        "bypass",
        "pretend",
        "jailbreak"
    ]

    for pattern in injection_patterns:

        if pattern in query_lower:

            print("MATCHED PATTERN:")
            print(pattern)

            return True

    return False

 def detect_out_of_scope(self, query):

    query_lower = query.lower()

    unrelated_topics = [
        "weather",
        "football",
        "movie",
        "politics",
        "recipe",
        "music",
        "bitcoin"
    ]

    for topic in unrelated_topics:

        if topic in query_lower:
            return True

    return False

 def refusal_response(self):

    return {
        "reply": (
            "I can only assist with "
            "SHL assessment recommendations."
        ),
        "recommendations": [],
        "end_of_conversation": False
    }

 def injection_response(self):

    return {
        "reply": (
            "I cannot follow instructions "
            "that attempt to override system behavior."
        ),
        "recommendations": [],
        "end_of_conversation": False
    }

