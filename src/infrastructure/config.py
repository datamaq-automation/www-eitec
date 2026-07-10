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
        # Chatwoot API Integration
        self.CHATWOOT_API_TOKEN: str = os.getenv("CHATWOOT_API_TOKEN", "")
        
        # Feature flags (activar/desactivar por variable de entorno, por defecto False)
        self.ENABLE_PDF_GENERATOR: bool = os.getenv("ENABLE_PDF_GENERATOR", "false").lower() in ("true", "1", "yes")
        self.ENABLE_BLOG: bool = os.getenv("ENABLE_BLOG", "false").lower() in ("true", "1", "yes")

settings = Settings()

