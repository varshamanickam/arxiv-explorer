import json
import re
from pathlib import Path

import pandas as pd

INPUT_PATH = Path("data/raw/arxiv-metadata-oai-snapshot.json")
OUTPUT_PATH = Path("data/processed/cleaned_arxiv_tree_input.json")

def normalize_text(text):
    if pd.isna(text):
        return None
    text = str(text).strip()
    text = re.sub(r"\s+", " ", text)
    return text if text != "" else None

def parse_categories(cat_str):
    if cat_str is None:
        return []

    parsed = []
    for c in cat_str.split():
        if "." in c:
            top, sub = c.split(".", 1)
        else:
            top, sub = c, None

        parsed.append({
            "full_code": c,
            "top_level": top,
            "subtopic": sub
        })
    return parsed

def preprocess_records(record):
    return {
        "id": normalize_text(record.get("id")),
        "title": normalize_text(record.get("title")),
        "abstract": normalize_text(record.get("abstract")),
        "authors": normalize_text(record.get("authors")),
        "doi": normalize_text(record.get("doi")),
        "categories": parse_categories(record.get("categories"))
    }

def main():
    cleaned_records = []
    num_skipped_malformed_json = 0

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        for line in f:
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                num_skipped_malformed_json += 1
                continue

            cleaned_records.append(preprocess_records(record))
    
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(cleaned_records, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(cleaned_records)} cleaned records to {OUTPUT_PATH}")
    print(f"Number of skipped malformed JSON lines: {num_skipped_malformed_json}")


if __name__ == "__main__":
    main()