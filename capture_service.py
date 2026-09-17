import os
import time
from playwright.sync_api import sync_playwright

def capturar_reporte_png(fecha=None, turno=None, output_path=None, port=8050):
    """
    Carga el reporte en headless Chromium y toma la captura exacta de #report-card
    idéntica a la del botón de la aplicación web.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Device scale factor 2 para máxima nitidez
        context = browser.new_context(
            viewport={"width": 1400, "height": 900},
            device_scale_factor=2.0
        )
        page = context.new_page()
        
        url = f"http://127.0.0.1:{port}/"
        params = []
        if fecha:
            params.append(f"fecha={fecha}")
        if turno:
            params.append(f"turno={turno}")
        if params:
            url += "?" + "&".join(params)
            
        print(f"Cargando reporte en: {url} ...")
        page.goto(url, wait_until="networkidle", timeout=20000)
        
        # Esperar que #report-card sea visible
        page.wait_for_selector("#report-card", state="visible")
        
        # Esperar que los datos se hayan cargado y procesado
        try:
            page.wait_for_function("() => window.reportRendered === true", timeout=15000)
        except Exception:
            pass

        # Asegurar remoción de cualquier notificación emergente (toast) en pantalla
        page.evaluate("""() => {
            const toast = document.getElementById('toast');
            if (toast) toast.remove();
            document.querySelectorAll('.toast, .notification, #toast').forEach(el => el.remove());
        }""")
        
        # Pausa de estabilidad para fuentes, estilos e imágenes
        time.sleep(1.5)
        
        card_locator = page.locator("#report-card")
        
        if output_path:
            card_locator.screenshot(path=output_path)
            print(f"Captura guardada en: {output_path}")
            img_bytes = None
        else:
            img_bytes = card_locator.screenshot()
            
        browser.close()
        return img_bytes

if __name__ == "__main__":
    test_file = r"C:\Users\ac17157\Desktop\test_captura_teams.png"
    capturar_reporte_png(output_path=test_file)
    print("Prueba completada. Archivo generado en Escritorio.")
