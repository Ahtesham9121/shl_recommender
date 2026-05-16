class IntentClassifier:

    def classify(self, query: str):

        query_lower = query.lower()

        final_keywords = [
            "looks good",
            "lock it in",
            "final",
            "that covers it",
            "keep this",
            "confirmed",
            "done"
        ]

        if any(keyword in query_lower for keyword in final_keywords):
            return "finalize"

        refusal_keywords = [
            "weather",
            "politics",
            "movie",
            "music",
            "recipe",
            "football"
        ]

        if any(word in query_lower for word in refusal_keywords):
            return "refuse"

        comparison_keywords = [
            "compare",
            "difference",
            "vs",
            "versus",
            "better"
        ]

        if any(word in query_lower for word in comparison_keywords):
            return "compare"

        refinement_keywords = [
            "add",
            "drop",
            "remove",
            "shorter",
            "more technical",
            "less technical",
            "remote",
            "adaptive",
            "quick",
            "entry level",
            "senior",
            "manager"
        ]

        if any(word in query_lower for word in refinement_keywords):
            return "refine"

        recommendation_keywords = [
            "recommend",
            "assessment",
            "test",
            "hiring",
            "developer",
            "engineer",
            "candidate"
        ]

        if any(word in query_lower for word in recommendation_keywords):
            return "recommend"

        return "clarify"