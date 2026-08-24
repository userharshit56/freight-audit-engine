import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_test_invoices():
    os.makedirs("test_invoices", exist_ok=True)
    invoices = [
        {"id": "INV-1001", "carrier": "TCI Express", "billed": 45000, "audited": 45000, "overcharge": 0},
        {"id": "INV-1002", "carrier": "V-Trans India", "billed": 62000, "audited": 58000, "overcharge": 4000},
        {"id": "INV-1003", "carrier": "Mahindra Logistics", "billed": 31000, "audited": 31000, "overcharge": 0},
        {"id": "INV-1004", "carrier": "Gati KWE", "billed": 88000, "audited": 81500, "overcharge": 6500},
        {"id": "INV-1005", "carrier": "Delhivery", "billed": 24000, "audited": 24000, "overcharge": 0}
    ]
    
    styles = getSampleStyleSheet()
    pdf_paths = []
    
    for inv in invoices:
        filename = f"test_invoices/{inv['id']}.pdf"
        doc = SimpleDocTemplate(filename, pagesize=letter)
        elements = []
        
        title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=14, leading=18, textColor=colors.HexColor('#1a365d'))
        elements.append(Paragraph(f"<b>CARRIER FREIGHT INVOICE: {inv['id']}</b>", title_style))
        elements.append(Spacer(1, 10))
        
        data = [
            ["Invoice Number:", inv['id']],
            ["Carrier Name:", inv['carrier']],
            ["Billed Amount (INR):", f"Rs. {inv['billed']:,}"],
            ["Contract Base Rate:", f"Rs. {inv['audited']:,}"],
            ["Discrepancy / Overcharge:", f"Rs. {inv['overcharge']:,}"]
        ]
        
        table = Table(data, colWidths=[150, 250])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#f7fafc')),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e0')),
            ('PADDING', (0,0), (-1,-1), 6),
        ]))
        
        elements.append(table)
        doc.build(elements)
        pdf_paths.append(filename)
        
    return pdf_paths

def send_email():
    pdf_paths = generate_test_invoices()
    
    sender_email = os.getenv("SMTP_USER", "your_email@gmail.com")
    sender_password = os.getenv("SMTP_PASS", "your_app_password")
    recipient_email = os.getenv("IMAP_INBOX_USER", "your_test_inbox@gmail.com")
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = "INVOICE_BATCH_TEST_DAY7"
    
    body = "Day 7 Integration Test: 5 carrier invoice attachments included for n8n IMAP ingestion."
    msg.attach(MIMEText(body, 'plain'))
    
    for path in pdf_paths:
        with open(path, "rb") as f:
            part = MIMEApplication(f.read(), Name=os.path.basename(path))
            part['Content-Disposition'] = f'attachment; filename="{os.path.basename(path)}"'
            msg.attach(part)
            
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print("\n[+] Test email successfully sent with 5 invoice attachments!\n")
    except Exception as e:
        print(f"\n[-] Email send error: {e}")
        print("Note: Ensure your SMTP_USER and SMTP_PASS environment variables are configured.")

if __name__ == "__main__":
    send_email()
