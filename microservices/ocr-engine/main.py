import os
import json
from pipeline import HybridIngestionPipeline

if __name__ == "__main__":
    pipeline = HybridIngestionPipeline()
    sample_pdf = "sample_invoice.pdf"
    
    if os.path.exists(sample_pdf):
        result = pipeline.process_invoice(sample_pdf)
        print("\n--- Standardized JSON Output ---")
        print(json.dumps(result, indent=2))
    else:
        print(f"Please place a test invoice PDF at '{os.path.abspath(sample_pdf)}' to run the execution test.")
