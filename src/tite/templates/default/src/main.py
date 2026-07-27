"""Main entry point for the project."""

import logging
import sys
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/app.log", mode="a", encoding="utf-8"),
    ],
)

logger = logging.getLogger(__name__)


def main() -> int:
    """
    Main function that serves as the entry point for the application.

    Returns:
        int: Exit code (0 for success, non-zero for errors)
    """
    try:
        logger.info("Application started successfully")
        print("Hello from your Tite project!")
        print("Project path:", Path(__file__).parent.parent.absolute())
        print("Python version:", sys.version)
        
        # Add your application logic here
        
        logger.info("Application completed successfully")
        return 0
        
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        return 1
    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())