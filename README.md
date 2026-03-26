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
- Streaming based validation for a very large raw dataset
- exploratory data analysis on a 10,000 record subset of the data
- targeted preprocessing for noisy metadata
- Tree-based indexing for efficient lookup
- Multi-category insertion (one paper appears in multiple paths)
- Keyword-based search (title + abstract)
- React frontend with radial tree visualization
- Scalable design (tested on 10,000+ records, extendable to full dataset)
- frontend export format optimized for browser performance

---

## Project Structure
```
arxiv-explorer/
│
├── data/
│   ├── raw/                  # original dataset (not included in repo)
│   └── processed/
│       ├── cleaned_arxiv_tree_input.json      # preprocessed JSON output used for the tree
│       └── frontend_tree_data.json            # exported the above json in a format that was more digestible for the front end (dropped fields we weren't displaying,capped results to first 200 papers per category, and used ids instead of whole paper objects)
│
├── notebooks/
│   └── eda.ipynb             # exploratory data analysis (to figure out what the data looked like and what kind of preprocessing we needed to do)
│
├── src/
|   ├── load_data_check.py   # streaming + validation
│   ├── preprocessing.py
│   ├── tree_index.py        # main tree implementation
│   └── export_json_frontend.py
│
├── frontend/                 # React-based UI
│   ├── src/
│   │   ├── components/
│   │   │   ├── RadialTree.jsx
│   │   │   ├── InfoPanel.jsx
│   │   │   └── PaperCard.jsx
│   │   ├── data/
│   │   │   └── frontend_tree_data.json
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── main.jsx
│
├── .gitignore
└── README.md

```

---
## Data Loading and Validation
The ArXiv dataset is extremely large (~1.7M+ records) and stored as a line-delimited JSON file. Loading the entire dataset at once is unnecessary for initial inspection so the project first uses a streaming based validation script `load_data_check.py`

This script:
- reads the dataset line by line
- loads the first 10,000 records by default
- skips malformed JSON rows (no malformed rows so we didn't end up having to skip anything)
- prints the number of loaded rows
- prints column names
- prints sample category strings

This is just to provide a quick sanity check that:
- the right dataset was downloaded and placed in the correct location
- the file format is valid
- the category field looks suitable for hierarchical parsing

## Exploratory Data Analysis
Before writing the full preprocessing pipeline, we used `notebooks/eda.ipynb` on the first 10,000 records to understand the structure and noise in the raw data. We had to do this to know what kind of preprocessing had to be done.

The notebook was used to inspect:
- dataset shape and columns
- null value counts
- category frequency patterns
- whether category strings are space-separated
- whether categories follow dotted hierarchical form like `math.CO`
- whether some categories are flat codes like `hep-ph`
- whether records are missing critical fields
- whether category rows are malformed
- whether duplicate paper IDs are present

Main observations from EDA:
- category strings are space separated
- some categories are hierarchical and some are flat codes
- many papers belong to multiple categories
- critical fields used in this project were generally present in the 10,000 record subset that we inspected
- the dataset didn't really require heavy cleaning but did require normalization and structured category parsing

The EDA notebook `eda.ipynb` also helped us validate our preprocessing logic on a manageable subset before applying it to the full dataset in `preprocessing.py`


## Data Preprocessing
The preprocessing pipeline is implemented in `src/preprocessing.py`

### what it does
For each raw paper record, it:
- normalizes text fields by trimming whitespace and collapsing repeated whitespace
- preserves selected metadata fields:
    - id
    - title
    - abstract
    - authors
    - doi
- parses the category string into structured objects for tree insertion
- skips malformed JSON rows during streaming

### output
The preprocessing step writes:
`data/processed/cleaned_arxiv_tree_input.json`
This clean JSON is the direct input we feed in the tree building stage

---

## Tree Implementation
The tree implementation is in `src/tree_index.py`
Each paper is inserted into the tree based on its categories.

### Example:
```bash
math.CO → Root → math → CO
cs.CG   → Root → cs → CG
```

Flat categories:
```bash
hep-ph → Root → hep-ph
```
### Node Structure:
- Category name  
- Child nodes  
- A list of associated papers  

---

## Insert behavior
For each paper:
- read its parsed category list
- create the top-level node if needed
- create the subtopic node if needed
- attach the paper to the final node for that category path

Because papers can belong to multiple categories, the same paper may appear in multiple branches

## Helper functionality
The tree also provides:
- `get_top_categories()` to list top level categories
- `get_subcategories(top)` to list subtopics under a top level category
- recursive collection of all papers under a selected top level branch so for example if we selected "cs", it shouldn't just list papers that fall right under "cs" and don't have subcategories but all sub papers under "cs"

## Search Functionality

### Category Search
Retrieve papers by:
- Top-level category  
- Subcategory  

Example:
```python
tree.search("cs", "CL")
```

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

## Frontend (Radial Tree Visualization)
React-based frontend provides an interactive radial tree interface:
- Center node represents the dataset (arXiv)
- The first ring shows top level categories
- second layer displays the subcategories if we click a top category
- Clicking nodes updates results in real time

The information panel displays:
- current selected category or subcategory
- number of loaded papers
- keyword search input
- scrollable list of papers

In the paper cards, each paper displays:
- title
- authors
- abstract preview
- category tags

User interactions:
- Clicking a top level node 
    - loads all papers under that category
    - displays its subcategories in the radial view
- Clicking a subcategory
    - filters results to that subcategory
- Typing a keyword
    - filters currently loaded papers using title and abstract

### UI Features
- Radial tree visualization of category hierarchy
- Interactive node selection
- Keyword based filtering
- Paper preview cards with metadata
- space themed (we tried) UI

### Layout
The interface is divided into 2 main sections:
1. Radial Tree Panel (left half)
Displays the category hierarchy as a radial graph
2. Information Panel (right half)
Displays selected category, the search input, and paper results



### Frontend data optimization
The full cleaned dataset is too large to send directly to the browser in repeated full-paper form so a frontend specific export is generated in `src/export_json_frontend.py`

To address this:
- a frontend specific JSON is generated from the built tree in `src/export_json_frontend.py`
- this export also preserves the full discovered category structure
- Papers are:
    - stored once in a dictionary `id -> paper`
    - referenced by id within categories
- We capped number of papers that show up in results per category to 200 so that UI remains responsive

Note: Capping the # of papers at 200 means that sometimes even if a keyword technically exists in the database, searching by keyword might turn up "no results found" if that keyword isn't present in the 200 papers pulled up for that category. However, since the goal of this project was to algorithmically showcase the relationships within arXiv as an n-ary tree and not to make a production ready search engine, we overlook this flaw. 

This also helped us preserve
- The full category structure
- Multi-category relationships
- Efficient frontend performance

## Efficiency

- Tree lookup : near O(1) using dictionary access
- Traversal: O(k) where k = # of relevant papers
- Keyword filtering: O(n) within the selected node

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

### 3. Validate the raw dataset

```bash
python src/load_data_check.py
```

---
### 4. Run preprocessing

```bash
python src/preprocessing.py
```
```bash
This generates: `data/processed/cleaned_arxiv_tree_input.json`
```
---
### 5. Run tree indexing

```bash
python src/tree_index.py
```
This:
- loads the cleaned JSON
- builds the hierarchical category tree
- runs a sample search on cs.CL
- applies a sample keyword filter (transformer)
---

### 6. Export frontend friendly tree data

```bash
python src/export_json_frontend.py
```
This generates: 
```bash 
data/processed/frontend_tree_data.json
```
Then just place or copy over that file into: `frontend/src/data/frontend_tree_data.json`
---
### 7. Run the frontend

```bash
cd frontend
npm install
npm run dev
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

## ACKNOWLEDGEMENT and REFERENCES

The data loading, exploratory analysis, preprocessing pipeline, and tree-based backend implementation were our own logic and implementation. Did not use AI for those sections

AI tools were used to assist with frontend development (React component structure and UI styling). We described our design requirements (space dune early 2k video game themed).

No AI tools were used in the design or implementation of the core data structures or algos.

1) dataset: https://www.kaggle.com/datasets/Cornell-University/arxiv
2) original project inspiration: https://www.youtube.com/watch?v=8G8d-umcvfg
3) graph based research paper exploration: https://www.connectedpapers.com
4) handling large json files in python: https://dev.to/lovestaco/handling-large-json-files-in-python-efficient-read-write-and-update-strategies-3jgg
5) working with json in python: https://realpython.com/python-json/