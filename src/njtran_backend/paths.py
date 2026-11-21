"""Central place for filesystem paths, so moving a module doesn't move its data."""
from pathlib import Path

# src/njtran_backend/paths.py -> project root is two levels above the package
PACKAGE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = PACKAGE_DIR.parents[1]

CONFIG_PATH = PROJECT_ROOT / "config.json"

DATA_DIR = PROJECT_ROOT / "data"
GTFS_DATA_DIR = DATA_DIR / "GTFS_data"
GTFS_ARCHIVE_DIR = DATA_DIR / "GTFS_data_archive"
TOKENS_PATH = DATA_DIR / "GTFS-tokens.json"
