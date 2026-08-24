import csv

def merge_apollo_leads(apollo_file="apollo-contacts-export.csv", leads_file="indian_leads.csv"):
    apollo_leads = []
    
    try:
        with open(apollo_file, mode='r', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            for row in reader:
                first_name = row.get('First Name', '').strip()
                last_name = row.get('Last Name', '').strip()
                full_name = f"{first_name} {last_name}".strip()
                
                company = row.get('Company Name', '').strip() or row.get('Company Name for Emails', '').strip()
                title = row.get('Title', '').strip()
                email = row.get('Email', '').strip()
                city = row.get('City', '').strip() or "India"
                
                if email:
                    apollo_leads.append({
                        "name": full_name,
                        "company": company,
                        "title": title,
                        "email": email,
                        "city": city
                    })
    except FileNotFoundError:
        print(f"Error: {apollo_file} not found in current directory. Place the CSV in root.")
        return

    existing_emails = set()
    existing_leads = []
    
    try:
        with open(leads_file, mode='r', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            for row in reader:
                existing_leads.append(row)
                existing_emails.add(row['email'].strip().lower())
    except FileNotFoundError:
        pass

    new_added = 0
    for lead in apollo_leads:
        if lead['email'].lower() not in existing_emails:
            existing_leads.append(lead)
            existing_emails.add(lead['email'].lower())
            new_added += 1

    with open(leads_file, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=["name", "company", "title", "email", "city"])
        writer.writeheader()
        writer.writerows(existing_leads)

    print(f"\n[+] Successfully added {new_added} Apollo leads into {leads_file}. Total dataset count: {len(existing_leads)}\n")

if __name__ == "__main__":
    merge_apollo_leads()
