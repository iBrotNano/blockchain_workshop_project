import os

from dotenv import load_dotenv
from pathlib import Path


# Language for mnemonic generation, default is English.
MNEMONIC_LANGUAGE = None

# Name of the application
APP_NAME = None

LOCAL_APPDATA_PATH = None

DEPLOYMENT_RECORD_VERSION = None

SERVICE_ADDRESS = None


def configure():
    """
    Configure the application.
    """
    load_dotenv()
    global MNEMONIC_LANGUAGE
    global APP_NAME
    global LOCAL_APPDATA_PATH
    global DEPLOYMENT_RECORD_VERSION
    global SERVICE_ADDRESS
    MNEMONIC_LANGUAGE = os.getenv("MNEMONIC_LANGUAGE", "english")
    APP_NAME = os.getenv("APP_NAME", "Plockchain")
    LOCAL_APPDATA_PATH = Path(os.getenv("LOCALAPPDATA")) / APP_NAME
    LOCAL_APPDATA_PATH.mkdir(parents=True, exist_ok=True)
    # TODO: Test that the deployment record version is loaded correctly and used in the command line tool.
    DEPLOYMENT_RECORD_VERSION = os.getenv("DEPLOYMENT_RECORD_VERSION", "1")
    SERVICE_ADDRESS = os.getenv("SERVICE_ADDRESS", "localhost:5000")
