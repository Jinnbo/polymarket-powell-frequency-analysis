import json

FILE_PATH = "data/powell_counts.json"

word_totals = {}
word_date_counts = {}

with open(FILE_PATH, "r") as f:
    data = json.load(f)

total_dates = len(data)

for date, word_counts in data.items():
    for word, count in word_counts.items():
        word_totals[word] = word_totals.get(word, 0) + count

average_word_counts = {}
for word in word_totals:
    total_count = word_totals[word]
    avg_count = total_count / total_dates
    average_word_counts[word] = {"total_count": total_count, "avg_count": avg_count}

OUTPUT_PATH = "data/powell-avg_counts.json"
with open(OUTPUT_PATH, "w") as f:
    json.dump(average_word_counts, f, indent=2)
