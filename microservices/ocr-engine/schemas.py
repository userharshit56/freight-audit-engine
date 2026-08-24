from pydantic import BaseModel, Field
from typing import List, Optional

class LineItem(BaseModel):
    description: str = Field(description="Description of item (Line-Haul, Fuel Surcharge, etc.)")
    weight_lbs: Optional[float] = Field(default=None, description="Weight in pounds if applicable")
    rate: Optional[float] = Field(default=None, description="Rate per unit or flat charge")
    amount: float = Field(description="Final charge amount for this line item")

class AccessorialCharge(BaseModel):
    code: str = Field(description="Accessorial charge type (LIFTGATE, RESIDENTIAL, DETENTION, RECONSIGNMENT, etc.)")
    amount: float = Field(description="Charge amount for accessorial")

class NormalizedInvoice(BaseModel):
    carrier_id: str = Field(description="Carrier ID or SCAC code")
    invoice_number: str = Field(description="Unique carrier invoice number")
    bol_number: Optional[str] = Field(default=None, description="Bill of Lading number")
    invoice_date: str = Field(description="Invoice date in YYYY-MM-DD format")
    payment_terms: Optional[str] = Field(default="Net 30", description="Payment terms")
    line_items: List[LineItem] = Field(default_factory=list)
    accessorial_charges: List[AccessorialCharge] = Field(default_factory=list)
    total_amount: float = Field(description="Total invoice amount")
