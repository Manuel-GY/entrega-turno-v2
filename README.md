# 📊 Entrega de Turno ASRS v2

Aplicación web y generador visual para la **Entrega Consolidada de Turnos del ASRS (Automated Storage and Retrieval System)** en Goodyear Chile.

Integra en una única tarjeta visual de alta resolución los datos operativos del **Dashboard ASRS** y los registros de fallas/intervenciones de **Inspecciones y Órdenes Correctivas**. Diseñado específicamente para exportar imágenes listas para enviar por **Microsoft Teams** o correo.

---

## 🚀 Características

1. **Flujo de Producción (Input / Output):**
   - Construido vs. Vulcanizado (tires).
   - Entrada al ASRS (unidades y tasa por minuto `Rate in`).
   - Eficiencia de Entrada respecto a producción con semáforo de cumplimiento.
   - Total Salida ASRS con desglose de despacho **Manual** vs **Automático**.

2. **Crane Performance & Convección:**
   - % de Disponibilidad Global de los 11 Pasillos ASRS.
   - Top 3 pasillos con mayor tiempo de parada (Downtime en minutos y porcentaje).
   - Métricas de parada de Conveyor principal y frecuencia de eventos.

3. **Press Delivery Performance:**
   - Cumplimiento global del sistema de entrega a prensas.
   - Detalle por grupo de prensas (`400B`, `500A`, `500B`, `600A`, `600B`):
     * Neumáticos despachados por robots.
     * Neumáticos cargados manualmente.
     * Total vulcanizados y % de cumplimiento.

4. **Novedades y Órdenes Correctivas del Turno:**
   - Filtrado automático de órdenes de trabajo por ventana de turno:
     * **Turno T1 (Noche):** 22:00 a 06:00
     * **Turno T2 (Mañana):** 06:00 a 14:00
     * **Turno T3 (Tarde):** 14:00 a 22:00
   - Muestra N° de OT, hora exacta, equipo/máquina, título, tiempo de parada (TP) y clasificador **Breakdown (SÍ/NO)**.

5. **Exportación Inmediata para Equipos:**
   - 📸 **Copiar Imagen para Teams:** Copia directamente la tarjeta en 2x de resolución al portapapeles para pegar con `Ctrl + V` en Teams.
   - 💾 **Descargar PNG:** Guarda la imagen con nombre identificador `Reporte_ASRS_YYYY-MM-DD_T2.png`.
   - 📋 **Copiar Texto Resumen:** Copia el reporte formateado en texto plano para mensajería rápida.

---

## 🛠️ Fuentes de Datos

* **Dashboard ASRS:** `http://10.107.194.110:8006/` (`/api/io-data`, `/api/crane-performance`, `/api/press-delivery`, `/api/conveyor-full`)
* **Inspecciones ASRS:** `http://10.107.194.70/ASRS/inspecciones/` (`index_n1asrs_table.php`, `avisos_correctivos_ASRS_table.php`)

---

## 💻 Instalación y Uso

### 1. Requisitos
* Python 3.9+
* Conexión a la red interna de planta

### 2. Instalación de dependencias
```bash
pip install -r requirements.txt
```

### 3. Ejecutar la aplicación
Doble clic en `iniciar_reporte.bat` o desde la terminal:
```bash
python server.py
```
Abre en tu navegador: [http://localhost:8050](http://localhost:8050)
