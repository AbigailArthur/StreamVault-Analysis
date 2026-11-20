
import time
import pandas as pd

from config import OUTPUT_DIR, WEIGHTS

def rank_candidates(period):

    candidate_file = (
        "candidate_metrics_all_years.csv"
        if period == "All years"
        else "candidate_metrics_2000_onward.csv"
    )

    talent_file = (
        "talent_metrics_all_years.csv"
        if period == "All years"
        else "talent_metrics_2000_onward.csv"
    )

    candidates = pd.read_csv(OUTPUT_DIR / candidate_file)
    talent = pd.read_csv(OUTPUT_DIR / talent_file)

    # Combine financial and talent results
    data = candidates.merge(
        talent.drop(columns=["period"], errors="ignore"),
        on=["candidate_name", "candidate_type"],
        how="left",
        validate="one_to_one"
    )

    # Handle missing talent counts
    count_columns = [
        "leading_cast_count",
        "director_count",
        "producer_count"
    ]

    data[count_columns] = data[count_columns].fillna(0)

    # Normalize talent indicators by represented film count
    data["cast_per_film"] = (
        data["leading_cast_count"] / data["movie_count"]
    )

    data["directors_per_film"] = (
        data["director_count"] / data["movie_count"]
    )

    # Remove infinite or missing values before ranking
    metrics = {
        "median_film_return": "return_score",
        "median_rating": "rating_score",
        "median_popularity": "popularity_score",
        "cast_per_film": "cast_score",
        "directors_per_film": "director_score"
    }

    for column in metrics:
        data[column] = pd.to_numeric(
            data[column], errors="coerce"
        ).replace([float("inf"), float("-inf")], float("nan"))

    # Rank each indicator within its candidate category
    for source, score in metrics.items():
        data[score] = (
            data.groupby("candidate_type")[source]
            .rank(pct=True, method="average")
            .fillna(0)
        )

    # Calculate transparent weighted score
    data["weighted_score"] = sum(
        data[score] * weight
        for score, weight in WEIGHTS.items()
    )

    # Require at least two represented films for a bundle shortlist
    data["shortlist_eligible"] = (
        (data["candidate_type"] == "Standalone")
        | (
            (data["candidate_type"] == "Franchise")
            & (data["movie_count"] >= 2)
        )
    )

    data["period"]=period

    data = data.sort_values(
        ["candidate_type", "shortlist_eligible", "weighted_score"],
        ascending=[True, False, False]
    )

    return data


def run_pipeline():

    start = time.perf_counter()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    all_years = rank_candidates("All years")
    recent = rank_candidates("2000 onward")

    all_years.to_csv(
        OUTPUT_DIR / "candidate_rankings_all_years.csv",
        index=False
    )

    recent.to_csv(
        OUTPUT_DIR / "candidate_rankings_2000_onward.csv",
        index=False
    )

    # Produce separate shortlists for both time windows
    for period, data in [
        ("all_years", all_years),
        ("2000_onward", recent)
    ]:

        eligible = data[data["shortlist_eligible"]]

        franchises = (
            eligible[eligible["candidate_type"] == "Franchise"]
            .nlargest(3, "weighted_score")
        )

        standalones = (
            eligible[eligible["candidate_type"] == "Standalone"]
            .nlargest(5, "weighted_score")
        )

        shortlist = pd.concat(
            [franchises, standalones],
            ignore_index=True
        )

        shortlist.to_csv(
            OUTPUT_DIR / f"shortlist_{period}.csv",
            index=False
        )

    elapsed = time.perf_counter() - start

    print("\nFINAL RANKING COMPLETED")
    print("-----------------------")
    print("All-years candidates:", len(all_years))
    print("2000-onward candidates:", len(recent))
    print("All-years shortlist: 3 franchises + 5 standalones")
    print("2000-onward shortlist: 3 franchises + 5 standalones")
    print("Execution time:", round(elapsed, 4), "seconds")
    print("Ranking files saved in outputs/")


if __name__ == "__main__":
    run_pipeline()
