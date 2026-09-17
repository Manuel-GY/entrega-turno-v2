import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

pdf_path = r'C:\Users\ac17157\Desktop\Plan_Envio_Automatico_Teams.pdf'
doc = SimpleDocTemplate(pdf_path, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=36)
styles = getSampleStyleSheet()

navy = colors.HexColor('#0B1D45')
gold = colors.HexColor('#FBBD00')
slate = colors.HexColor('#334155')
light_gray = colors.HexColor('#F8FAFC')
border_gray = colors.HexColor('#CBD5E1')

title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=17, textColor=navy, spaceAfter=4)
subtitle_style = ParagraphStyle('SubTitleStyle', parent=styles['Normal'], fontName='Helvetica', fontSize=10.5, textColor=slate, spaceAfter=10)
h2_style = ParagraphStyle('H2Style', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=12, textColor=navy, spaceBefore=8, spaceAfter=5)
body_style = ParagraphStyle('BodyStyle', parent=styles['Normal'], fontName='Helvetica', fontSize=9.5, textColor=colors.HexColor('#1E293B'), leading=14)
bold_body = ParagraphStyle('BoldBody', parent=body_style, fontName='Helvetica-Bold')
code_style = ParagraphStyle('CodeStyle', parent=styles['Normal'], fontName='Courier', fontSize=8.5, textColor=navy, leading=12)

story = []

# Title & Header
story.append(Paragraph('GOODYEAR CHILE • SISTEMA ASRS', ParagraphStyle('GY', fontName='Helvetica-Bold', fontSize=9, textColor=gold, spaceAfter=2)))
story.append(Paragraph('Plan de Implementacion: Envio Automatico a Microsoft Teams', title_style))
story.append(Paragraph('Servicio desatendido de captura PNG y despacho condicionado a <b>Ticket Requerido > 0</b>', subtitle_style))
story.append(HRFlowable(width='100%', thickness=2, color=gold, spaceAfter=12))

# 1. Reglas y Horarios
story.append(Paragraph('1. Horarios de Ejecucion y Condicion de Envio', h2_style))
story.append(Paragraph('El reporte se generara y enviara automaticamente <b>15 minutos antes de la finalizacion del turno</b>, siempre y cuando exista programacion de produccion activa en la planta (Ticket Requerido > 0).', body_style))
story.append(Spacer(1, 8))

# Table Horarios
th_style = ParagraphStyle('THStyle', parent=bold_body, textColor=colors.white)
table_data = [
    [Paragraph('<b>Turno</b>', th_style), Paragraph('<b>Rango Horario</b>', th_style), Paragraph('<b>Hora de Disparo</b>', th_style), Paragraph('<b>Condicion Requerida</b>', th_style), Paragraph('<b>Formato</b>', th_style)],
    [Paragraph('Turno 1 (Noche)', body_style), Paragraph('22:00 a 06:00', body_style), Paragraph('<b>06:45</b>', bold_body), Paragraph('Ticket Requerido > 0', body_style), Paragraph('Imagen PNG Ultra HD', body_style)],
    [Paragraph('Turno 2 (Manana)', body_style), Paragraph('06:00 a 14:00', body_style), Paragraph('<b>14:45</b>', bold_body), Paragraph('Ticket Requerido > 0', body_style), Paragraph('Imagen PNG Ultra HD', body_style)],
    [Paragraph('Turno 3 (Tarde)', body_style), Paragraph('14:00 a 22:00', body_style), Paragraph('<b>22:45</b>', bold_body), Paragraph('Ticket Requerido > 0', body_style), Paragraph('Imagen PNG Ultra HD', body_style)]
]
t = Table(table_data, colWidths=[90, 85, 95, 130, 130])
t.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), navy),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('GRID', (0, 0), (-1, -1), 0.5, border_gray),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, light_gray]),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
]))
story.append(t)
story.append(Spacer(1, 10))

# 2. Origen del Dato del Ticket
story.append(Paragraph('2. Origen del Dato: Ticket Requerido de Produccion', h2_style))
story.append(Paragraph('El estado de programacion de la planta se valida consultando el endpoint oficial del sistema ASRS:<br/>• <b>Endpoint:</b> http://10.107.194.110:8006/api/daily-ticket<br/>• <b>Valor actual de ejemplo:</b> 13,500 tires (total: 13500)<br/>• <b>Criterio de Despacho:</b><br/>&nbsp;&nbsp;&nbsp;&nbsp;- Si <b>total > 0</b> (ej. 13,500 tires): Se ejecuta la captura y se despacha a Teams.<br/>&nbsp;&nbsp;&nbsp;&nbsp;- Si <b>total == 0</b> (dias sin produccion, paro general): El envio se omite en silencio sin generar alertas innecesarias.', body_style))
story.append(Spacer(1, 10))

# 3. Flujo Tecnico
story.append(Paragraph('3. Componentes y Arquitectura Tecnica', h2_style))
story.append(Paragraph('<b>A. Captura Headless (Playwright Chromium):</b> En segundo plano, un proceso sin interfaz abre la URL <code>http://127.0.0.1:8050/?turno=...</code> y toma una instantanea en alta resolucion del elemento <code>#report-card</code>.<br/><b>B. Integracion con Teams (Webhook):</b> Despacha el archivo de imagen mediante una solicitud HTTP POST al Webhook oficial del canal de Teams.<br/><b>C. Planificador en Segundo Plano (Scheduler Daemon):</b> Hilo continuo que supervisa el reloj minuto a minuto y ejecuta en los 3 horarios exactos.', body_style))
story.append(Spacer(1, 10))

# 4. Configuracion Segura
story.append(Paragraph('4. Configuracion en Servidor (.env)', h2_style))
box_data = [[Paragraph('<b>Archivo de configuracion local protegido:</b><br/><code>TEAMS_WEBHOOK_URL=https://goodyear.webhook.office.com/...<br/>AUTO_SEND_ENABLED=true<br/>TICKET_API_URL=http://10.107.194.110:8006/api/daily-ticket<br/>T1_TIME=06:45<br/>T2_TIME=14:45<br/>T3_TIME=22:45</code>', code_style)]]
t_box = Table(box_data, colWidths=[530])
t_box.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, -1), light_gray),
    ('BOX', (0, 0), (-1, -1), 1, border_gray),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('LEFTPADDING', (0, 0), (-1, -1), 10),
    ('RIGHTPADDING', (0, 0), (-1, -1), 10),
]))
story.append(t_box)

doc.build(story)
print('PDF generado exitosamente en:', pdf_path)
