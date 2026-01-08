import json
import os
import re
from collections import OrderedDict, defaultdict

import pymupdf

FILE_PATH = "transcripts/"
DATA_FOLDER = "data"


def get_granular_data(filename):
    doc = pymupdf.open(os.path.join(FILE_PATH, filename))

    all_words_metadata = []
    full_string_parts = []
    current_pos = 0

    for page_num, page in enumerate(doc):
        words = page.get_text("words")
        words.sort(
            key=lambda w: (w[5], w[6], w[7])
        )  # Sort by block, line, then word_no

        for w in words:
            x0, y0, x1, y1, text = w[:5]

            word_len = len(text)
            all_words_metadata.append(
                {
                    "text": text,
                    "start": current_pos,
                    "end": current_pos + word_len,
                    "page": page_num + 1,
                    "bbox": [round(x0, 1), round(y0, 1), round(x1, 1), round(y1, 1)],
                }
            )
            full_string_parts.append(text)
            current_pos += word_len + 1

    full_string = " ".join(full_string_parts)
    doc.close()

    speaker_pattern = r"([A-Z]{2,}(?:\s[A-Z]{2,})*\.)"
    powell_segments = []
    matches = list(re.finditer(speaker_pattern, full_string))

    for i in range(len(matches)):
        speaker_name = matches[i].group().upper()
        if "CHAIR POWELL" in speaker_name:
            start_speech = matches[i].end()
            end_speech = (
                matches[i + 1].start() if i + 1 < len(matches) else len(full_string)
            )
            powell_segments.append((start_speech, end_speech))

    powell_counts = defaultdict(lambda: {"frequency": 0, "occurrences": []})

    for word_meta in all_words_metadata:
        is_powell = any(
            seg[0] <= word_meta["start"] < seg[1] for seg in powell_segments
        )

        if is_powell:
            tokens = re.findall(r"\b\w+\b", word_meta["text"].lower())
            for token in tokens:
                powell_counts[token]["frequency"] += 1
                powell_counts[token]["occurrences"].append(
                    {"p": word_meta["page"], "b": word_meta["bbox"]}
                )

    return OrderedDict(
        sorted(powell_counts.items(), key=lambda x: x[1]["frequency"], reverse=True)
    )


def analysis():
    files = [f for f in os.listdir(FILE_PATH) if f.endswith(".pdf")]
    meeting_map = {}

    for filename in files:
        try:
            date_key = re.search(r"\d{8}", filename).group()
            meeting_map[date_key] = get_granular_data(filename)
            print(f"Processed: {filename}")
        except Exception as e:
            print(f"Error: {filename} -> {e}")

    return meeting_map


def save_output(data):
    with open(os.path.join(DATA_FOLDER, "powell_granular.json"), "w") as f:
        json.dump(data, f)
    print("Saved to data/powell_granular.json")


if __name__ == "__main__":
    results = analysis()
    save_output(results)
