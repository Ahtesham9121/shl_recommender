import json
from pathlib import Path

RAW_PATH = Path("data/raw/shl_catalog.json")
CLEAN_PATH = Path("data/cleaned/clean_catalog.json")


def load_catalog():
    with open(RAW_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"Loaded {len(data)} assessments")

    return data


def clean_record(record):
    return {
        "id": record.get("entity_id"),
        "name": record.get("name", "").strip(),
        "url": record.get("link", "").strip(),
        "description": record.get("description", "").strip(),
        "job_levels": record.get("job_levels", []),
        "languages": record.get("languages", []),
        "duration": record.get("duration", "").strip(),
        "remote": record.get("remote", "no"),
        "adaptive": record.get("adaptive", "no"),
        "test_types": record.get("keys", [])
    }


def clean_catalog(data):
    cleaned = []

    for record in data:
        cleaned.append(clean_record(record))

    return cleaned


def save_cleaned(data):
    with open(CLEAN_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"Saved cleaned catalog to {CLEAN_PATH}")


if __name__ == "__main__":
    raw_data = load_catalog()

    cleaned_data = clean_catalog(raw_data)

    save_cleaned(cleaned_data)

    print("Catalog cleaning complete.")