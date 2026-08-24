import csv
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def create_leads_pdf(input_csv="verified_leads.csv", output_pdf="my_software_leads.pdf"):
    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=letter,
        rightMargin=20,
        leftMargin=20,
        topMargin=20,
        bottomMargin=20
    )
    
    elements = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=16,
        leading=20,
        textColor=colors.HexColor('#1a365d'),
        spaceAfter=10
    )
    
    elements.append(Paragraph("<b>Freight Audit Systems — Verified Lead Database</b>", title_style))
    elements.append(Spacer(1, 10))
    
    table_data = [["#", "Executive Name", "Title", "Company", "Verified Email", "City"]]
    
    try:
        with open(input_csv, mode='r', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            for idx, row in enumerate(reader, 1):
                table_data.append([
                    str(idx),
                    row.get('name', ''),
                    row.get('title', ''),
                    row.get('company', ''),
                    row.get('email', ''),
                    row.get('city', '')
                ])
    except FileNotFoundError:
        print(f"Error: {input_csv} not found. Run verify_leads.py first.")
        return

    col_widths = [25, 100, 120, 130, 140, 55]
    
    table = Table(table_data, colWidths=col_widths, repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2b6cb0')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('TOPPADDING', (0, 0), (-1, 0), 6),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 7.5),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 4),
        ('TOPPADDING', (0, 1), (-1, -1), 4),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')])
    ]))
    
    elements.append(table)
    doc.build(elements)
    print(f"\n[+] PDF generated directly from local software: {output_pdf}\n")

if __name__ == "__main__":
    create_leads_pdf()
