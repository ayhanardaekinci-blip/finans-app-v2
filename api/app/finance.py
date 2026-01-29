from __future__ import annotations
from typing import List, Optional
import numpy as np

def npv_from_flows(cf0: float, cfs: List[float], r: float) -> float:
    total = cf0
    for t, cf in enumerate(cfs, start=1):
        total += cf / ((1.0 + r) ** t)
    return float(total)

def irr_bisection(
    cf0: float,
    cfs: List[float],
    low: float = -0.9,
    high: float = 5.0,
    tol: float = 1e-7,
    max_iter: int = 200,
) -> Optional[float]:
    # Robust bisection on NPV(rate)=0
    f_low = npv_from_flows(cf0, cfs, low)
    f_high = npv_from_flows(cf0, cfs, high)

    # try expanding high to find sign change
    if f_low * f_high > 0:
        h = high
        for _ in range(20):
            h *= 2
            if h > 1e6:
                break
            f_h = npv_from_flows(cf0, cfs, h)
            if f_low * f_h <= 0:
                high, f_high = h, f_h
                break

    if f_low * f_high > 0:
        return None

    a, b = low, high
    fa, fb = f_low, f_high

    for _ in range(max_iter):
        m = (a + b) / 2.0
        fm = npv_from_flows(cf0, cfs, m)

        if abs(fm) < tol:
            return float(m)

        if fa * fm <= 0:
            b, fb = m, fm
        else:
            a, fa = m, fm

        if abs(b - a) < tol:
            return float((a + b) / 2.0)

    return float((a + b) / 2.0)

def payback_period(cf0: float, cfs: List[float]) -> Optional[float]:
    # Bu mantık senin dosyadakiyle aynı: lineer interpolasyon :contentReference[oaicite:2]{index=2}
    cum = cf0
    if cum >= 0:
        return 0.0

    for i, cf in enumerate(cfs, start=1):
        prev = cum
        cum += cf
        if cum >= 0:
            if cf == 0:
                return float(i)
            frac = (0 - prev) / cf
            return float((i - 1) + frac)
    return None

def discounted_payback_period(cf0: float, cfs: List[float], r: float) -> Optional[float]:
    # Bu da senin dosyadakiyle aynı :contentReference[oaicite:3]{index=3}
    cum = cf0
    if cum >= 0:
        return 0.0

    for i, cf in enumerate(cfs, start=1):
        disc_cf = cf / ((1.0 + r) ** i)
        prev = cum
        cum += disc_cf
        if cum >= 0:
            if disc_cf == 0:
                return float(i)
            frac = (0 - prev) / disc_cf
            return float((i - 1) + frac)
    return None

def executive_warnings(cf0: float, cfs: List[float], wacc: float, npv: float, irr: Optional[float]) -> List[str]:
    warnings: List[str] = []
    if npv < 0:
        warnings.append("NPV < 0 at WACC: proje mevcut varsayımlarla değer yaratmıyor.")
    if irr is None:
        warnings.append("IRR güvenilir bulunamadı (NPV kökü bulunamadı / non-standard cashflow). NPV'yi öncelikle yorumlayın.")
    else:
        if irr < wacc:
            warnings.append("IRR < WACC: hurdle rate geçilemiyor.")
        if irr > 1.0:
            warnings.append("IRR > 100%: nakit akışı zamanlaması/işaret değişimleri gözden geçirilmeli.")

    # sign changes check (multiple IRR risk)
    series = [cf0] + cfs
    signs = []
    for x in series:
        signs.append(1 if x > 0 else (-1 if x < 0 else 0))
    last = None
    changes = 0
    for s in signs:
        if s == 0:
            continue
        if last is None:
            last = s
        elif s != last:
            changes += 1
            last = s
    if changes >= 2:
        warnings.append("Nakit akışında birden fazla işaret değişimi var: IRR yanıltıcı/çoklu olabilir. NPV profiliyle birlikte değerlendirin.")
    return warnings
