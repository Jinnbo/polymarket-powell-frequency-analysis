import json
import os
import pickle
import re
from collections import Counter, OrderedDict

import pymupdf

FILE_PATH = "transcripts/"
DATA_FOLDER = "data"


def save_as_pkl(meeting_map):
    filepath = os.path.join(DATA_FOLDER, "powell_counts.pkl")
    with open(filepath, "wb") as f:
        pickle.dump(meeting_map, f)
    print(f"Saved to {filepath}")


def save_as_json(meeting_map):
    sorted_dates = sorted(meeting_map.keys())
    final_output = OrderedDict()

    for date in sorted_dates:
        counter = meeting_map[date]
        sorted_words = OrderedDict(counter.most_common())
        final_output[date] = sorted_words

    filepath = os.path.join(DATA_FOLDER, "powell_counts.json")
    with open(filepath, "w") as f:
        json.dump(final_output, f, indent=4)
    print(f"Saved to {filepath}")


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
    meeting_map = {}

    for filename in files:
        try:
            date_match = re.search(r"\d{8}", filename)
            date_key = date_match.group()
            speech = get_powell_text(filename)
            words = re.findall(r"\b\w+\b", speech.lower())
            meeting_map[date_key] = Counter(words)
            print(f"Processed {filename}")
        except Exception as e:
            print(f"Error processing {filename}: {e}")

    return meeting_map


if __name__ == "__main__":
    counts = analysis()
    save_as_pkl(counts)
    save_as_json(counts)
