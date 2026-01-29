from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware

from .finance import (
    npv_from_flows,
    irr_bisection,
    payback_period,
    discounted_payback_period,
    executive_warnings,
)

app = FastAPI(title="CFO-grade Investment Engine", version="1.0.0")

# MVP: public demo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class EvaluateRequest(BaseModel):
    cf0: float = Field(..., description="Initial investment (typically negative)")
    cashflows: List[float] = Field(..., min_length=1, description="t=1..N cashflows")
    wacc: float = Field(..., ge=-0.9999, description="decimal, e.g. 0.30")

class EvaluateResponse(BaseModel):
    npv: float
    irr: Optional[float] = None
    payback: Optional[float] = None
    discounted_payback: Optional[float] = None
    warnings: List[str] = []

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/investment/evaluate", response_model=EvaluateResponse)
def evaluate(req: EvaluateRequest):
    npv = npv_from_flows(req.cf0, req.cashflows, req.wacc)
    irr = irr_bisection(req.cf0, req.cashflows)
    pb = payback_period(req.cf0, req.cashflows)
    dpb = discounted_payback_period(req.cf0, req.cashflows, req.wacc)
    warnings = executive_warnings(req.cf0, req.cashflows, req.wacc, npv, irr)

    return EvaluateResponse(
        npv=npv,
        irr=irr,
        payback=pb,
        discounted_payback=dpb,
        warnings=warnings,
    )
