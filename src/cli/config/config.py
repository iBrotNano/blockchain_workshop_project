import os

from dotenv import load_dotenv
from pathlib import Path


# Language for mnemonic generation, default is English.
MNEMONIC_LANGUAGE = None

# Name of the application
APP_NAME = None

LOCAL_APPDATA_PATH = None


def configure():
    """
    Configure the application.
    """
    load_dotenv()
    global MNEMONIC_LANGUAGE
    global APP_NAME
    global LOCAL_APPDATA_PATH
    MNEMONIC_LANGUAGE = os.getenv("MNEMONIC_LANGUAGE", "english")
    APP_NAME = os.getenv("APP_NAME", "Plockchain")
    LOCAL_APPDATA_PATH = Path(os.getenv("LOCALAPPDATA")) / APP_NAME
    LOCAL_APPDATA_PATH.mkdir(parents=True, exist_ok=True)
