import csv
from datetime import datetime

def prepare_and_dispatch_batch1(input_csv="../../verified_leads.csv", batch_size=30):
    dispatched = []
    
    # Check current directory or root for verified_leads.csv
    import os
    target_csv = "verified_leads.csv" if os.path.exists("verified_leads.csv") else "../../verified_leads.csv"
    
    with open(target_csv, mode='r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        for idx, row in enumerate(reader, 1):
            if idx > batch_size:
                break
            dispatched.append({
                "batch_id": "BATCH_01",
                "recipient_name": row['name'],
                "company": row['company'],
                "email": row['email'],
                "status": "QUEUED_FOR_DISPATCH",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            
    output_file = "batch_1_outreach_log.csv"
    with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=["batch_id", "recipient_name", "company", "email", "status", "timestamp"])
        writer.writeheader()
        writer.writerows(dispatched)
        
    print(f"\n[+] Batch 1 Queue Prepared: {len(dispatched)} leads saved to {output_file}\n")

if __name__ == "__main__":
    prepare_and_dispatch_batch1()
