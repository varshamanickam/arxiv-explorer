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
- Multi-category insertion (one paper appears in multiple paths)
- Keyword-based search (title + abstract)
- Scalable design (tested on 10,000+ records, extendable to full dataset)

---

## Project Structure
```

arxiv-explorer/
│
├── data/
│   ├── raw/              # (not included in repo)
│   └── processed/        # cleaned JSON output
│
├── notebooks/
│   └── eda.ipynb         # exploratory data analysis
│
├── src/
│   ├── load_data_check.py
│   ├── preprocessing.py
│   └── tree_index.py     # main tree implementation
│
├── .gitignore
└── README.md

```

---

## Data Preprocessing
The dataset contains noisy real-world data including:
- Missing values  
- Inconsistent formatting  
- Multi-category assignments  

### Steps performed:
- Normalize text (remove whitespace, newlines)
- Parse category strings into structured format
- Drop sparse/unnecessary columns
- Handle malformed JSON entries
- Convert dataset into tree-friendly JSON

Output:
```

data/processed/cleaned_arxiv_tree_input.json

```

---

## Tree Implementation
Each paper is inserted into the tree based on its categories.

### Example:
```

math.CO → Root → math → CO
cs.CG   → Root → cs → CG

```

Flat categories:
```

hep-ph → Root → hep-ph

````

### Node Structure:
- Category name  
- Child nodes  
- List of associated papers  

---

## 🔍 Search Functionality

### Category Search
Retrieve papers by:
- Top-level category  
- Subcategory  

Example:
```python
tree.search("cs", "CL")
````

---

### Keyword Search

Filter papers by keywords in:

* Title
* Abstract

Example:

```python
keyword_search(papers, "transformer")
```

---

## Efficiency

* Tree lookup: near O(1) using dictionary access
* Traversal: O(k) where k is number of relevant papers
* Keyword filtering: O(n) within selected node

This reduces unnecessary scanning of the full dataset.

---

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/varshamanickam/arxiv-explorer.git
cd arxiv-explorer
```

---

### 2. Download dataset

Download from Kaggle:
[https://www.kaggle.com/datasets/Cornell-University/arxiv](https://www.kaggle.com/datasets/Cornell-University/arxiv)

Place file in:

```
data/raw/arxiv-metadata-oai-snapshot.json
```

---

### 3. Run preprocessing

```bash
python src/preprocessing.py
```

---

### 4. Run tree indexing

```bash
python src/tree_index.py
```

---

## Notes

* Dataset files are not included due to size limitations
* Ensure correct folder structure before running scripts
* Designed to scale beyond sample subset

---

## Future Improvements

* Radial tree visualization (interactive UI)
* Streamlit-based frontend
* Advanced filtering (year, authors)
* Improved search ranking

---

## Key Learning Outcomes

* Handling noisy real-world datasets
* Designing hierarchical data structures
* Efficient indexing and search
* Applying theory to practical systems

---

## NO AI OR EXTERNAL RESOURCES WERE USED IN THIS PROJECT
