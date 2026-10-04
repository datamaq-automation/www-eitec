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
    def __init__(self) -> None:
        # SMTP Configuration for email notifications
        self.SMTP_HOST: str = os.getenv("SMTP_HOST", "")
        self.SMTP_PORT: int = int(os.getenv("SMTP_PORT", "0"))
        self.SMTP_USER: str = os.getenv("SMTP_USER", "")
        self.SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
        self.SMTP_FROM: str = os.getenv("SMTP_FROM", "noreply@eitec.coop.ar")
        self.SMTP_TLS: bool = os.getenv("SMTP_TLS", "true").lower() in (
            "true",
            "1",
            "yes",
        )

        # reCAPTCHA v2 Configuration
        self.RECAPTCHA_SITE_KEY: str = os.getenv("RECAPTCHA_SITE_KEY", "")
        self.RECAPTCHA_SECRET_KEY: str = os.getenv("RECAPTCHA_SECRET_KEY", "")

        # Feature flags (activar/desactivar por variable de entorno, por defecto False)
        self.ENABLE_PDF_GENERATOR: bool = os.getenv(
            "ENABLE_PDF_GENERATOR", "false"
        ).lower() in ("true", "1", "yes")
        self.ENABLE_BLOG: bool = os.getenv("ENABLE_BLOG", "false").lower() in (
            "true",
            "1",
            "yes",
        )


settings = Settings()
