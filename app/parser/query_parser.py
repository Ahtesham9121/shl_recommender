
class QueryParser:

    def parse(self, query):

        query_lower = query.lower()

        extracted = {

            "role": None,

            "seniority": None,

            "skills": [],

            "adaptive": False,

            "remote": False,

            "duration": None
        }

        # -------------------------
        # Seniority
        # -------------------------

        if "junior" in query_lower:
            extracted["seniority"] = "junior"

        elif "senior" in query_lower:
            extracted["seniority"] = "senior"

        elif "mid" in query_lower:
            extracted["seniority"] = "mid"

        elif "manager" in query_lower:
            extracted["seniority"] = "manager"

        # -------------------------
        # Skills
        # -------------------------

        known_skills = [

            "python",
            "java",
            "react",
            "angular",
            "javascript",
            "sql",
            "django",
            "flask",
            "spring",
            "aws",
            "docker"
        ]

        for skill in known_skills:

            if skill in query_lower:
                extracted["skills"].append(skill)

        # -------------------------
        # Role Detection
        # -------------------------

        known_roles = [

            "backend developer",
            "frontend developer",
            "software engineer",
            "data scientist",
            "python developer",
            "java developer",
            "devops engineer"
        ]

        for role in known_roles:

            if role in query_lower:
                extracted["role"] = role

        # -------------------------
        # Adaptive Preference
        # -------------------------

        if "adaptive" in query_lower:
            extracted["adaptive"] = True

        # -------------------------
        # Remote Preference
        # -------------------------

        if "remote" in query_lower:
            extracted["remote"] = True

        # -------------------------
        # Duration Preference
        # -------------------------

        if "short" in query_lower:
            extracted["duration"] = "short"

        elif "quick" in query_lower:
            extracted["duration"] = "quick"

        return extracted
