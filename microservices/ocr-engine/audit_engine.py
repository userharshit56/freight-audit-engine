import hashlib
from typing import Dict, Any, List, Tuple

class AuditEngine:
    def __init__(self, diesel_index_price: float, base_diesel_threshold: float = 3.00, fuel_rate_per_gallon: float = 0.05):
        self.diesel_index_price = diesel_index_price
        self.base_diesel_threshold = base_diesel_threshold
        self.fuel_rate_per_gallon = fuel_rate_per_gallon

    def generate_shipment_hash(self, carrier_id: str, bol_number: str, ship_date: str, total_weight: float) -> str:
        """
        SHA-256 Hash to uniquely identify duplicate shipments:
        H(Bi) = SHA-256(Carrier ID || BOL Number || Ship Date || Total Weight)
        """
        payload = f"{carrier_id.strip().upper()}|{bol_number.strip().upper()}|{ship_date.strip()}|{float(total_weight):.2f}"
        return hashlib.sha256(payload.encode('utf-8')).hexdigest()

    def calculate_fuel_surcharge(self, distance_miles: float) -> float:
        """
        Calculates dynamic fuel surcharge based on current DOE diesel price vs threshold.
        """
        if self.diesel_index_price <= self.base_diesel_threshold:
            return 0.0
        
        excess_fuel_cost = (self.diesel_index_price - self.base_diesel_threshold) / 0.10
        surcharge_per_mile = excess_fuel_cost * self.fuel_rate_per_gallon
        return round(distance_miles * surcharge_per_mile, 2)

    def calculate_line_item_variance(
        self, 
        invoiced_price: float, 
        contract_price: float, 
        accessorial_rates: List[float], 
        distance_miles: float
    ) -> float:
        """
        Delta Vi = P_invoiced - (P_contract * (1 + sum(alpha_accessorial)) + S_fuel(t))
        """
        accessorial_multiplier = 1.0 + sum(accessorial_rates)
        fuel_surcharge = self.calculate_fuel_surcharge(distance_miles)
        
        expected_total = (contract_price * accessorial_multiplier) + fuel_surcharge
        variance = invoiced_price - expected_total
        return round(variance, 2)

    def compute_audit_confidence(self, s_ocr: float, s_rule_match: float, s_llm: float) -> Tuple[float, str]:
        """
        C_audit = 0.30 * S_OCR + 0.50 * S_RuleMatch + 0.20 * S_LLM Verification
        """
        c_audit = (0.30 * s_ocr) + (0.50 * s_rule_match) + (0.20 * s_llm)
        c_audit = round(c_audit, 4)

        if c_audit >= 0.95:
            action = "AUTONOMOUS_DISPUTE"
        elif 0.70 <= c_audit < 0.95:
            action = "HUMAN_REVIEW"
        else:
            action = "RE_PARSE"

        return c_audit, action
