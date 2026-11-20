
import pandas as pd

from config import PROCESSED_DIR, OUTPUT_DIR


MIN_TALENT_FILMS = 2


def validate_credit_columns(credits):
    """Ensure credits use the expected prepared-data schema."""

    required_columns = {
        "movie_id",
        "person_id",
        "name",
        "job",
        "character",
        "department",
        "order",
    }

    missing = required_columns - set(credits.columns)

    if missing:
        raise ValueError(
            f"Credits schema is missing columns: {sorted(missing)}"
        )


def build_candidate_talent_metrics(movies, credits, period):
    """Retain talent counts and names at candidate level."""

    movies = movies.copy()
    credits = credits.copy()

    validate_credit_columns(credits)

    has_collection = (
        movies["belongs_to_collection_id"].notna()
        & movies["belongs_to_collection_id"].astype(str).str.strip().ne("")
    )

    movies["candidate_id"] = movies["id"].astype(str)
    movies["candidate_name"] = movies["title"]

    movies.loc[has_collection, "candidate_id"] = (
        movies.loc[has_collection, "belongs_to_collection_id"].astype(str)
    )

    movies.loc[has_collection, "candidate_name"] = (
        movies.loc[has_collection, "belongs_to_collection_name"]
    )

    movies["candidate_type"] = "Standalone"
    movies.loc[has_collection, "candidate_type"] = "Franchise"

    credits["movie_id"] = credits["movie_id"].astype(str)
    movies["id"] = movies["id"].astype(str)

    credits = credits.merge(
        movies[["id", "candidate_id", "candidate_name", "candidate_type"]],
        left_on="movie_id",
        right_on="id",
        how="inner"
    )

    credits["order"] = pd.to_numeric(
        credits["order"], errors="coerce"
    )

    # Leading cast members: first five credited actors.
    leading_cast = credits.loc[
        (credits["job"] == "Cast")
        & (credits["order"] < 5)
    ]

    cast_metrics = (
        leading_cast.groupby(
            ["candidate_id", "candidate_name", "candidate_type"]
        )
        .agg(
            leading_cast_count=("person_id", "nunique"),
            leading_cast_names=(
                "name",
                lambda x: ", ".join(sorted(set(x.dropna())))
            )
        )
        .reset_index()
    )

    # Directors.
    directors = credits.loc[
        (credits["job"] == "Director")
        & (credits["department"] == "Directing")
    ]

    director_metrics = (
        directors.groupby(
            ["candidate_id", "candidate_name", "candidate_type"]
        )
        .agg(
            director_count=("person_id", "nunique"),
            director_names=(
                "name",
                lambda x: ", ".join(sorted(set(x.dropna())))
            )
        )
        .reset_index()
    )

    # Preserve the original definition: include all producer roles.
    producers = credits.loc[
        credits["job"].str.contains(
            "Producer", case=False, na=False
        )
    ]

    producer_metrics = (
        producers.groupby(
            ["candidate_id", "candidate_name", "candidate_type"]
        )
        .agg(
            producer_count=("person_id", "nunique"),
            producer_names=(
                "name",
                lambda x: ", ".join(sorted(set(x.dropna())))
            )
        )
        .reset_index()
    )

    candidates = movies[
        ["candidate_id", "candidate_name", "candidate_type"]
    ].drop_duplicates()

    candidates = candidates.merge(
        cast_metrics,
        on=["candidate_id", "candidate_name", "candidate_type"],
        how="left"
    )

    candidates = candidates.merge(
        director_metrics,
        on=["candidate_id", "candidate_name", "candidate_type"],
        how="left"
    )

    candidates = candidates.merge(
        producer_metrics,
        on=["candidate_id", "candidate_name", "candidate_type"],
        how="left"
    )

    count_columns = [
        "leading_cast_count",
        "director_count",
        "producer_count"
    ]

    candidates[count_columns] = (
        candidates[count_columns].fillna(0).astype(int)
    )

    candidates.insert(0, "period", period)

    return candidates


def build_person_talent_metrics(movies, credits, period):
    """Measure individual lead actors' and directors' film track records."""

    movies = movies.copy()
    credits = credits.copy()

    validate_credit_columns(credits)

    movies["id"] = movies["id"].astype(str)
    credits["movie_id"] = credits["movie_id"].astype(str)

    movie_metrics = movies[
        [
            "id",
            "title",
            "revenue_to_budget",
            "vote_average",
            "popularity"
        ]
    ].copy()

    for column in [
        "revenue_to_budget",
        "vote_average",
        "popularity"
    ]:
        movie_metrics[column] = pd.to_numeric(
            movie_metrics[column], errors="coerce"
        )

    joined = credits.merge(
        movie_metrics,
        left_on="movie_id",
        right_on="id",
        how="inner"
    )

    joined["order"] = pd.to_numeric(
        joined["order"], errors="coerce"
    )

    lead_actors = joined.loc[
        (joined["job"] == "Cast")
        & (joined["order"] < 5)
    ].copy()

    directors = joined.loc[
        (joined["job"] == "Director")
        & (joined["department"] == "Directing")
    ].copy()

    def summarize_people(data, talent_type):

        data = data.drop_duplicates(
            subset=["person_id", "movie_id"]
        )

        summary = (
            data.groupby("person_id")
            .agg(
                person_name=("name", "first"),
                film_count=("movie_id", "nunique"),
                median_revenue_to_budget=("revenue_to_budget", "median"),
                share_films_revenue_above_budget=(
                    "revenue_to_budget",
                    lambda x: x.dropna().gt(1).mean()
                ),
                median_vote_average=("vote_average", "median"),
                median_popularity=("popularity", "median"),
                film_titles=(
                    "title",
                    lambda x: "; ".join(sorted(set(x.dropna())))
                )
            )
            .reset_index()
        )

        summary.insert(0, "talent_type", talent_type)
        summary.insert(0, "period", period)

        summary["eligible_for_signal"] = (
            summary["film_count"] >= MIN_TALENT_FILMS
        )

        return summary

    actor_metrics = summarize_people(lead_actors, "Lead actor")
    director_metrics = summarize_people(directors, "Director")

    result = pd.concat(
        [actor_metrics, director_metrics],
        ignore_index=True
    )

    result = result.sort_values(
        [
            "talent_type",
            "eligible_for_signal",
            "median_revenue_to_budget",
            "film_count"
        ],
        ascending=[True, False, False, False],
        na_position="last"
    ).reset_index(drop=True)

    return result


def run_pipeline():

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    movies = pd.read_csv(PROCESSED_DIR / "analysis_movies.csv")
    credits = pd.read_csv(PROCESSED_DIR / "credits.csv")

    validate_credit_columns(credits)

    # All-years analysis
    all_candidate_metrics = build_candidate_talent_metrics(
        movies, credits, "All years"
    )

    all_person_metrics = build_person_talent_metrics(
        movies, credits, "All years"
    )

    # 2000-onward analysis
    recent_movies = movies.loc[movies["release_year"] >= 2000]

    recent_credits = credits[
        credits["movie_id"].astype(str).isin(
            recent_movies["id"].astype(str)
        )
    ]

    recent_candidate_metrics = build_candidate_talent_metrics(
        recent_movies, recent_credits, "2000 onward"
    )

    recent_person_metrics = build_person_talent_metrics(
        recent_movies, recent_credits, "2000 onward"
    )

    # Save candidate-level outputs
    all_candidate_metrics.to_csv(
        OUTPUT_DIR / "talent_metrics_all_years.csv",
        index=False
    )

    recent_candidate_metrics.to_csv(
        OUTPUT_DIR / "talent_metrics_2000_onward.csv",
        index=False
    )

    # Save individual talent track-record outputs
    all_person_metrics.to_csv(
        OUTPUT_DIR / "talent_person_metrics_all_years.csv",
        index=False
    )

    recent_person_metrics.to_csv(
        OUTPUT_DIR / "talent_person_metrics_2000_onward.csv",
        index=False
    )

    print("TALENT ANALYSIS COMPLETED")
    print("All-years candidate records:", len(all_candidate_metrics))
    print("2000-onward candidate records:", len(recent_candidate_metrics))
    print("All-years individual talent records:", len(all_person_metrics))
    print("2000-onward individual talent records:", len(recent_person_metrics))
    print(
        "All-years talent with at least two films:",
        int(all_person_metrics["eligible_for_signal"].sum())
    )
    print(
        "2000-onward talent with at least two films:",
        int(recent_person_metrics["eligible_for_signal"].sum())
    )
    print("Files saved in outputs/")


if __name__ == "__main__":
    run_pipeline()
