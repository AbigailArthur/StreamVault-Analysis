
import numpy as np
import pandas as pd

from config import PROCESSED_DIR


def convert_numeric_with_report(data, column):
    """
    Convert a column to numeric and report values that
    could not be converted.
    """

    original_values = data[column].copy()

    converted_values = pd.to_numeric(
        original_values,
        errors="coerce"
    )

    # Count invalid values, excluding values that were already missing.
    coerced_count = int(
        (original_values.notna() & converted_values.isna()).sum()
    )

    original_missing_count = int(original_values.isna().sum())

    print(f"\n{column.upper()} DATA QUALITY")
    print("---------------------------")
    print(f"Invalid values converted to NaN: {coerced_count}")
    print(f"Values already missing: {original_missing_count}")

    data[column] = converted_values

    return data


def analysis_pipeline():

    input_file = PROCESSED_DIR / "movies.csv"
    output_file = PROCESSED_DIR / "analysis_movies.csv"

    # Load processed movie data.
    if not input_file.exists():
        raise FileNotFoundError(
            f"Movie data file not found: {input_file}"
        )

    movies = pd.read_csv(input_file)

    # Enforce the required input schema.
    required_columns = {
        "id",
        "title",
        "release_date",
        "budget",
        "revenue",
        "belongs_to_collection_id",
    }

    missing_columns = required_columns - set(movies.columns)

    if missing_columns:
        raise ValueError(
            "Analysis schema contract failed. "
            f"Missing columns: {sorted(missing_columns)}"
        )

    print("\nDATA QUALITY AND FEATURE ENGINEERING")
    print("====================================")

    # Convert release dates.
    movies["release_date"] = pd.to_datetime(
        movies["release_date"],
        errors="coerce"
    )

    invalid_dates = int(
        movies["release_date"].isna().sum()
    )

    print(f"Missing or invalid release dates: {invalid_dates}")

    # Convert financial columns and report invalid values.
    movies = convert_numeric_with_report(
        movies,
        "budget"
    )

    movies = convert_numeric_with_report(
        movies,
        "revenue"
    )

    # Reject negative financial values.
    negative_budget = int(movies["budget"].lt(0).sum())
    negative_revenue = int(movies["revenue"].lt(0).sum())

    if negative_budget or negative_revenue:
        raise ValueError(
            "Financial data contract failed. "
            f"Negative budgets: {negative_budget}; "
            f"negative revenues: {negative_revenue}."
        )

    # Create analytical features.
    movies["release_year"] = movies["release_date"].dt.year

    has_collection = (
        movies["belongs_to_collection_id"].notna()
        & movies["belongs_to_collection_id"]
        .astype(str)
        .str.strip()
        .ne("")
    )

    movies["candidate_type"] = np.where(
        has_collection,
        "Franchise",
        "Standalone"
    )

    # Calculate gross minus budget.
    movies["gross_minus_budget"] = (
        movies["revenue"] - movies["budget"]
    )

    # Calculate revenue-to-budget only for positive budgets.
    movies["revenue_to_budget"] = (
        movies["revenue"]
        / movies["budget"].where(movies["budget"] > 0)
    )

    # Save analytical dataset.
    movies.to_csv(
        output_file,
        index=False
    )

    # Report results.
    print("\nFEATURE ENGINEERING SUMMARY")
    print("---------------------------")

    print("Total movies:", len(movies))

    print(
        "Franchise movies:",
        (movies["candidate_type"] == "Franchise").sum()
    )

    print(
        "Standalone movies:",
        (movies["candidate_type"] == "Standalone").sum()
    )

    print(
        "Unique TMDb collections:",
        movies.loc[
            has_collection,
            "belongs_to_collection_id"
        ].nunique()
    )

    print("\nRELEASE PERIODS")
    print("----------------")

    print("All years:", len(movies))

    print(
        "2000 onward:",
        (movies["release_year"] >= 2000).sum()
    )

    print("\nNEW FEATURES CREATED")
    print("--------------------")
    print("release_year")
    print("candidate_type")
    print("gross_minus_budget")
    print("revenue_to_budget")

    print(f"\nSaved: {output_file}")
    print("\nAnalysis pipeline completed successfully.")

    return movies


if __name__ == "__main__":
    analysis_pipeline()
