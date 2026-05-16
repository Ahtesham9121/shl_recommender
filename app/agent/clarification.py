class ClarificationHandler:

    def needs_clarification(
        self,
        parsed_query
    ):

        has_skills = len(
            parsed_query.get(
                "skills",
                []
            )
        ) > 0

        has_seniority = (
            parsed_query.get(
                "seniority"
            )
            is not None
        )

        return not (
            has_skills
            or has_seniority
        )

    def clarification_question(self):

        return (
            "Could you clarify the hiring "
            "requirements? Please mention:\n"
            "- role\n"
            "- seniority level\n"
            "- required skills\n"
            "- constraints (remote, adaptive, duration)"
        )