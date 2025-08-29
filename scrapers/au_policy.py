# AU policy scraper placeholder
"""
AU Policy Scraper
-----------------
Fetches AU policy PDFs from predefined URLs and saves to /data/raw/au_policy/.
"""

import os
import requests
from processors.logger import get_logger

RAW_DIR = "data/raw/au_policy"

logger = get_logger("au_policy")

URLS = {
    "AU_Child_Online_Safety_2024": "https://au.int/sites/default/files/documents/43798-doc-African_Union_Child_Online_Safety_and_Empowerment_Policy_Feb_2024.pdf",
    "AU_AI_Strategy_2024": "https://au.int/sites/default/files/documents/44004-doc-EN-_Continental_AI_Strategy_July_2024.pdf",
    "AU_Digital_Compact_2024": "https://au.int/sites/default/files/documents/44005-doc-AU_Digital_Compact_V4.pdf",
    "AU_Digtial_Transformation_Strategy_2020": "https://digitaltransformationcar.org/assets/docs/38507-doc-DTS_for_Africa_2020-2030_English.pdf",
    "AU_Cybersecurity_Data_Protection_Strategy_2014": "https://dataprotection.org.gh/wp-content/uploads/2025/05/Malabo-Convention.pdf",
    "AU_Digital_ID_2022": "https://techpolicyadvisory.com/wp-content/uploads/2025/03/African-Union-AU-Interoperability-Framework-for-Digital-ID.pdf",
    "AU_Data_Policy_2022": "https://youngafricanpolicyresearch.org/wp-content/uploads/2023/07/42078-doc-AU-DATA-POLICY-FRAMEWORK-ENG1.pdf",
    "AU_Digital_Economy_2021": "https://africaportal.org/wp-content/uploads/2023/06/Building-an-Enabling-Environment-for-Inclusive-Digital-Transformation-Africa-R_DQzy95E.pdf",
    "AU_Free_Trade_2012": "https://au.int/sites/default/files/treaties/36437-treaty-consolidated_text_on_cfta_-_en.pdf",
    "AU_AI_Africa_2021": "https://smartafrica.org/wp-content/uploads/2023/11/70029-eng_ai-for-africa-blueprint-min.pdf",
}


def scrape():
    os.makedirs(RAW_DIR, exist_ok=True)
    for name, url in URLS.items():
        filename = os.path.join(RAW_DIR, f"{name}.pdf")
        if os.path.exists(filename):
            logger.info(f"Skipping (already exists): {filename}")
            continue
        try:
            logger.info(f"Downloading {url}")
            resp = requests.get(url, timeout=30)
            resp.raise_for_status()
            with open(filename, "wb") as f:
                f.write(resp.content)
            logger.info(f"Saved → {filename}")
        except Exception as e:
            logger.error(f"Error downloading {url}: {e}")


if __name__ == "__main__":
    scrape()
