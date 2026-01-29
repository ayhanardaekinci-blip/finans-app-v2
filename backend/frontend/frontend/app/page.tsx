"use client";

import { useMemo, useState } from "react";

type Resp = { npv: number; irr: number | null; payback_years: number | null };

export default function Page() {
  const [c0, setC0] = useState(-100000);
  const [wacc, setWacc] = useState(30);
  const [flows, setFlows] = useState([30000, 30000, 30000, 30000, 30000]);
  const [resp, setResp] = useState<Resp | null>(null);
  const [loading, setLoading] = useState(false);

  const cashflowsText = useMemo(() => flows.join(","), [flows]);

  async function calculate() {
    setLoading(true);
    setResp(null);
    try {
      // local backend default
      const r = await fetch("http://localhost:8000/investment/evaluate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ c0, cashflows: flows, wacc })
      });
      const data = (await r.json()) as Resp;
      setResp(data);
    } finally {
      setLoading(false);
    }
  }

  function exportCsv() {
    const rows = [
      ["c0", String(c0)],
      ["wacc_%", String(wacc)],
      ["cashflows", cashflowsText],
      ["npv", resp ? String(resp.npv) : ""],
      ["irr_%", resp?.irr == null ? "" : String(resp.irr)],
      ["payback_years", resp?.payback_years == null ? "" : String(resp.payback_years)]
    ];
    const csv = rows.map(r => r.map(x => `"${x.replaceAll('"', '""')}"`).join(",")).join("\n");
    const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "investment_pack.csv";
    a.click();
    URL.revokeObjectURL(url);
  }

  return (
    <main style={{
      minHeight: "100vh",
      background: "#0B1220",
      color: "#F9FAFB",
      padding: 24,
      fontFamily: "ui-sans-serif, system-ui"
    }}>
      <div style={{
        position: "sticky", top: 0, zIndex: 10,
        background: "#0B1220", paddingBottom: 12, marginBottom: 16
      }}>
        <h1 style={{ fontSize: 28, margin: 0 }}>Investment Pack (NPV / IRR / Payback)</h1>
        <div style={{ opacity: 0.8, marginTop: 6 }}>Dark only • Public demo • CSV export</div>
      </div>

      <section style={{
        display: "grid",
        gridTemplateColumns: "1fr 1fr 1fr",
        gap: 12,
        background: "rgba(255,255,255,0.06)",
        border: "1px solid rgba(255,255,255,0.10)",
        borderRadius: 16,
        padding: 16
      }}>
        <label>
          <div style={{ opacity: 0.8, marginBottom: 6 }}>Initial Investment (CF0)</div>
          <input value={c0} onChange={e => setC0(Number(e.target.value))} style={inp()} />
        </label>
        <label>
          <div style={{ opacity: 0.8, marginBottom: 6 }}>WACC (%)</div>
          <input value={wacc} onChange={e => setWacc(Number(e.target.value))} style={inp()} />
        </label>
        <label>
          <div style={{ opacity: 0.8, marginBottom: 6 }}>Cashflows (comma)</div>
          <input
            value={cashflowsText}
            onChange={e => setFlows(e.target.value.split(",").map(x => Number(x.trim() || 0)))}
            style={inp()}
          />
        </label>

        <div style={{ gridColumn: "1 / -1", display: "flex", gap: 12, marginTop: 8 }}>
          <button onClick={calculate} disabled={loading} style={btn()}>
            {loading ? "Calculating..." : "CALCULATE"}
          </button>
          <button onClick={exportCsv} disabled={!resp} style={btnSecondary()}>
            Download CSV
          </button>
        </div>
      </section>

      {resp && (
        <section style={{
          marginTop: 16,
          display: "grid",
          gridTemplateColumns: "1fr 1fr 1fr",
          gap: 12
        }}>
          <Card title="NPV">{fmt(resp.npv)}</Card>
          <Card title="IRR">{resp.irr == null ? "—" : `%${resp.irr.toFixed(2)}`}</Card>
          <Card title="Payback">{resp.payback_years == null ? "—" : `${resp.payback_years.toFixed(2)} yıl`}</Card>
        </section>
      )}
    </main>
  );
}

function Card({ title, children }: any) {
  return (
    <div style={{
      background: "rgba(255,255,255,0.06)",
      border: "1px solid rgba(255,255,255,0.10)",
      borderRadius: 16,
      padding: 16
    }}>
      <div style={{ opacity: 0.8, marginBottom: 10 }}>{title}</div>
      <div style={{ fontSize: 24, fontWeight: 700 }}>{children}</div>
    </div>
  );
}

function inp(): React.CSSProperties {
  return {
    width: "100%",
    height: 42,
    borderRadius: 12,
    border: "1px solid rgba(255,255,255,0.16)",
    background: "rgba(255,255,255,0.06)",
    color: "#F9FAFB",
    padding: "0 12px",
    outline: "none"
  };
}
function btn(): React.CSSProperties {
  return {
    height: 42,
    padding: "0 14px",
    borderRadius: 12,
    border: "1px solid rgba(255,255,255,0.18)",
    background: "rgba(255,255,255,0.12)",
    color: "#F9FAFB",
    cursor: "pointer"
  };
}
function btnSecondary(): React.CSSProperties {
  return {
    ...btn(),
    background: "transparent"
  };
}
function fmt(n: number) {
  return new Intl.NumberFormat("tr-TR", { maximumFractionDigits: 2 }).format(n);
}
