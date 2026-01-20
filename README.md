# Powell Frequency Analysis

[**View the Dashboard**](https://powell-word-count.vercel.app/)

## Purpose
This project analyzes Jerome Powell's speech patterns during FOMC press conferences to identify correlations between his diction and word frequency with interest rate decisions.

It also helps in making a prediction for the Polymarket event: [What will Powell say during January press conference?](https://polymarket.com/event/what-will-powell-say-during-january-press-conference-639)

## Methodology
1.  **Collection**: Transcripts are downloaded from the [Federal Reserve's FOMC calendar](https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm).
2.  **Processing**: PDFs are parsed to isolate Chair Powell's introductory statements and Q&A responses, excluding other participants.
3.  **Analysis**:
    - Word frequencies are calculated, accounting for pluralizations (e.g., "inflation" + "inflations").
    - Specific target phrases (e.g., "not our job", "stock market", "good afternoon") are tracked.
4.  **Aggregation**: Historical averages are computed to establish baselines.

## Dashboard Preview
<img width="1435" height="809" alt="Dashboard View 1" src="https://github.com/user-attachments/assets/01d04437-b12d-4d23-87e0-d8a2b9b5cf1f" />

<img width="1437" height="809" alt="Dashboard View 2" src="https://github.com/user-attachments/assets/2791a5e4-3c18-4d56-8b12-5a63e6a3b46b" />
