
import time
import pandas as pd

from config import PROCESSED_DIR, OUTPUT_DIR

def create_comparison_units(movies):

    # Identify franchise and standalone movies
    has_collection = (
        movies["belongs_to_collection_id"].notna()
        & movies["belongs_to_collection_id"].astype(str).str.strip().ne("")
    )

    franchise_movies = movies.loc[has_collection].copy()
    standalone_movies = movies.loc[~has_collection].copy()

    # Aggregate franchise movies into collection-level bundles
    franchises = (
        franchise_movies
        .groupby(
            ["belongs_to_collection_id", "belongs_to_collection_name"],
            as_index=False
        )
        .agg(
            movie_count=("id", "nunique"),
            total_budget=("budget", "sum"),
            total_revenue=("revenue", "sum"),
            gross_minus_budget=("gross_minus_budget", "sum")
        )
        .rename(columns={
            "belongs_to_collection_id": "unit_id",
            "belongs_to_collection_name": "unit_name"
        })
    )

    franchises["candidate_type"] = "Franchise"

    franchises["revenue_to_budget"] = (
        franchises["total_revenue"] / franchises["total_budget"]
    )

    # Keep standalone movies as individual licensing candidates
    standalones = standalone_movies[
        ["id", "title", "budget", "revenue", "gross_minus_budget"]
    ].copy()

    standalones = standalones.rename(columns={
        "id": "unit_id",
        "title": "unit_name",
        "budget": "total_budget",
        "revenue": "total_revenue"
    })

    standalones["movie_count"] = 1
    standalones["candidate_type"] = "Standalone"

    standalones["revenue_to_budget"] = (
        standalones["total_revenue"] / standalones["total_budget"]
    )

    # Combine both licensing candidate types
    units = pd.concat(
        [franchises, standalones],
        ignore_index=True
    )

    return units


def summarize_comparison(units, period):

    summary = (
        units.groupby("candidate_type")
        .agg(
            candidate_units=("unit_id", "nunique"),
            films_represented=("movie_count", "sum"),
            total_budget=("total_budget", "sum"),
            total_revenue=("total_revenue", "sum"),
            median_budget=("total_budget", "median"),
            median_revenue=("total_revenue", "median"),
            median_revenue_to_budget=("revenue_to_budget", "median"),
            median_gross_minus_budget=("gross_minus_budget", "median")
        )
        .reset_index()
    )

    summary.insert(0, "period", period)

    return summary


def run_comparison():

    start_time = time.perf_counter()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    movies = pd.read_csv(PROCESSED_DIR / "analysis_movies.csv")

    movies["release_year"] = pd.to_numeric(
        movies["release_year"], errors="coerce"
    )

    # All-years comparison
    all_units = create_comparison_units(movies)

    # 2000-onward comparison
    recent_movies = movies.loc[
        movies["release_year"] >= 2000
    ].copy()

    recent_units = create_comparison_units(recent_movies)

    # Create comparison summaries
    all_summary = summarize_comparison(
        all_units, "All years"
    )

    recent_summary = summarize_comparison(
        recent_units, "2000 onward"
    )

    comparison = pd.concat(
        [all_summary, recent_summary],
        ignore_index=True
    )

    # Save outputs
    comparison.to_csv(
        OUTPUT_DIR / "comparison_summary.csv",
        index=False
    )

    all_units.to_csv(
        OUTPUT_DIR / "comparison_units_all_years.csv",
        index=False
    )

    recent_units.to_csv(
        OUTPUT_DIR / "comparison_units_2000_onward.csv",
        index=False
    )

    elapsed_time = time.perf_counter() - start_time

    print("\nLICENSING COMPARISON SUMMARY")
    print("----------------------------")
    print(comparison.to_string(index=False))

    print("\nCANDIDATE COUNTS")
    print("----------------")
    print("All-years franchise bundles:",
          len(all_units[all_units["candidate_type"] == "Franchise"]))
    print("All-years standalone films:",
          len(all_units[all_units["candidate_type"] == "Standalone"]))
    print("2000-onward franchise bundles:",
          len(recent_units[recent_units["candidate_type"] == "Franchise"]))
    print("2000-onward standalone films:",
          len(recent_units[recent_units["candidate_type"] == "Standalone"]))

    print("\nExecution time:", round(elapsed_time, 4), "seconds")

    print("\nComparison files saved successfully.")


if __name__ == "__main__":
    run_comparison()
