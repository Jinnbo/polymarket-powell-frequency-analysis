import os
import re
from datetime import datetime

from dotenv import load_dotenv
from supabase import Client, create_client

from frequency_analysis import analysis

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SERVICE_KEY = os.getenv("SERVICE_KEY")

supabase: Client = create_client(SUPABASE_URL, SERVICE_KEY)


def upload_to_supabase(meeting_map):
    for date_str, word_counts in meeting_map.items():
        formatted_date = datetime.strptime(date_str, "%Y%m%d").date().isoformat()
        total_words = sum(word_counts.values())
        meeting_data = {"meeting_date": formatted_date, "total_words": total_words}

        meeting_res = (
            supabase.table("fomc_meetings")
            .upsert(meeting_data, on_conflict="meeting_date")
            .execute()
        )

        meeting_id = meeting_res.data[0]["id"]

        metrics_batch = []
        for word, freq in word_counts.items():
            metrics_batch.append(
                {"meeting_id": meeting_id, "word": word, "frequency": freq}
            )

        supabase.table("word_metrics").upsert(
            metrics_batch, on_conflict="meeting_id, word"
        ).execute()


if __name__ == "__main__":
    meeting_results = analysis()
    upload_to_supabase(meeting_results)
