# needed ui friendly json to build basic radial tree strcuture first.
# didn't want to bloat the json with fields we won't dispaly in the front end anyways so just chose the fields we'll be using for the frontend
import json
from pathlib import Path

from tree_index import build_tree

OUTPUT_PATH = Path("data/processed/frontend_tree_data.json")
MAX_PAPERS_PER_CATEGORY = 200


def simplify_paper(paper):
    return {
        "id": paper.get("id") or paper.get("title"),
        "title": paper.get("title"),
        "abstract": paper.get("abstract"),
        "authors": paper.get("authors"),
        "categories": paper.get("categories"),
    }


def export_frontend_data():
    tree = build_tree()

    top_categories = tree.get_top_categories()
    subcategories = {}
    papers_by_category = {}
    papers_dict = {}

    for top in top_categories:
        sub_list = tree.get_subcategories(top)
        subcategories[top] = sub_list

        top_papers = tree.search(top)[:MAX_PAPERS_PER_CATEGORY]
        ids = []

        for p in top_papers:
            pid = p.get("id") or p.get("title")
            if pid not in papers_dict:
                papers_dict[pid] = simplify_paper(p)
            ids.append(pid)

        papers_by_category[top] = ids

        for sub in sub_list:
            key = f"{top}.{sub}"
            sub_papers = tree.search(top, sub)[:MAX_PAPERS_PER_CATEGORY]

            ids = []
            for p in sub_papers:
                pid = p.get("id") or p.get("title")
                if pid not in papers_dict:
                    papers_dict[pid] = simplify_paper(p)
                ids.append(pid)

            papers_by_category[key] = ids

    frontend_data = {
        "top_categories": top_categories,
        "subcategories": subcategories,
        "papers_by_category": papers_by_category,
        "papers": papers_dict,
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(frontend_data, f)

    print(f"Saved frontend data to {OUTPUT_PATH}")


if __name__ == "__main__":
    export_frontend_data()