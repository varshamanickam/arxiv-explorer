import json
import os

# path to dataset. Relative to repo root so make sure to run this file from the repo root
DATA_PATH = os.path.join("data", "raw", "arxiv-metadata-oai-snapshot.json")

# to load first 10000 records from the arxiv dataset 
#uses streaming to avoid crashing by loading everythign at once
def load_sample(n=10000):
    data = []

    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(
            f"Dataset not found at {DATA_PATH}. Please download the data from https://www.kaggle.com/datasets/Cornell-University/arxiv?resource=download and place it under data/raw/"
        )
    
    with open(DATA_PATH, "r") as f:
        for i, line in enumerate(f):
            if i >= n:
                break
            try:
                data.append(json.loads(line))
            except json.JSONDecodeError:
                continue #so it just skips any malformed rows
    
    return data

def main():
    print("Loading the sample subset from the ArXiv kaggle dataset\n")
    data = load_sample()
    print(f"Number of rows loaded: {len(data)}")

    if len(data) == 0:
        print("No data loaded. Check dataset file again")
        return
    
    #printing the columns
    print("\nColumns:")
    print(list(data[0].keys()))

    #print sample categories just to get a feel for what the data looks liek
    print("\nSample categories:")
    for i in range(5):
        print(data[i].get("categories", "N/A"))#so if there are no cat tags for a row, it won't break and will just show N/A in that case


if __name__ == "__main__":
    main()