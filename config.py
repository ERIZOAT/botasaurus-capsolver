# src/config.py
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from project root
ROOT_DIR = Path(__file__).parent.parent
load_dotenv(ROOT_DIR / ".env")

class Config:
    """Configuration class for CapSolver integration."""

    # CapSolver API Key
    CAPSOLVER_API_KEY: str = os.getenv("CAPSOLVER_API_KEY", "")

    # CapSolver API endpoints
    CAPSOLVER_API_URL = "https://api.capsolver.com"
    CREATE_TASK_ENDPOINT = f"{CAPSOLVER_API_URL}/createTask"
    GET_RESULT_ENDPOINT = f"{CAPSOLVER_API_URL}/getTaskResult"

    @classmethod
    def validate(cls) -> bool:
        """Check if the configuration is valid."""
        if not cls.CAPSOLVER_API_KEY:
            print("Error: CAPSOLVER_API_KEY not set! Please check your .env file.")
            return False
        return True
