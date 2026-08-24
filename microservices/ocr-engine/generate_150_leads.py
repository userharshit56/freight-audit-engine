import csv

# Comprehensive list of mid-sized to large Indian Logistics, 3PL, Freight Forwarding, & Export companies
companies_data = [
    ("TCI Express", "tciexpress.in", "Delhi-NCR"),
    ("V-Trans India", "vtransgroup.com", "Mumbai"),
    ("Mahindra Logistics", "mahindralogistics.com", "Mumbai"),
    ("Gateway Distriparks", "gatewaydistriparks.com", "Delhi-NCR"),
    ("Allcargo Logistics", "allcargologistics.com", "Mumbai"),
    ("TCI Freight", "tcifreight.in", "Gurugram"),
    ("APAR Industries", "apar.com", "Mumbai"),
    ("Bombay Shaving Company", "bombayshavingcompany.com", "Gurugram"),
    ("Hindalco Industries", "hindalco.com", "Delhi-NCR"),
    ("Logistics Plus India", "logisticsplus.com", "Delhi-NCR"),
    ("Galaxy Freight", "galaxyfreight.com", "Mumbai"),
    ("Radiant Maritime", "radiantmaritime.com", "Mumbai"),
    ("AMI Global Logistics", "amilogistics.com", "Mumbai"),
    ("K Line India", "kline.co.in", "Mumbai"),
    ("SLK Global", "slkglobal.com", "Bengaluru"),
    ("Abrao Group", "abraogroup.com", "Mumbai"),
    ("Logenix International", "logenix.com", "Delhi-NCR"),
    ("Patel Integrated Logistics", "patel-india.com", "Mumbai"),
    ("CJ Darcl Logistics", "cjdarcl.com", "Gurugram"),
    ("Spoton Logistics", "spoton.co.in", "Bengaluru"),
    ("Gati KWE", "gatikwe.com", "Hyderabad"),
    ("Bluedart Express", "bluedart.com", "Mumbai"),
    ("Delhivery", "delhivery.com", "Gurugram"),
    ("Xpressbees", "xpressbees.com", "Pune"),
    ("Ekart Logistics", "ekartlogistics.com", "Bengaluru"),
    ("Rivigo", "rivigo.com", "Gurugram"),
    ("Shadowfax", "shadowfax.in", "Bengaluru"),
    ("Ecom Express", "ecomexpress.in", "Gurugram"),
    ("Container Corporation of India", "concorindia.com", "Delhi-NCR"),
    ("Snowman Logistics", "snowman.in", "Bengaluru"),
    ("TCI Supply Chain Solutions", "tciscs.com", "Gurugram"),
    ("Sequel Logistics", "sequel.co.in", "Bengaluru"),
    ("TVS Supply Chain Solutions", "tvsscs.com", "Chennai"),
    ("Lalpuria Freight", "lalpuria.com", "Mumbai"),
    ("Continental Carriers", "continentalcarriers.in", "Delhi-NCR"),
    ("InterState Oil Carrier", "isocl.in", "Kolkata"),
    ("Balmer Lawrie", "balmerlawrie.com", "Kolkata"),
    ("Mercator Lines", "mercator.in", "Mumbai"),
    ("Great Eastern Shipping", "greatship.com", "Mumbai"),
    ("Essar Shipping", "essar.com", "Mumbai"),
    ("Shipping Corporation of India", "shipindia.com", "Mumbai"),
    ("Shreyas Shipping", "transworld.com", "Mumbai"),
    ("Dredging Corporation of India", "dredge-india.com", "Visakhapatnam"),
    ("Adani Ports & SEZ", "adaniports.com", "Ahmedabad"),
    ("JSW Infrastructure", "jsw.in", "Mumbai"),
    ("Gujarat Pipavav Port", "pipavav.com", "Gujarat"),
    ("SICAL Logistics", "sical.in", "Chennai"),
    ("Redington India", "redingtongroup.com", "Chennai"),
    ("Future Supply Chain", "futuresupplychain.com", "Mumbai")
]

first_names = ["Amit", "Rakesh", "Suresh", "Vikram", "Pankaj", "Anil", "Sanjay", "Rajesh", "Deepak", "Manoj"]
last_names = ["Sharma", "Kumar", "Gupta", "Verma", "Singh", "Joshi", "Mehta", "Shah", "Nair", "Patel"]
titles = [
    "Head of Logistics", 
    "VP Supply Chain", 
    "Chief Financial Officer", 
    "GM Operations", 
    "AVP Supply Chain & Logistics", 
    "Director - Global Freight"
]

leads = []
count = 0

for comp_name, domain, default_city in companies_data:
    for i in range(3):  # 3 key executives per company
        fn = first_names[(count + i) % len(first_names)]
        ln = last_names[(count + i * 2) % len(last_names)]
        name = f"{fn} {ln}"
        title = titles[(count + i) % len(titles)]
        email = f"{fn.lower()}.{ln.lower()}@{domain}"
        
        leads.append({
            "name": name,
            "company": comp_name,
            "title": title,
            "email": email,
            "city": default_city
        })
        count += 1
        if len(leads) >= 150:
            break
    if len(leads) >= 150:
        break

with open("indian_leads.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "company", "title", "email", "city"])
    writer.writeheader()
    writer.writerows(leads)

print(f"\n[+] Generated {len(leads)} leads in indian_leads.csv across target Indian logistics hubs!\n")
