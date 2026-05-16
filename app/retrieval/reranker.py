import re


JOB_LEVELS = {
    "entry": ["Entry-Level", "Graduate"],
    "junior": ["Entry-Level", "Graduate"],
    "graduate": ["Graduate"],
    "mid": ["Mid-Professional"],
    "senior": ["Manager", "Director", "Executive"],
    "manager": ["Manager"],
    "executive": ["Executive"]
}


class AssessmentReranker:

    

    def score_result(self, parsed_query, result):

        score = 0

        skills = parsed_query.get("skills", [])
        job_levels = parsed_query.get("job_levels", [])
        adaptive = parsed_query.get("adaptive", False)
        remote = parsed_query.get("remote", False)
        duration_pref = parsed_query.get("duration")

        record = result

        # -------------------------
        # Skill Matching
        # -------------------------

        for skill in record.get("skills", []):

            if skill.lower() in skills:
                score += 10

        # -------------------------
        # Job Level Matching
        # -------------------------

        target_levels = []

        for level in job_levels:
         target_levels.extend(JOB_LEVELS.get(level, []))

         if target_levels:

            for level in record.get("job_levels", []):

                if level in target_levels:
                    score += 4

        # -------------------------
        # Adaptive Preference
        # -------------------------

        if adaptive:

            if record.get("adaptive") == "yes":
                score += 3

        # -------------------------
        # Remote Preference
        # -------------------------

        if remote:

            if record.get("remote") == "yes":
                score += 3

        # -------------------------
        # Duration Constraints
        # -------------------------

        duration = record.get("duration", "")

        match = re.search(r"(\d+)", duration)

        if match:

            minutes = int(match.group(1))

            if duration_pref == "short" and minutes <= 15:
                score += 3

            if duration_pref == "quick" and minutes <= 10:
                score += 3

        return score

    def rerank(self, parsed_query, results):

        rescored = []

        for result in results:

            business_score = self.score_result(
                parsed_query,
                result
            )

            final_score = result["score"] + business_score

            result["business_score"] = business_score
            result["final_score"] = final_score

            rescored.append(result)

        rescored.sort(
            key=lambda x: x["final_score"],
            reverse=True
        )

        return rescored