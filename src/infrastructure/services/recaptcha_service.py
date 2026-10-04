import requests

from src.infrastructure.config import settings
from src.infrastructure.services.logger import logger


class RecaptchaService:
    VERIFY_URL = "https://www.google.com/recaptcha/api/siteverify"

    @staticmethod
    def verify_token(token: str, ip: str = "") -> bool:
        """Verifica el token de reCAPTCHA v2 con los servidores de Google."""
        if not settings.RECAPTCHA_SECRET_KEY:
            logger.warning("reCAPTCHA secret key no configurada")
            return True

        try:
            response = requests.post(
                RecaptchaService.VERIFY_URL,
                data={
                    "secret": settings.RECAPTCHA_SECRET_KEY,
                    "response": token,
                    "remoteip": ip,
                },
                timeout=5,
            )
            result = response.json()

            if result.get("success"):
                score = result.get("score", 0)
                logger.info(
                    "reCAPTCHA validado exitosamente - Score: %.2f - IP: %s",
                    score,
                    ip,
                )
                return True
            else:
                error_codes = result.get("error-codes", [])
                logger.warning(
                    "reCAPTCHA falló - Errores: %s - IP: %s",
                    error_codes,
                    ip,
                )
                return False
        except requests.RequestException as e:
            logger.error("Error al validar reCAPTCHA: %s", str(e))
            return False
