from fpdf import FPDF
import os

def generate_pdf(name, cert_type, details):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt=f"{cert_type} Certificate", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Name: {name}", ln=True)
    pdf.multi_cell(200, 10, txt=f"Details: {details}")
    
    if not os.path.exists("certs"):
        os.makedirs("certs")
        
    filename = f"certs/{name.replace(' ', '_')}_{cert_type.lower()}.pdf"
    pdf.output(filename)
    return filename
