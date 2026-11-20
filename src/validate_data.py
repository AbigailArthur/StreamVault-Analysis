
import pandas as pd

from config import PROCESSED_DIR

def validate_data():

    movies = pd.read_csv(PROCESSED_DIR / "movies.csv")

    print("\nFINANCIAL DATA QUALITY")
    print("----------------------")
    print("Missing budgets:", movies["budget"].isna().sum())
    print("Missing revenues:", movies["revenue"].isna().sum())
    print("Negative budgets:", (movies["budget"] < 0).sum())
    print("Negative revenues:", (movies["revenue"] < 0).sum())

    print("\nMOVIE ATTRIBUTES")
    print("----------------")
    print("Missing runtime:", movies["runtime"].isna().sum())
    print("Zero runtime:", (movies["runtime"] == 0).sum())

    movies["release_date"] = pd.to_datetime(
        movies["release_date"], errors="coerce"
    )

    print("Invalid release dates:", movies["release_date"].isna().sum())

    movies["release_year"] = movies["release_date"].dt.year

    print("\nRELEASE YEAR COVERAGE")
    print("---------------------")
    print("Earliest year:", movies["release_year"].min())
    print("Latest year:", movies["release_year"].max())
    print("Movies from 2000 onward:",
          (movies["release_year"] >= 2000).sum())

    print("\nCOLLECTION COVERAGE")
    print("-------------------")
    print("Collection movies:",
          movies["belongs_to_collection_id"].notna().sum())
    print("Standalone candidates:",
          movies["belongs_to_collection_id"].isna().sum())

    print("\nVALIDATION COMPLETED")


if __name__ == "__main__":
    validate_data()
