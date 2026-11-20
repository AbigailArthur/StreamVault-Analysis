
import time

from src.fetch_tmdb import run_acquisition
from src.prepare_data import prepare_data
from src.validate_data import validate_data
from src.analysis_pipeline import analysis_pipeline
from src.comparison_pipeline import run_comparison
from src.candidate_analysis_pipeline import run_pipeline as run_candidate_analysis
from src.talent_analysis_pipeline import run_pipeline as run_talent_analysis
from src.final_ranking_pipeline import run_pipeline as run_final_ranking


def main():
    start_time = time.perf_counter()

    print("\n========== STREAMVAULT ANALYSIS ==========")

    print("\nSTEP 1: DATA ACQUISITION")
    run_acquisition()

    print("\nSTEP 2: DATA PREPARATION")
    prepare_data()

    print("\nSTEP 3: DATA VALIDATION")
    validate_data()

    print("\nSTEP 4: FEATURE ENGINEERING")
    analysis_pipeline()

    print("\nSTEP 5: FRANCHISE VS STANDALONE COMPARISON")
    run_comparison()

    print("\nSTEP 6: CANDIDATE ANALYSIS")
    run_candidate_analysis()

    print("\nSTEP 7: TALENT ANALYSIS")
    run_talent_analysis()

    print("\nSTEP 8: FINAL RANKING")
    run_final_ranking()

    elapsed_time = time.perf_counter() - start_time

    print("\n========== PIPELINE COMPLETED ==========")
    print(f"Total execution time: {elapsed_time:.2f} seconds")
    print("Analysis outputs are saved in the outputs/ folder.")


if __name__ == "__main__":
    main()
