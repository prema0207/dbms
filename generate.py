from reportlab.pdfgen import canvas

def create_pdf(app_data):
    filename = f"static/{app_data['name']}_{app_data['cert_type']}_certificate.pdf"
    c = canvas.Canvas(filename)
    c.drawString(100, 750, f"Certificate Type: {app_data['cert_type']}")
    c.drawString(100, 730, f"Name: {app_data['name']}")
    c.drawString(100, 710, f"Income: {app_data['income']}")
    c.drawString(100, 690, f"Status: Approved")
    c.drawString(100, 670, "This certificate is digitally generated.")
    c.save()
