
import pandas as pd

from config import PROCESSED_DIR, QUARANTINE_DIR


def validate_data():
    """Enforce data contracts and quarantine invalid movie records."""

    movies_file = PROCESSED_DIR / "movies.csv"
    credits_file = PROCESSED_DIR / "credits.csv"

    required_movie_columns = {
        "id",
        "title",
        "budget",
        "revenue",
        "release_date",
        "vote_average",
        "vote_count",
        "popularity",
    }

    # These match the columns created by prepare_data.py
    required_credit_columns = {
        "movie_id",
        "person_id",
        "name",
        "job",
    }

    if not movies_file.exists():
        raise FileNotFoundError(
            f"Required movie file not found: {movies_file}"
        )

    if not credits_file.exists():
        raise FileNotFoundError(
            f"Required credits file not found: {credits_file}"
        )

    QUARANTINE_DIR.mkdir(parents=True, exist_ok=True)

    movies = pd.read_csv(movies_file)
    credits = pd.read_csv(credits_file)

    print("\nDATA QUALITY VALIDATION")
    print("=" * 40)

    # 1. Enforce movie schema
    missing_movie_columns = (
        required_movie_columns - set(movies.columns)
    )

    if missing_movie_columns:
        raise ValueError(
            "Movie schema contract failed. Missing columns: "
            f"{sorted(missing_movie_columns)}"
        )

    # 2. Enforce credits schema
    missing_credit_columns = (
        required_credit_columns - set(credits.columns)
    )

    if missing_credit_columns:
        raise ValueError(
            "Credit schema contract failed. Missing columns: "
            f"{sorted(missing_credit_columns)}"
        )

    print("Movie schema contract: PASSED")
    print("Credits schema contract: PASSED")

    # 3. Reject duplicate movie IDs
    duplicate_count = int(movies["id"].duplicated().sum())

    if duplicate_count:
        raise ValueError(
            f"Movie data contains {duplicate_count} duplicate IDs."
        )

    # 4. Identify invalid movie records
    invalid_reasons = pd.Series(
        "",
        index=movies.index,
        dtype="object"
    )

    invalid_identity = (
        movies["id"].isna()
        | movies["title"].isna()
        | movies["title"].astype(str).str.strip().eq("")
    )

    invalid_reasons.loc[invalid_identity] = (
        "Missing movie ID or title"
    )

    # 5. Validate numeric fields and report coercions
    numeric_columns = [
        "budget",
        "revenue",
        "vote_average",
        "vote_count",
        "popularity",
    ]

    invalid_numeric = pd.Series(
        False,
        index=movies.index
    )

    for column in numeric_columns:
        original = movies[column]

        converted = pd.to_numeric(
            original,
            errors="coerce"
        )

        # Distinguish genuinely missing values from invalid text
        invalid_values = original.notna() & converted.isna()

        count = int(invalid_values.sum())

        print(
            f"{column}: {count} invalid numeric values "
            "converted to missing"
        )

        invalid_numeric |= invalid_values
        movies[column] = converted

    invalid_reasons.loc[
        invalid_numeric & invalid_reasons.eq("")
    ] = "Invalid numeric value"

    # 6. Reject negative financial values
    negative_financial = (
        movies["budget"].lt(0)
        | movies["revenue"].lt(0)
    )

    negative_count = int(negative_financial.sum())

    print("Negative financial records:", negative_count)

    invalid_reasons.loc[
        negative_financial & invalid_reasons.eq("")
    ] = "Negative budget or revenue"

    # 7. Quarantine invalid records
    invalid_movies = invalid_reasons.ne("")

    quarantine_count = int(invalid_movies.sum())

    if quarantine_count:
        quarantine = movies.loc[invalid_movies].copy()
        quarantine["quarantine_reason"] = invalid_reasons.loc[
            invalid_movies
        ]

        quarantine_file = (
            QUARANTINE_DIR / "quarantined_validation_movies.csv"
        )

        quarantine.to_csv(
            quarantine_file,
            index=False
        )

        print(f"Invalid movie records quarantined: {quarantine_count}")
        print(f"Quarantine file: {quarantine_file}")

        movies = movies.loc[~invalid_movies].copy()

        movies.to_csv(
            movies_file,
            index=False
        )

    else:
        print("Invalid movie records quarantined: 0")

    # 8. Report legitimate missing financial values
    print(
        "Movies with missing budgets:",
        int(movies["budget"].isna().sum())
    )

    print(
        "Movies with missing revenues:",
        int(movies["revenue"].isna().sum())
    )

    # 9. Final validation summary
    print("\nVALIDATION SUMMARY")
    print("-" * 40)
    print("Valid movie records:", len(movies))
    print("Credit records:", len(credits))
    print("Quarantined movie records:", quarantine_count)
    print("Data validation completed successfully.")

    return True


if __name__ == "__main__":
    validate_data()
