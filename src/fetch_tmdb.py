

import json
import time
import requests
import pandas as pd

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from config import (
    TOKEN,
    BASE_URL,
    DATA_FILE,
    RAW_DIR,
    PROCESSED_DIR,
    QUARANTINE_DIR,
    API_DELAY_SECONDS
)


def create_session():
    retry = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )

    session = requests.Session()
    session.mount("https://", HTTPAdapter(max_retries=retry))
    session.headers.update({
        "Authorization": f"Bearer {TOKEN}",
        "accept": "application/json"
    })
    return session


def fetch_data(session, endpoint):
    response = session.get(
        f"{BASE_URL}/{endpoint}",
        timeout=30
    )
    response.raise_for_status()
    return response.json()


def run_acquisition():
    if not TOKEN:
        raise ValueError("TMDB_ACCESS_TOKEN is missing from .env")

    for folder in [RAW_DIR, PROCESSED_DIR, QUARANTINE_DIR]:
        folder.mkdir(parents=True, exist_ok=True)

    # Read original candidate list
    df = pd.read_csv(DATA_FILE, dtype=str)

    audit = pd.DataFrame({
        "source_row": range(2, len(df) + 2),
        "tmdb_id": df["tmdb_id"]
    })

    audit["normalized_tmdb_id"] = (
        audit["tmdb_id"].str.strip()
    )

    valid = audit["normalized_tmdb_id"].str.fullmatch(
        r"[1-9]\d*", na=False
    )

    duplicate = (
        valid
        & audit["normalized_tmdb_id"].duplicated(keep="first")
    )

    audit["record_status"] = "invalid_id"
    audit.loc[audit["tmdb_id"].isna() |
              audit["normalized_tmdb_id"].eq(""), "record_status"] = "missing_id"
    audit.loc[valid & ~duplicate, "record_status"] = "pending_fetch"
    audit.loc[duplicate, "record_status"] = "duplicate_id"

    audit["canonical_tmdb_id"] = audit["normalized_tmdb_id"]

    session = create_session()

    movie_data = {}
    credits_data = {}

    unique_ids = audit.loc[
        audit["record_status"] == "pending_fetch",
        "normalized_tmdb_id"
    ]

    for movie_id in unique_ids:
        details_ok = False
        credits_ok = False

        try:
            movie_data[movie_id] = fetch_data(
                session, f"movie/{movie_id}"
            )
            details_ok = True
        except requests.RequestException as error:
            print(f"Movie {movie_id} details failed: {error}")

        time.sleep(API_DELAY_SECONDS)

        try:
            credits_data[movie_id] = fetch_data(
                session, f"movie/{movie_id}/credits"
            )
            credits_ok = True
        except requests.RequestException as error:
            print(f"Movie {movie_id} credits failed: {error}")

        status = (
            "success" if details_ok and credits_ok
            else "details_failed" if not details_ok and credits_ok
            else "credits_failed" if details_ok and not credits_ok
            else "both_failed"
        )

        audit.loc[
            (audit["normalized_tmdb_id"] == movie_id) & (~duplicate),
            "record_status"
        ] = status

    # Save original API responses
    for filename, data in [
        ("movie_details.json", movie_data),
        ("movie_credits.json", credits_data)
    ]:
        with open(RAW_DIR / filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

    # Save complete audit and quarantine records
    audit.to_csv(PROCESSED_DIR / "id_audit.csv", index=False)

    quarantine = audit[
        audit["record_status"] != "success"
    ]
    quarantine.to_csv(
        QUARANTINE_DIR / "quarantined_records.csv",
        index=False
    )

    print("\nDATA ACQUISITION SUMMARY")
    print("-----------------------")
    print("Input rows:", len(audit))
    print("Unique valid IDs:", valid.sum() - duplicate.sum())
    print("Successful fetches:", (audit["record_status"] == "success").sum())
    print("Quarantined records:", len(quarantine))
    print("Movie details retrieved:", len(movie_data))
    print("Credits retrieved:", len(credits_data))
    print("\nAcquisition completed.")


if __name__ == "__main__":
    run_acquisition()
