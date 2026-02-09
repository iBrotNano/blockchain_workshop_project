from dotenv import load_dotenv
import os

load_dotenv()

# Language for mnemonic generation, default is English.
MNEMONIC_LANGUAGE = os.getenv("MNEMONIC_LANGUAGE", "english")

# Name of the application
APP_NAME = os.getenv("APP_NAME", "Plockchain")
