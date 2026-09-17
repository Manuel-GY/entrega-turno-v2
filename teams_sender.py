import os
import base64
import logging
import requests
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # Fallback simple .env reader
    env_file = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_file):
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())

log = logging.getLogger("teams_sender")

TEAMS_WEBHOOK_URL = os.getenv("TEAMS_WEBHOOK_URL", "")

def enviar_imagen_a_teams(img_bytes, titulo="Entrega de Turno - ASRS", webhook_url=None):
    """
    Envía la imagen PNG de la entrega de turno a un canal de Microsoft Teams
    mediante una Adaptive Card con la imagen incrustada en Base64.
    """
    url = webhook_url or TEAMS_WEBHOOK_URL
    if not url:
        log.warning("No se ha configurado TEAMS_WEBHOOK_URL en el archivo .env o variables de entorno.")
        return False, "TEAMS_WEBHOOK_URL no configurada"

    try:
        b64_img = base64.b64encode(img_bytes).decode("utf-8")
        data_uri = f"data:image/png;base64,{b64_img}"

        # Adaptive Card para Microsoft Teams
        payload = {
            "type": "message",
            "attachments": [
                {
                    "contentType": "application/vnd.microsoft.card.adaptive",
                    "content": {
                        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                        "type": "AdaptiveCard",
                        "version": "1.4",
                        "body": [
                            {
                                "type": "TextBlock",
                                "text": f"📋 **{titulo}**",
                                "weight": "Bolder",
                                "size": "Medium",
                                "color": "Dark"
                            },
                            {
                                "type": "Image",
                                "url": data_uri,
                                "altText": "Reporte Consolidado Entrega de Turno ASRS",
                                "size": "Auto"
                            }
                        ]
                    }
                }
            ]
        }

        resp = requests.post(url, json=payload, timeout=20)
        if resp.status_code in [200, 201, 202]:
            log.info("Reporte enviado exitosamente a Microsoft Teams.")
            return True, "Enviado exitosamente a Teams"
        else:
            log.error(f"Error al enviar a Teams. Código HTTP: {resp.status_code} - {resp.text}")
            return False, f"Error HTTP {resp.status_code}: {resp.text}"

    except Exception as e:
        log.error(f"Excepción al enviar reporte a Teams: {e}")
        return False, str(e)
