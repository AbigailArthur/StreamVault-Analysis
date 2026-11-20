
import time

import pandas as pd

from config import OUTPUT_DIR, PROCESSED_DIR


def evaluate_candidates(movies, period):
    # Calculate financial performance for each film.
    # Only positive budgets are valid for return calculations.
    movies = movies.copy()

    movies["film_revenue_to_budget"] = (
        movies["revenue"] / movies["budget"].where(movies["budget"] > 0)
    )

    # Separate franchise and standalone candidates
    has_collection = (
        movies["belongs_to_collection_id"].notna()
        & movies["belongs_to_collection_id"].astype(str).str.strip().ne("")
    )

    franchise_movies = movies.loc[has_collection].copy()
    standalone_movies = movies.loc[~has_collection].copy()

    # Aggregate franchise performance using per-film metrics
    franchises = (
        franchise_movies
        .groupby(
            ["belongs_to_collection_id", "belongs_to_collection_name"],
            as_index=False
        )
        .agg(
            movie_count=("id", "nunique"),
            median_film_budget=("budget", "median"),
            median_film_revenue=("revenue", "median"),
            median_film_return=("film_revenue_to_budget", "median"),
            median_rating=("vote_average", "median"),
            median_popularity=("popularity", "median"),
            total_revenue=("revenue", "sum"),
            total_budget=("budget", "sum")
        )
        .rename(
            columns={
                "belongs_to_collection_id": "candidate_id",
                "belongs_to_collection_name": "candidate_name"
            }
        )
    )

    franchises["candidate_type"] = "Franchise"

    # Keep standalone films as individual candidates
    standalones = standalone_movies[
        [
            "id",
            "title",
            "budget",
            "revenue",
            "film_revenue_to_budget",
            "vote_average",
            "popularity"
        ]
    ].copy()

    standalones = standalones.rename(
        columns={
            "id": "candidate_id",
            "title": "candidate_name",
            "budget": "median_film_budget",
            "revenue": "median_film_revenue",
            "film_revenue_to_budget": "median_film_return",
            "vote_average": "median_rating",
            "popularity": "median_popularity"
        }
    )

    standalones["movie_count"] = 1
    standalones["total_budget"] = standalones["median_film_budget"]
    standalones["total_revenue"] = standalones["median_film_revenue"]
    standalones["candidate_type"] = "Standalone"

    # Combine franchise and standalone candidates
    candidates = pd.concat(
        [franchises, standalones],
        ignore_index=True
    )

    candidates.insert(0, "period", period)

    return candidates


def run_pipeline():
    start = time.perf_counter()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    movies = pd.read_csv(PROCESSED_DIR / "analysis_movies.csv")

    all_candidates = evaluate_candidates(movies, "All years")

    recent_movies = movies.loc[
        movies["release_year"] >= 2000
    ].copy()

    recent_candidates = evaluate_candidates(
        recent_movies,
        "2000 onward"
    )

    all_candidates.to_csv(
        OUTPUT_DIR / "candidate_metrics_all_years.csv",
        index=False
    )

    recent_candidates.to_csv(
        OUTPUT_DIR / "candidate_metrics_2000_onward.csv",
        index=False
    )

    elapsed = time.perf_counter() - start

    print("\nCANDIDATE EVALUATION SUMMARY")
    print("----------------------------")

    for period, data in [
        ("All years", all_candidates),
        ("2000 onward", recent_candidates)
    ]:
        print(f"\n{period}")
        print(
            "Franchise bundles:",
            (data["candidate_type"] == "Franchise").sum()
        )
        print(
            "Standalone films:",
            (data["candidate_type"] == "Standalone").sum()
        )

    print("\nExecution time:", round(elapsed, 4), "seconds")
    print("\nCandidate evaluation completed.")


if __name__ == "__main__":
    run_pipeline()
