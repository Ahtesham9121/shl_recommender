class ComparisonHandler:

    def is_compare_request(self, intent):

        return intent == "compare"

    def build_comparison_response(self, latest_query, recommendations):

        if not recommendations:

            return {
                "reply": (
                    "I can compare SHL assessments only when matching "
                    "catalog items are available from the retrieved catalog."
                ),
                "recommendations": [],
                "end_of_conversation": False
            }

        selected = recommendations[:2]

        comparison_lines = []

        for rec in selected:

            comparison_lines.append(
                f"{rec['name']} is categorized as {rec['test_type']}."
            )

        reply = (
            "Here is a grounded comparison based on the retrieved SHL catalog items. "
            + " ".join(comparison_lines)
            + " Use the recommendation URLs to verify the official catalog pages."
        )

        return {
            "reply": reply,
            "recommendations": selected,
            "end_of_conversation": False
        }