from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np

app = FastAPI(title="Finance Engine", version="0.1.0")

class InvestmentRequest(BaseModel):
    c0: float                # initial investment (negative)
    cashflows: list[float]   # year 1..N
    wacc: float              # percent (e.g., 30 for 30%)

def npv(c0: float, cashflows: list[float], r: float) -> float:
    return float(c0 + sum(cf / ((1 + r) ** (i + 1)) for i, cf in enumerate(cashflows)))

def irr(c0: float, cashflows: list[float]) -> float | None:
    # Use numpy.irr-like via npf is not guaranteed installed; do a simple search with np.roots style is overkill.
    # We'll do a robust bisection on NPV if possible.
    # If NPV never changes sign over range, return None.
    def f(x): return npv(c0, cashflows, x)

    lo, hi = -0.9, 5.0  # -90% to 500%
    flo, fhi = f(lo), f(hi)
    if np.isnan(flo) or np.isnan(fhi) or flo * fhi > 0:
        return None

    for _ in range(120):
        mid = (lo + hi) / 2
        fmid = f(mid)
        if abs(fmid) < 1e-8:
            return float(mid)
        if flo * fmid <= 0:
            hi, fhi = mid, fmid
        else:
            lo, flo = mid, fmid
    return float((lo + hi) / 2)

def payback(c0: float, cashflows: list[float]) -> float | None:
    cum = c0
    for i, cf in enumerate(cashflows, start=1):
        prev = cum
        cum += cf
        if cum >= 0:
            # linear interpolation within year
            if cf == 0:
                return float(i)
            frac = (0 - prev) / cf
            return float((i - 1) + frac)
    return None

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/investment/evaluate")
def investment_evaluate(req: InvestmentRequest):
    r = req.wacc / 100.0
    out_npv = npv(req.c0, req.cashflows, r)
    out_irr = irr(req.c0, req.cashflows)
    out_pb = payback(req.c0, req.cashflows)
    return {
        "npv": out_npv,
        "irr": (out_irr * 100.0) if out_irr is not None else None,
        "payback_years": out_pb,
    }
