
import numpy as np
import pandas as pd

from config import PROCESSED_DIR


def analysis_pipeline():

    movies = pd.read_csv(PROCESSED_DIR / "movies.csv")

    # Convert fields to appropriate data types
    movies["release_date"] = pd.to_datetime(
        movies["release_date"], errors="coerce"
    )

    movies["budget"] = pd.to_numeric(
        movies["budget"], errors="coerce"
    )

    movies["revenue"] = pd.to_numeric(
        movies["revenue"], errors="coerce"
    )

    # Create analytical features
    movies["release_year"] = movies["release_date"].dt.year

    has_collection = (
        movies["belongs_to_collection_id"].notna()
        & movies["belongs_to_collection_id"].astype(str).str.strip().ne("")
    )

    movies["candidate_type"] = np.where(
        has_collection, "Franchise", "Standalone"
    )

    movies["gross_minus_budget"] = (
        movies["revenue"] - movies["budget"]
    )

    movies["revenue_to_budget"] = np.where(
        movies["budget"] > 0,
        movies["revenue"] / movies["budget"],
        np.nan
    )

    # Save analytical dataset
    movies.to_csv(
        PROCESSED_DIR / "analysis_movies.csv",
        index=False
    )

    # Report results
    print("\nFEATURE ENGINEERING SUMMARY")
    print("---------------------------")
    print("Total movies:", len(movies))
    print("Franchise movies:", (movies["candidate_type"] == "Franchise").sum())
    print("Standalone movies:", (movies["candidate_type"] == "Standalone").sum())

    print(
        "Unique TMDb collections:",
        movies.loc[has_collection, "belongs_to_collection_id"].nunique()
    )

    print("\nRELEASE PERIODS")
    print("----------------")
    print("All years:", len(movies))
    print("2000 onward:", (movies["release_year"] >= 2000).sum())

    print("\nNew features created:")
    print("release_year")
    print("candidate_type")
    print("gross_minus_budget")
    print("revenue_to_budget")

    print("\nSaved: data/processed/analysis_movies.csv")


if __name__ == "__main__":
    analysis_pipeline()
