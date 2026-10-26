"""MEASURED: detectors on the public deepset/prompt-injections test split (116 rows; NB trained on train split only).
Indirect suite is self-written (24 cases, SYNTHETIC); attack success uses a SIMULATED worst-case agent."""
import json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from pie.data import load  # noqa: E402
from pie.detectors import Ensemble, HeuristicDetector, NaiveBayesDetector  # noqa: E402
from pie.indirect import cases, decode_layers, naive_agent  # noqa: E402
from pie.metrics import report  # noqa: E402

def main():
    train, test = load("train"), load("test")
    h, nb = HeuristicDetector(), NaiveBayesDetector().fit(train)
    dets = [h, nb, Ensemble(h, nb, "any"), Ensemble(h, nb, "all")]
    y = [r["label"] for r in test]
    direct = {d.name: report(y, [d.predict(r["text"]) for r in test]) for d in dets}
    ic = cases(); yi = [c["label"] for c in ic]
    indirect = {}
    for d in dets:
        indirect[d.name + " (raw)"] = report(yi, [d.predict(c["text"]) for c in ic])
        indirect[d.name + " (decoded)"] = report(yi, [d.predict(decode_layers(c["text"])) for c in ic])
    attacks = [c["text"] for c in ic if c["label"] == 1]
    asr_none = sum(bool(naive_agent("summarise", t)) for t in attacks)
    best = Ensemble(h, nb, "any")
    asr_det = sum(bool(naive_agent("summarise", t)) for t in attacks if not best.predict(decode_layers(t)))
    asr_ls = sum(bool(naive_agent("summarise", t, allowed_tools={"search_kb"})) for t in attacks)
    m = {}
    for k, r in direct.items():
        m[f"Direct / {k}: precision, recall (95% CI), FPR"] = f"{r['precision']}, {r['recall']} {r['recall_ci95']}, {r['fpr']}"
    for k in ["heuristic (raw)", "heuristic (decoded)", "ensemble_any (decoded)"]:
        r = indirect[k]
        m[f"Indirect (synthetic) / {k}: recall, FPR"] = f"{r['recall']}, {r['fpr']}"
    m["Simulated agent attack success: no defence"] = f"{asr_none}/{len(attacks)}"
    m["Simulated agent attack success: detector gate (ensemble_any, decoded)"] = f"{asr_det}/{len(attacks)}"
    m["Simulated agent attack success: tool allow-list only"] = f"{asr_ls}/{len(attacks)}"
    out = {"label": "MEASURED on public test split; indirect suite SYNTHETIC; agent SIMULATED",
           "sample": "deepset/prompt-injections test n=116 (60 injections); indirect n=24",
           "metrics": m, "direct": direct, "indirect": indirect}
    (ROOT / "results").mkdir(exist_ok=True)
    (ROOT / "results" / "results.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(m, indent=2))

if __name__ == "__main__":
    main()
