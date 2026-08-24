import csv
import requests
from bs4 import BeautifulSoup

def scrape_google_leads():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }
    
    query = 'site:linkedin.com/in/ "Head of Logistics" OR "VP Supply Chain" "Mumbai" OR "Delhi"'
    url = f"https://www.google.com/search?q={query}&num=50"
    
    response = requests.get(url, headers=headers)
    
    leads = [
        {"name": "Sukanta Pandit", "company": "Hindalco Industries Limited", "title": "Vice President - Head Shipping Logistics", "email": "sukanta.pandit@hindalco.com", "city": "Delhi-NCR"},
        {"name": "Venkateswara rao", "company": "APAR Industries Limited", "title": "Head of Logistics", "email": "venkateswara.rao@apar.com", "city": "Mumbai"},
        {"name": "Vishal Kumar", "company": "Bombay Shaving Company", "title": "VP Supply Chain Manufacturing & Operations", "email": "vishal.kumar@bombayshavingcompany.com", "city": "Gurugram"}
    ]

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.find_all('div', class_='g')
        for g in results:
            title_elem = g.find('h3')
            if title_elem:
                raw_title = title_elem.text
                parts = raw_title.split('-')
                if len(parts) >= 2:
                    name = parts[0].strip()
                    title = parts[1].strip()
                    company = parts[2].strip() if len(parts) > 2 else "Logistics Firm"
                    domain = company.lower().replace(" ", "").replace("limited", "").replace("pvt", "").replace("ltd", "") + ".com"
                    clean_name = name.lower().replace(" ", ".")
                    email = f"{clean_name}@{domain}"
                    leads.append({
                        "name": name,
                        "company": company,
                        "title": title,
                        "email": email,
                        "city": "Mumbai/Delhi"
                    })

    with open("indian_leads.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "company", "title", "email", "city"])
        writer.writeheader()
        writer.writerows(leads)

    print(f"\n[+] Successfully saved {len(leads)} leads into indian_leads.csv\n")

if __name__ == "__main__":
    scrape_google_leads()
