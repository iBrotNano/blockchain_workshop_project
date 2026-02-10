import dotenv
import config.config as config_module

from tests.helpers import reload_module


def test_mnemonic_language_defaults_to_english(monkeypatch):
    monkeypatch.setattr(dotenv, "load_dotenv", lambda *args, **kwargs: None)
    monkeypatch.delenv("MNEMONIC_LANGUAGE", raising=False)
    reload_module(config_module)
    config_module.configure()
    assert config_module.MNEMONIC_LANGUAGE == "english"


def test_mnemonic_language_respects_env(monkeypatch):
    monkeypatch.setattr(dotenv, "load_dotenv", lambda *args, **kwargs: None)
    monkeypatch.setenv("MNEMONIC_LANGUAGE", "german")
    reload_module(config_module)
    config_module.configure()
    assert config_module.MNEMONIC_LANGUAGE == "german"


def test_app_name_defaults_to_plockchain(monkeypatch):
    monkeypatch.setattr(dotenv, "load_dotenv", lambda *args, **kwargs: None)
    monkeypatch.delenv("APP_NAME", raising=False)
    reload_module(config_module)
    config_module.configure()
    assert config_module.APP_NAME == "Plockchain"


def test_app_name_respects_env(monkeypatch):
    monkeypatch.setattr(dotenv, "load_dotenv", lambda *args, **kwargs: None)
    monkeypatch.setenv("APP_NAME", "MyApp")
    reload_module(config_module)
    config_module.configure()
    assert config_module.APP_NAME == "MyApp"


def test_configure_creates_local_appdata_path():
    config_module.configure()
    assert config_module.LOCAL_APPDATA_PATH.exists()
    assert config_module.LOCAL_APPDATA_PATH.is_dir()
