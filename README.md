# ArXiv Tree-Based Explorer

## Project Overview
This project moves beyond clean, classroom-style datasets and applies tree-based data structures to real-world, noisy data. Using the ArXiv research paper dataset, we build a hierarchical indexing system that enables efficient navigation and search of research papers by category and metadata.

The system organizes papers into a tree structure based on:
- Primary category (e.g., cs, math, physics)
- Subcategory (e.g., cs.CL, math.CO)
- Metadata (title, authors, abstract, DOI)

This allows users to perform queries such as:
> "Find all papers in Computer Science → NLP → Transformers"

---

## Core Idea
We implement an **N-ary tree (hierarchical tree)** where:

- The root represents the entire dataset
- First-level nodes represent **top-level categories**
- Second-level nodes represent **subtopics**
- Each node stores associated research papers

Since papers can belong to multiple categories, they may appear in multiple branches of the tree.

---

## Features
- Handles real-world noisy data (missing values, formatting issues)
- Preprocessing pipeline for large-scale JSON dataset
- Tree-based indexing for efficient lookup
- Multi-category insertion (one paper → multiple paths)
- Keyword-based search (title + abstract)
- Scalable design (tested on 10,000+ records, extendable to full dataset)

---

## Project Structure
arxiv-explorer/
│
├── data/
│ ├── raw/ # (not included in repo)
│ └── processed/ # cleaned JSON output
│
├── notebooks/
│ └── eda.ipynb # exploratory data analysis
│
├── src/
│ ├── load_data_check.py
│ ├── preprocessing.py
│ └── tree_index.py # main tree implementation
│
├── .gitignore
└── README.md


---

## Data Preprocessing

The dataset contains noisy real-world data including:
- missing values
- inconsistent formatting
- multi-category assignments

### Steps performed:
- Normalize text (remove whitespace, newlines)
- Parse category strings into structured format
- Drop sparse/unnecessary columns
- Handle malformed JSON entries
- Convert dataset into tree-friendly JSON

Output: data/processed/cleaned_arxiv_tree_input.json


---

## Tree Implementation

Each paper is inserted into the tree based on its categories:

Example:
math.CO → Root → math → CO
cs.CG → Root → cs → CG


Flat categories:

hep-ph → Root → hep-ph


### Node Structure:
- category name
- child nodes
- list of associated papers

---

## Search Functionality

### 1. Category Search
Retrieve papers by:
- top-level category
- subcategory

Example:
```python
tree.search("cs", "CL")  # NLP papers
'''
