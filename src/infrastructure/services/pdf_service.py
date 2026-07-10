from datetime import datetime
from fpdf import FPDF

def create_pdf_bytes(nombre: str, email: str, telefono: str, mensaje: str, productos: list[str]) -> bytes:
    pdf = FPDF()
    pdf.add_page()
    
    # 1. Header decoration (top bar)
    pdf.set_fill_color(0, 42, 95)
    pdf.rect(0, 0, 210, 8, "F")
    
    # Brand
    pdf.set_font("helvetica", "B", 22)
    pdf.set_text_color(0, 42, 95)
    pdf.text(14, 25, "EITEC")
    
    pdf.set_font("helvetica", "", 10)
    pdf.set_text_color(100, 116, 139)
    pdf.text(14, 30, "Cooperativa de Trabajo ex EITAR")
    
    # Title & Metadata
    pdf.set_font("helvetica", "B", 12)
    pdf.set_text_color(0, 42, 95)
    pdf.text(120, 22, "SOLICITUD DE COTIZACIÓN B2B")
    
    pdf.set_font("helvetica", "", 9)
    pdf.set_text_color(51, 65, 85)
    today_str = datetime.now().strftime("%d/%m/%Y")
    pdf.text(120, 27, f"Fecha: {today_str}")
    pdf.text(120, 32, f"Código: EITEC-{datetime.now().strftime('%H%M%S')}")
    
    # Divider line
    pdf.set_draw_color(226, 232, 240)
    pdf.line(14, 38, 196, 38)
    
    # 2. Applicant Section
    pdf.set_font("helvetica", "B", 11)
    pdf.set_text_color(0, 42, 95)
    pdf.text(14, 46, "DATOS DEL SOLICITANTE")
    
    pdf.set_font("helvetica", "", 9.5)
    pdf.set_text_color(51, 65, 85)
    pdf.text(14, 52, f"Nombre/Razón Social: {nombre}")
    pdf.text(14, 57, f"Email de contacto: {email or 'No provisto'}")
    pdf.text(14, 62, f"Teléfono de contacto: {telefono or 'No provisto'}")
    
    # 3. Table of products
    pdf.set_y(70)
    
    # Table header
    pdf.set_font("helvetica", "B", 9.5)
    pdf.set_fill_color(0, 42, 95)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(15, 8, "Item", border=1, fill=True)
    pdf.cell(90, 8, "Categoría / Producto", border=1, fill=True)
    pdf.cell(35, 8, "Línea / Origen", border=1, fill=True)
    pdf.cell(42, 8, "Precio Unitario", border=1, fill=True)
    pdf.ln()
    
    # Table body
    pdf.set_font("helvetica", "", 9)
    pdf.set_text_color(51, 65, 85)
    for idx, prod in enumerate(productos, 1):
        pdf.cell(15, 8, str(idx), border=1)
        short_prod = prod[:45] + "..." if len(prod) > 48 else prod
        pdf.cell(90, 8, short_prod, border=1)
        pdf.cell(35, 8, "Original EITAR", border=1)
        pdf.cell(42, 8, "Pendiente de cotización", border=1)
        pdf.ln()
        
    # 4. Notes Section
    if mensaje:
        pdf.ln(5)
        pdf.set_font("helvetica", "B", 11)
        pdf.set_text_color(0, 42, 95)
        pdf.cell(182, 8, "NOTAS O INSTRUCCIONES ADICIONALES")
        pdf.ln(8)
        
        pdf.set_font("helvetica", "", 9.5)
        pdf.set_text_color(51, 65, 85)
        pdf.multi_cell(182, 5, mensaje)
        
    # 5. Footer & Legal disclaimer
    page_height = 297
    box_y = page_height - 35
    pdf.set_fill_color(248, 250, 252)
    pdf.set_draw_color(203, 213, 225)
    pdf.rect(14, box_y, 182, 16, "FD")
    
    # Disclaimer Text
    pdf.set_font("helvetica", "B", 8)
    pdf.set_text_color(0, 42, 95)
    pdf.text(17, box_y + 5, "IMPORTANTE:")
    pdf.set_font("helvetica", "", 8)
    pdf.text(39, box_y + 5, "Este documento representa una solicitud formal de presupuesto mayorista.")
    pdf.text(17, box_y + 11, "Los precios finales y condiciones comerciales de venta serán confirmados por la administración de la cooperativa.")
    
    # EITEC contact line
    pdf.set_font("helvetica", "", 8)
    pdf.set_text_color(100, 116, 139)
    pdf.text(14, page_height - 12, "EITEC Cooperativa - Bernal Oeste, Quilmes - Email: horacio@eitec.coop.ar - Tel: +54 11 4270-7341")
    
    return bytes(pdf.output())
