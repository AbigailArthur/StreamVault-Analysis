
import os
from pathlib import Path
from dotenv import load_dotenv


# ==========================================
# PROJECT ROOT
# ==========================================

ROOT = Path(__file__).resolve().parent

# Load environment variables from the project .env file
load_dotenv(ROOT / ".env")


# ==========================================
# TMDB CONFIGURATION
# ==========================================

TOKEN = os.getenv("TMDB_ACCESS_TOKEN")
BASE_URL = "https://api.themoviedb.org/3"
API_DELAY_SECONDS = 0.25


# ==========================================
# PROJECT DIRECTORIES
# ==========================================

DATA_DIR = ROOT / "data" / "processed"
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = DATA_DIR
QUARANTINE_DIR = ROOT / "data" / "quarantine"
OUTPUT_DIR = ROOT / "outputs"


# ==========================================
# INPUT FILES
# ==========================================

DATA_FILE = ROOT / "id_list.csv"

MOVIE_DETAILS_FILE = RAW_DIR / "movie_details.json"
MOVIE_CREDITS_FILE = RAW_DIR / "movie_credits.json"


# ==========================================
# RANKING CONFIGURATION
# ==========================================

WEIGHTS = {
    "return_score": 0.50,
    "rating_score": 0.25,
    "popularity_score": 0.25,
    "cast_score": 0.00,
    "director_score": 0.00
}
