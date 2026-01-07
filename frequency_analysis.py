import json
import os
import pickle
import re
from collections import Counter, OrderedDict

import pymupdf

FILE_PATH = "transcripts/"
DATA_FOLDER = "data/"


def save_as_pkl(counter_obj):
    filepath = os.path.join(DATA_FOLDER, "powell_counts.pkl")
    with open(filepath, "wb") as f:
        pickle.dump(counter_obj, f)
    print(f"Analysis saved to {filepath}")


def save_as_json(counter_obj):
    sorted_dict = OrderedDict(counter_obj.most_common())
    filepath = os.path.join(DATA_FOLDER, "powell_counts.json")
    with open(filepath, "w") as f:
        json.dump(sorted_dict, f, indent=4)


def get_powell_text(pdf_file):
    full_text = ""
    with pymupdf.open(FILE_PATH + pdf_file) as doc:
        for page in doc:
            full_text += page.get_text("text")

    # Remove Page Headers and Footers
    full_text = re.sub(r"Page \d+ of \d+", "", full_text)
    full_text = re.sub(r"FINAL", "", full_text)
    full_text = re.sub(
        r"(January|February|March|April|May|June|July|August|September|October|November|December)\s\d{1,2},\s\d{4}",
        "",
        full_text,
    )
    full_text = re.sub("Chair Powell’s Press Conference", "", full_text)

    # Split parts by speakers
    speaker_pattern = r"(\n?[A-Z]{2,}(?:\s[A-Z]{2,})*\.)"
    parts = re.split(speaker_pattern, full_text)

    powell_blocks = []
    for i in range(len(parts)):
        if "CHAIR POWELL" in parts[i]:
            powell_blocks.append(parts[i + 1])

    return " ".join(powell_blocks)


def analysis():
    files = [f for f in os.listdir(FILE_PATH) if f.endswith(".pdf")]
    master_counts = Counter()

    for filename in files:
        try:
            speech = get_powell_text(filename)
            words = re.findall(r"\b\w+\b", speech.lower())
            master_counts.update(words)
        except Exception as e:
            print(f"Error processing {filename}: {e}")

    return master_counts


if __name__ == "__main__":
    counts = analysis()
    save_as_pkl(counts)
    save_as_json(counts)
