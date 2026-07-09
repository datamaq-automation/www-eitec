import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = BASE_DIR / ".env"

def load_dotenv(env_path: Path = ENV_FILE) -> None:
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, val = line.split("=", 1)
                val = val.strip().strip("'\"")
                os.environ.setdefault(key.strip(), val)

# Cargar variables de entorno del .env si existe
load_dotenv()

class Settings:
    SMTP_HOST: str = os.getenv("SMTP_HOST", "localhost")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME: str = os.getenv("SMTP_USERNAME", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    SMTP_USE_TLS: bool = os.getenv("SMTP_USE_TLS", "True").lower() in ("true", "1", "yes")
    
    CONTACT_RECIPIENT_EMAIL: str = os.getenv("CONTACT_RECIPIENT_EMAIL", "")
    CONTACT_SENDER_EMAIL: str = os.getenv("CONTACT_SENDER_EMAIL", "")

    # Google reCAPTCHA v2
    RECAPTCHA_SITE_KEY: str = os.getenv("RECAPTCHA_SITE_KEY", "")
    RECAPTCHA_SECRET_KEY: str = os.getenv("RECAPTCHA_SECRET_KEY", "")

    # Chatwoot API Integration
    CHATWOOT_API_URL: str = os.getenv("CHATWOOT_API_URL", "")
    CHATWOOT_API_TOKEN: str = os.getenv("CHATWOOT_API_TOKEN", "")
    CHATWOOT_ACCOUNT_ID: int = int(os.getenv("CHATWOOT_ACCOUNT_ID", "1"))
    CHATWOOT_INBOX_ID: int = int(os.getenv("CHATWOOT_INBOX_ID", "1"))

settings = Settings()
