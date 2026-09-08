from .pipeline import clean_data
from .pipeline import clean_data
from .analysis import build_report
from .logger import get_logger
from .config import RAW, PROCESSED

log = get_logger(__name__)

def main() -> None:
    log.info("Starting Digital Commerce analytics pipeline")
    clean_data()
    build_report()
    log.info("Pipeline completed successfully")

if __name__ == "__main__":
    main()
