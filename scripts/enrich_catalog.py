import json
import re
from pathlib import Path

INPUT_PATH = Path("data/cleaned/clean_catalog.json")
OUTPUT_PATH = Path("data/enriched/enriched_catalog.json")


TECH_KEYWORDS = {
    "python": ["python"],
    "java": ["java"],
    "javascript": ["javascript", "js"],
    "typescript": ["typescript"],
    "angular": ["angular"],
    "react": ["react"],
    "aws": ["aws", "amazon web services"],
    "android": ["android"],
    "sql": ["sql"],
    "mvc": ["mvc"],
    "wpf": ["wpf"],
    "wcf": ["wcf"],
    "xaml": ["xaml"],
    "agile": ["agile", "scrum"],
    "testing": ["testing", "qa"],
    "frontend": ["frontend", "ui"],
    "backend": ["backend", "api"],
    "cloud": ["cloud"],
    "security": ["security"],
}


def load_catalog():
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_skills(text):
    text = text.lower()

    found = []

    for skill, keywords in TECH_KEYWORDS.items():
        for keyword in keywords:
            if re.search(rf"\b{re.escape(keyword)}\b", text):
                found.append(skill)
                break

    return sorted(list(set(found)))


def build_search_text(record, skills):
    parts = [
        record.get("name", ""),
        record.get("description", ""),
        " ".join(record.get("job_levels", [])),
        " ".join(record.get("test_types", [])),
        " ".join(skills)
    ]

    return " ".join(parts)


def enrich_record(record):
    combined_text = f"""
    {record.get('name', '')}
    {record.get('description', '')}
    """

    skills = extract_skills(combined_text)

    enriched = record.copy()

    enriched["skills"] = skills

    enriched["search_text"] = build_search_text(record, skills)

    return enriched


def enrich_catalog(data):
    enriched = []

    for record in data:
        enriched.append(enrich_record(record))

    return enriched


def save_catalog(data):
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"Saved enriched catalog to {OUTPUT_PATH}")


if __name__ == "__main__":
    catalog = load_catalog()

    enriched_catalog = enrich_catalog(catalog)

    save_catalog(enriched_catalog)

    print("Enrichment complete.")