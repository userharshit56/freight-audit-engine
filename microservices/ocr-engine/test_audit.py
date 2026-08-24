from audit_engine import AuditEngine

# Initialize with $3.80/gal current diesel price
engine = AuditEngine(diesel_index_price=3.80, base_diesel_threshold=3.00)

# 1. Duplicate Detection
hash_1 = engine.generate_shipment_hash("FEDEX", "BOL-99823", "2026-08-24", 1450.50)
hash_2 = engine.generate_shipment_hash("FEDEX", "BOL-99823", "2026-08-24", 1450.50)
print(f"Hash Match (Duplicate Detected): {hash_1 == hash_2} -> {hash_1[:12]}...")

# 2. Line Item Variance
# Invoiced: $1,250.00 | Contract: $1,000.00 | Accessorials: 5% lift | Distance: 500 miles
variance = engine.calculate_line_item_variance(
    invoiced_price=1250.00, 
    contract_price=1000.00, 
    accessorial_rates=[0.05], 
    distance_miles=500.0
)
print(f"Line Item Variance: ${variance:.2f}")

# 3. Confidence Routing
score, route = engine.compute_audit_confidence(s_ocr=0.98, s_rule_match=0.90, s_llm=0.95)
print(f"Audit Score: {score} -> Route: {route}")
