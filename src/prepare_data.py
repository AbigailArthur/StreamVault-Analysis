
import json
import re

import pandas as pd

from config import RAW_DIR, PROCESSED_DIR


# Expected columns in the final processed movie dataset.
MOVIE_COLUMNS = [
    "id",
    "title",
    "original_title",
    "overview",
    "release_date",
    "budget",
    "revenue",
    "runtime",
    "vote_average",
    "vote_count",
    "popularity",
    "original_language",
    "status",
    "belongs_to_collection_id",
    "belongs_to_collection_name",
    "genres",
    "production_companies",
    "production_countries",
    "spoken_languages",
    "adult",
    "video",
    "tagline",
    "homepage",
    "poster_path",
    "backdrop_path",
]

# Fields expected in the raw TMDb movie response.
RAW_MOVIE_REQUIRED_COLUMNS = {
    "id",
    "title",
    "original_title",
    "overview",
    "release_date",
    "budget",
    "revenue",
    "runtime",
    "vote_average",
    "vote_count",
    "popularity",
    "original_language",
    "status",
    "belongs_to_collection",
    "genres",
    "production_companies",
    "production_countries",
    "spoken_languages",
    "adult",
    "video",
    "tagline",
    "homepage",
    "poster_path",
    "backdrop_path",
}


def normalize_movie_id(value):
    """Validate and normalize TMDb movie IDs."""

    if pd.isna(value):
        raise ValueError("Movie ID cannot be empty.")

    value = str(value).strip()

    if re.fullmatch(r"\d+\.0+", value):
        value = value.split(".")[0]

    if not re.fullmatch(r"\d+", value):
        raise ValueError(f"Invalid movie ID: {value!r}")

    movie_id = int(value)

    if movie_id <= 0:
        raise ValueError(
            f"Movie ID must be positive: {movie_id}"
        )

    return str(movie_id)


def load_json_records(file_path):
    """
    Load JSON records.

    Supports both:
    1. A list of records.
    2. A dictionary with movie IDs as keys and records as values.
    """

    if not file_path.exists():
        raise FileNotFoundError(
            f"Required raw data file not found: {file_path}"
        )

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    if isinstance(data, list):
        records = data

    elif isinstance(data, dict):
        records = []

        for key, value in data.items():
            if not isinstance(value, dict):
                raise TypeError(
                    f"Invalid record for key {key!r} in {file_path.name}."
                )

            record = value.copy()

            # Use the dictionary key if the record has no ID.
            if record.get("id") is None:
                record["id"] = key

            records.append(record)

    else:
        raise TypeError(
            f"{file_path.name} must contain a list or dictionary."
        )

    if not records:
        raise ValueError(
            f"{file_path.name} contains no records."
        )

    return records


def validate_schema(data, required_columns, dataset_name):
    """Check required columns and report unexpected columns."""

    missing_columns = required_columns - set(data.columns)

    if missing_columns:
        raise ValueError(
            f"{dataset_name} schema contract failed. "
            f"Missing columns: {sorted(missing_columns)}"
        )

    unexpected_columns = set(data.columns) - required_columns

    if unexpected_columns:
        print(
            f"WARNING: Unexpected {dataset_name} fields: "
            f"{sorted(unexpected_columns)}"
        )

    return unexpected_columns


def prepare_movies():
    """Prepare raw TMDb movie details into movies.csv."""

    raw_file = RAW_DIR / "movie_details.json"
    output_file = PROCESSED_DIR / "movies.csv"

    raw_movies = load_json_records(raw_file)
    movies = pd.DataFrame(raw_movies)

    # Validate the raw API response.
    unexpected_columns = validate_schema(
        movies,
        RAW_MOVIE_REQUIRED_COLUMNS,
        "TMDb movie"
    )

    # Normalize movie IDs.
    movies["id"] = movies["id"].apply(normalize_movie_id)

    if movies["id"].duplicated().any():
        raise ValueError(
            "Movie data contains duplicate movie IDs."
        )

    # Validate titles.
    invalid_titles = (
        movies["title"].isna()
        | movies["title"].astype(str).str.strip().eq("")
    )

    if invalid_titles.any():
        raise ValueError(
            f"Found {int(invalid_titles.sum())} movies "
            "without valid titles."
        )

    # Extract franchise collection information.
    collection_data = movies["belongs_to_collection"].apply(
        lambda value: value if isinstance(value, dict) else {}
    )

    movies["belongs_to_collection_id"] = (
        collection_data.apply(lambda value: value.get("id"))
    )

    movies["belongs_to_collection_name"] = (
        collection_data.apply(lambda value: value.get("name"))
    )

    # Convert nested fields into JSON strings for CSV storage.
    list_columns = [
        "genres",
        "production_companies",
        "production_countries",
        "spoken_languages",
    ]

    for column in list_columns:
        movies[column] = movies[column].apply(
            lambda value: json.dumps(
                value,
                ensure_ascii=False
            )
            if isinstance(value, (list, dict))
            else value
        )

    # Remove the original nested collection object.
    movies = movies.drop(
        columns=["belongs_to_collection"]
    )

    # Enforce the final output schema.
    missing_output_columns = (
        set(MOVIE_COLUMNS) - set(movies.columns)
    )

    if missing_output_columns:
        raise ValueError(
            "Processed movie schema contract failed. "
            f"Missing columns: {sorted(missing_output_columns)}"
        )

    # Select only the expected output columns after validation.
    movies = movies.loc[:, MOVIE_COLUMNS].copy()

    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    movies.to_csv(output_file, index=False)

    print("\nMOVIE DATA PREPARATION")
    print("----------------------")
    print(f"Movie records prepared: {len(movies)}")
    print(f"Output columns: {len(movies.columns)}")
    print(f"Unexpected API fields: {len(unexpected_columns)}")
    print(f"Saved: {output_file}")

    return movies


def prepare_credits():
    """Prepare raw TMDb credits into credits.csv."""

    raw_file = RAW_DIR / "movie_credits.json"
    output_file = PROCESSED_DIR / "credits.csv"

    raw_credits = load_json_records(raw_file)
    credits = pd.DataFrame(raw_credits)

    required_columns = {
        "id",
        "cast",
        "crew",
    }

    unexpected_columns = validate_schema(
        credits,
        required_columns,
        "TMDb credits"
    )

    # Normalize credit movie IDs.
    credits["id"] = credits["id"].apply(
        normalize_movie_id
    )

    if credits["id"].duplicated().any():
        raise ValueError(
            "Credits data contains duplicate movie IDs."
        )

    credit_rows = []

    for _, movie in credits.iterrows():
        movie_id = movie["id"]

        cast_members = movie["cast"]
        crew_members = movie["crew"]

        if not isinstance(cast_members, list):
            raise ValueError(
                f"Invalid cast data for movie ID {movie_id}."
            )

        if not isinstance(crew_members, list):
            raise ValueError(
                f"Invalid crew data for movie ID {movie_id}."
            )

        # Process cast members.
        for person in cast_members:
            if not isinstance(person, dict):
                continue

            credit_rows.append({
                "movie_id": movie_id,
                "person_id": person.get("id"),
                "name": person.get("name"),
                "job": "Cast",
                "character": person.get("character"),
                "department": "Acting",
                "order": person.get("order"),
            })

        # Process crew members.
        for person in crew_members:
            if not isinstance(person, dict):
                continue

            credit_rows.append({
                "movie_id": movie_id,
                "person_id": person.get("id"),
                "name": person.get("name"),
                "job": person.get("job"),
                "character": None,
                "department": person.get("department"),
                "order": None,
            })

    prepared_credits = pd.DataFrame(
        credit_rows,
        columns=[
            "movie_id",
            "person_id",
            "name",
            "job",
            "character",
            "department",
            "order",
        ]
    )

    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    prepared_credits.to_csv(
        output_file,
        index=False
    )

    print("\nCREDIT DATA PREPARATION")
    print("----------------------")
    print(f"Credit records prepared: {len(prepared_credits)}")
    print(f"Unexpected API fields: {len(unexpected_columns)}")
    print(f"Saved: {output_file}")

    return prepared_credits


def prepare_data():
    """Run all data preparation steps."""

    movies = prepare_movies()
    credits = prepare_credits()

    print("\nData preparation completed successfully.")

    return movies, credits


if __name__ == "__main__":
    prepare_data()
