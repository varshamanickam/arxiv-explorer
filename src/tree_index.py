import json
from pathlib import Path

INPUT_PATH = Path("data/processed/cleaned_arxiv_tree_input.json")


class TreeNode:
    def __init__(self, name):
        self.name = name
        self.children = {}
        self.papers = []


class ArxivTree:
    def __init__(self):
        self.root = TreeNode("root")

    def insert_paper(self, paper):
        for cat in paper["categories"]:
            top = cat["top_level"]
            sub = cat["subtopic"]

            if top not in self.root.children:
                self.root.children[top] = TreeNode(top)

            top_node = self.root.children[top]

            if sub:
                if sub not in top_node.children:
                    top_node.children[sub] = TreeNode(sub)

                top_node.children[sub].papers.append(paper)
            else:
                top_node.papers.append(paper)

    def collect_all_papers_recursive(self, node):
        papers = list(node.papers)

        for child_node in node.children.values():
            papers.extend(self.collect_all_papers_recursive(child_node))

        return papers
    
    def get_top_categories(self):
        return sorted(self.root.children.keys())
    
    def get_subcategories(self, top):
        if top not in self.root.children:
            return []
        return sorted(self.root.children[top].children.keys())


    def search(self, top, sub=None):
        if top not in self.root.children:
            return []
        top_node = self.root.children[top]

        if sub:
            if sub not in top_node.children:
                return []
            return self.root.children[top].children[sub].papers

        return self.collect_all_papers_recursive(top_node)


def load_data():
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def build_tree():
    data = load_data()
    tree = ArxivTree()

    for paper in data:
        tree.insert_paper(paper)

    return tree


def keyword_search(papers, keyword):
    keyword = keyword.lower()
    return [
        p for p in papers
        if keyword in (p["title"] or "").lower()
        or keyword in (p["abstract"] or "").lower()
    ]


if __name__ == "__main__":
    tree = build_tree()

    papers = tree.search("cs", "CL")  # NLP
    results = keyword_search(papers, "transformer") #sample search

    print(f"Found {len(results)} papers")
    if results:
        print(results[0]["title"])