import os
import time
import logging
from datetime import datetime, timedelta
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
log = logging.getLogger("scheduler_service")

DASHBOARD_BASE = os.getenv("DASHBOARD_BASE", "http://10.107.194.110:8006")
TICKET_API_URL = os.getenv("TICKET_API_URL", f"{DASHBOARD_BASE}/api/daily-ticket")

# Horarios de disparo automático (15 min antes de finalizar el turno)
HORARIOS_DISPARO = {
    "06:45": "T1",  # Turno Noche
    "14:45": "T2",  # Turno Mañana
    "22:45": "T3",  # Turno Tarde
}

def consultar_ticket_programado():
    """
    Consulta el ticket requerido de producción de neumáticos en /api/daily-ticket.
    Retorna (ticket_total, ticket_formatted, success)
    """
    try:
        resp = requests.get(TICKET_API_URL, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            total = data.get("total", 0)
            formatted = data.get("formatted", str(total))
            return int(total) if str(total).isdigit() else 0, formatted, True
    except Exception as e:
        log.error(f"Error al consultar Ticket Requerido en {TICKET_API_URL}: {e}")
    return 0, "0", False

def ejecutar_proceso_envio_turno(turno, fecha=None, port=8050):
    """
    Verifica si el ticket requerido > 0.
    Si es positivo, genera la captura en Playwright y despacha a Teams.
    """
    from capture_service import capturar_reporte_png
    from teams_sender import enviar_imagen_a_teams

    if fecha is None:
        fecha = datetime.now().strftime("%Y-%m-%d")

    log.info(f"=== INICIANDO EVALUACIÓN DE ENVÍO: {turno} ({fecha}) ===")
    
    # 1. Validar condición: Ticket Requerido > 0
    total_ticket, formatted_ticket, ok = consultar_ticket_programado()
    log.info(f"Estado de Producción: Ticket Requerido = {formatted_ticket} tires (total: {total_ticket})")

    if total_ticket <= 0:
        log.info(f"🚫 [ENVÍO OMITIDO] Ticket Requerido en 0 tires. El reporte de {turno} no se despacha.")
        return False, f"Omitido: Ticket Requerido en 0 tires ({formatted_ticket})"

    # 2. Generar imagen del reporte exacto
    log.info(f"📸 Generando captura Ultra HD del reporte para {turno} ({fecha})...")
    try:
        img_bytes = capturar_reporte_png(fecha=fecha, turno=turno, port=port)
        if not img_bytes:
            return False, "Error al generar imagen PNG del reporte"
    except Exception as e:
        log.error(f"Error en captura Playwright: {e}")
        return False, str(e)

    # 3. Enviar a Microsoft Teams
    titulo = f"Entrega de Turno - ASRS | {turno} ({fecha}) • Ticket: {formatted_ticket} tires"
    log.info(f"🚀 Despachando reporte a Microsoft Teams...")
    exito, msg = enviar_imagen_a_teams(img_bytes, titulo=titulo)
    return exito, msg

def iniciar_scheduler_loop(port=8050):
    """
    Bucle continuo en segundo plano que monitorea el reloj.
    """
    log.info("Iniciando Planificador Automático de Entrega de Turno ASRS...")
    log.info(f"Horarios configurados: {HORARIOS_DISPARO}")
    
    ultimo_disparo = None
    
    while True:
        try:
            ahora = datetime.now()
            hora_str = ahora.strftime("%H:%M")
            fecha_str = ahora.strftime("%Y-%m-%d")
            
            if hora_str in HORARIOS_DISPARO and ultimo_disparo != f"{fecha_str}_{hora_str}":
                turno = HORARIOS_DISPARO[hora_str]
                log.info(f"⏰ Disparador horario alcanzado: {hora_str} -> Ejecutando {turno}...")
                ultimo_disparo = f"{fecha_str}_{hora_str}"
                
                # Ejecutar en segundo plano
                exito, msg = ejecutar_proceso_envio_turno(turno, fecha_str, port=port)
                log.info(f"Resultado de envío: {msg}")
                
            time.sleep(30)
        except Exception as e:
            log.error(f"Error en bucle de scheduler: {e}")
            time.sleep(30)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    print("Probando ejecución manual de T2...")
    ejecutar_proceso_envio_turno("T2")
