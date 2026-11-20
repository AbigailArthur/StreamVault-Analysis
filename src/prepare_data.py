
import json
import pandas as pd

from config import RAW_DIR, PROCESSED_DIR

def prepare_data():

    # Load raw API responses
    with open(RAW_DIR / "movie_details.json", encoding="utf-8") as file:
        movie_data = json.load(file)

    with open(RAW_DIR / "movie_credits.json", encoding="utf-8") as file:
        credits_data = json.load(file)

    # Transform movie details
    movies = pd.json_normalize(
        list(movie_data.values()),
        sep="_"
    )

    # Convert nested lists into readable text
    list_columns = [
        "genres",
        "production_companies",
        "production_countries"
    ]

    for column in list_columns:
        if column in movies.columns:
            movies[column] = movies[column].map(
                lambda items: "; ".join(
                    item.get("name", "")
                    for item in items
                ) if isinstance(items, list) else ""
            )

    # Select useful movie columns
    movie_columns = [
        "id", "title", "original_title", "release_date",
        "runtime", "genres", "budget", "revenue",
        "popularity", "vote_average", "vote_count",
        "original_language", "overview", "status",
        "belongs_to_collection_id",
        "belongs_to_collection_name",
        "production_companies", "production_countries"
    ]

    movies = movies.reindex(columns=movie_columns)

    # Transform cast and crew information
    credit_rows = []

    for movie_id, credit in credits_data.items():

        for person in credit.get("cast", []):
            credit_rows.append({
                "tmdb_id": movie_id,
                "credit_type": "cast",
                "person_id": person.get("id"),
                "person_name": person.get("name"),
                "character": person.get("character"),
                "job": None,
                "department": person.get("known_for_department"),
                "cast_order": person.get("order")
            })

        for person in credit.get("crew", []):
            credit_rows.append({
                "tmdb_id": movie_id,
                "credit_type": "crew",
                "person_id": person.get("id"),
                "person_name": person.get("name"),
                "character": None,
                "job": person.get("job"),
                "department": person.get("department"),
                "cast_order": None
            })

    credits = pd.DataFrame(credit_rows)

    # Save transformed datasets
    movies.to_csv(
        PROCESSED_DIR / "movies.csv",
        index=False
    )

    credits.to_csv(
        PROCESSED_DIR / "credits.csv",
        index=False
    )

    print("\nDATA TRANSFORMATION SUMMARY")
    print("---------------------------")
    print("Movies:", len(movies))
    print("Credit records:", len(credits))
    print("Unique movies in details:", movies["id"].nunique())
    print("Unique movies in credits:", credits["tmdb_id"].nunique())
    print("\nFiles saved successfully.")


if __name__ == "__main__":
    prepare_data()
