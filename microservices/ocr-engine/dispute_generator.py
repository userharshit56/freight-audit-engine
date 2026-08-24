import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_dispute_pdf(
    output_filename: str,
    carrier_name: str,
    invoice_number: str,
    bol_number: str,
    invoiced_amount: float,
    contracted_amount: float,
    variance: float,
    reason: str
):
    doc = SimpleDocTemplate(output_filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Header Title
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#0f172a'),
        spaceAfter=12
    )
    story.append(Paragraph("FORMAL FREIGHT CHARGE DISPUTE NOTICE", title_style))
    story.append(Spacer(1, 12))

    # Context Details
    body_style = styles['Normal']
    story.append(Paragraph(f"<b>Carrier:</b> {carrier_name}", body_style))
    story.append(Paragraph(f"<b>Invoice #:</b> {invoice_number}", body_style))
    story.append(Paragraph(f"<b>BOL Reference #:</b> {bol_number}", body_style))
    story.append(Paragraph(f"<b>Audit Finding:</b> {reason}", body_style))
    story.append(Spacer(1, 16))

    # Discrepancy Breakdown Table
    table_data = [
        ["Line Item / Description", "Invoiced", "Contract Rate", "Disputed Overcharge"],
        ["Freight Base & Fuel Charge", f"${invoiced_amount:.2f}", f"${contracted_amount:.2f}", f"${variance:.2f}"]
    ]

    t = Table(table_data, colWidths=[200, 90, 90, 110])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0284c7')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8fafc')),
    ]))
    story.append(t)
    story.append(Spacer(1, 20))

    # Closing Notice
    story.append(Paragraph("<b>Notice:</b> Payment for the undisputed portion has been processed. Please issue a corrected invoice or credit memo for the disputed variance.", body_style))

    doc.build(story)
    print(f"Successfully generated dispute package: {output_filename}")

if __name__ == "__main__":
    generate_dispute_pdf(
        output_filename="DISPUTE_INV_99823.pdf",
        carrier_name="FedEx Freight",
        invoice_number="INV-99823",
        bol_number="BOL-7712",
        invoiced_amount=1250.00,
        contracted_amount=1000.00,
        variance=250.00,
        reason="Rate sheet variance exceeding contracted fuel & base tariff threshold."
    )
