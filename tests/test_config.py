import os
from pathlib import Path
from src.infrastructure.config import load_dotenv, Settings

def test_load_dotenv(tmp_path: Path):
    # Create a temporary .env file
    env_file = tmp_path / ".env"
    env_file.write_text("TEST_VAR_CONFIG=env_value\n# Comment\nINVALID_LINE", encoding="utf-8")

    # Ensure it's not currently set
    if "TEST_VAR_CONFIG" in os.environ:
        del os.environ["TEST_VAR_CONFIG"]

    load_dotenv(env_file)
    assert os.environ.get("TEST_VAR_CONFIG") == "env_value"
    
    # Cleanup
    if "TEST_VAR_CONFIG" in os.environ:
        del os.environ["TEST_VAR_CONFIG"]


def test_settings_defaults():
    # Verify that SMTP defaults are sensible
    assert Settings.SMTP_PORT == 587
    assert Settings.SMTP_USE_TLS is True
    assert Settings.RECAPTCHA_SITE_KEY == os.getenv("RECAPTCHA_SITE_KEY", "")
