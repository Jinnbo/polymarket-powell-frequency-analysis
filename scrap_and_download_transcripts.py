import os

import requests
from bs4 import BeautifulSoup

FOLDER = "transcripts"
FOMC_CALENDAR_URL = "https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm"
FOMC_PRES_CONF_BASE_URL = (
    "https://www.federalreserve.gov/mediacenter/files/FOMCpresconf"
)

response = requests.get(FOMC_CALENDAR_URL)
soup = BeautifulSoup(response.text, "html.parser")

links = soup.find_all("a", href=True)
meeting_links = [
    l["href"]
    for l in links
    if "fomcpresconf" in l["href"] and l["href"].endswith(".htm")
]

for link in meeting_links:
    date_str = "".join(filter(str.isdigit, link))
    pdf_url = f"{FOMC_PRES_CONF_BASE_URL}{date_str}.pdf"
    filename = f"FOMCpresconf{date_str}.pdf"
    filepath = os.path.join(FOLDER, filename)
    print(f"Downloading {filepath}")

    pdf_response = requests.get(FOMC_PRES_CONF_BASE_URL + pdf_url)
    if pdf_response.status_code == 200:
        with open(filepath, "wb") as f:
            f.write(pdf_response.content)
    else:
        print(f"Failed to find PDF for date {date_str}")
