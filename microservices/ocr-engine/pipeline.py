import hashlib
import redis
import json
import os
from google import genai
from google.genai import types
from schemas import NormalizedInvoice
from local_ocr import LocalOCREngine

class HybridIngestionPipeline:
    def __init__(self):
        self.ocr_engine = LocalOCREngine()
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        self.gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    def _compute_pdf_hash(self, pdf_path: str) -> str:
        hasher = hashlib.sha256()
        with open(pdf_path, 'rb') as f:
            hasher.update(f.read())
        return f"pdf_cache:{hasher.hexdigest()}"

    def process_invoice(self, pdf_path: str) -> dict:
        cache_key = self._compute_pdf_hash(pdf_path)
        cached_result = self.redis_client.get(cache_key)

        if cached_result:
            print("CACHE HIT: Returning cached invoice data from Redis.")
            return json.loads(cached_result)

        print("CACHE MISS: Extracting PDF with Local OCR Engine...")
        extracted_text = self.ocr_engine.extract_text_from_pdf(pdf_path)

        prompt = f"""
        You are an expert freight audit system. Parse the following raw text extracted from a freight invoice document into the target JSON schema.
        
        Extraction Guidance:
        - carrier_id: The carrier or billing company name (e.g., Express Freight Lines or Shipper Logistics Inc.).
        - invoice_number: Exact invoice number string (e.g., INV-76469).
        - bol_number: BOL or Bill of Lading number (e.g., BOL-2026-0824-001).
        - invoice_date: Date in YYYY-MM-DD format (e.g., 2026-08-23).
        - payment_terms: Payment terms string (e.g., Net 30).
        - total_amount: Total numeric balance due (e.g., 1301.40).
        - line_items: Items under charges like Freight - LTL Shipment.
        - accessorial_charges: Additional charges like Liftgate, Fuel Surcharge, Inside Delivery.

        Raw Extracted Document Text:
        {extracted_text}
        """

        print("Calling gemini-3.6-flash with structured schema...")
        response = self.gemini_client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=NormalizedInvoice,
            ),
        )

        parsed_data = json.loads(response.text)
        self.redis_client.setex(cache_key, 86400, json.dumps(parsed_data))

        return parsed_data
