import csv
import re
import dns.resolver

EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

def check_mx_record(domain):
    try:
        records = dns.resolver.resolve(domain, 'MX')
        return len(records) > 0
    except Exception:
        return False

def validate_email(email):
    email = email.strip()
    if not re.match(EMAIL_REGEX, email):
        return False, "Invalid Syntax"
    
    domain = email.split('@')[1]
    if not check_mx_record(domain):
        return False, "No MX Record"
    
    return True, "Deliverable (MX Verified)"

def process_lead_list(input_csv="indian_leads.csv", output_csv="verified_leads.csv"):
    verified_count = 0
    
    with open(input_csv, mode='r', encoding='utf-8') as infile, \
         open(output_csv, mode='w', newline='', encoding='utf-8') as outfile:
        
        reader = csv.DictReader(infile)
        fieldnames = list(reader.fieldnames) + ['validation_status', 'is_valid']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for row in reader:
            is_valid, status = validate_email(row['email'])
            row['validation_status'] = status
            row['is_valid'] = is_valid
            writer.writerow(row)
            if is_valid:
                verified_count += 1
                
    print(f"\n[+] Validation Complete! Verified {verified_count} deliverable leads saved to {output_csv}\n")

if __name__ == "__main__":
    process_lead_list()
