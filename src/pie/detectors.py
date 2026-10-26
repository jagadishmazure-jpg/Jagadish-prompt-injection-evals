"""Offline injection detectors.

- HeuristicDetector: hand-written patterns (English + German), no training.
- NaiveBayesDetector: multinomial NB over word unigrams/bigrams + char 4-grams, trained on the public train split only.
- Ensemble: flags if either flags (recall-oriented) or both flag (precision-oriented).
Production stand-ins: Azure AI Content Safety Prompt Shields, Llama Guard / Prompt Guard, NeMo Guardrails."""
import math, re
from collections import Counter

PATTERNS = [
    r"\bignore (all |any )?(the )?(previous|prior|above|earlier)\b", r"\bforget (all |everything|about)",
    r"\bdisregard\b", r"\bnew (task|tasks|instructions?)\b", r"\byou are now\b", r"\bact as\b",
    r"\bpretend (to be|you)\b", r"\bsystem prompt\b", r"\bjailbreak\b", r"\bdo anything now\b", r"\bDAN\b",
    r"\breveal\b.*\b(prompt|instructions|password|secret)", r"\boverride\b", r"\bnow (you|answer|focus|say)\b",
    r"\bvergiss\b", r"\bignorier", r"\bneue aufgabe", r"\bdu bist (jetzt|nun)\b", r"\bvorherigen\b", r"\bab jetzt\b",
]
RX = [re.compile(p, re.I) for p in PATTERNS]

class HeuristicDetector:
    name = "heuristic"
    def predict(self, text: str) -> int:
        return int(any(r.search(text) for r in RX))

def feats(text: str) -> list[str]:
    t = text.lower()
    w = re.findall(r"\w+", t)
    out = w + [a + "_" + b for a, b in zip(w, w[1:])]
    s = re.sub(r"\s+", " ", t)
    out += ["c:" + s[i:i + 4] for i in range(max(0, len(s) - 3))]
    return out

class NaiveBayesDetector:
    name = "naive_bayes"
    def __init__(self, alpha: float = 1.0, threshold: float = 0.0):
        self.alpha, self.threshold = alpha, threshold

    def fit(self, rows):
        self.c = {0: Counter(), 1: Counter()}
        n = Counter(r["label"] for r in rows)
        for r in rows:
            self.c[r["label"]].update(feats(r["text"]))
        self.vocab = set(self.c[0]) | set(self.c[1])
        self.tot = {k: sum(v.values()) for k, v in self.c.items()}
        self.prior = {k: math.log(n[k] / len(rows)) for k in (0, 1)}
        return self

    def score(self, text: str) -> float:
        V = len(self.vocab)
        s = {k: self.prior[k] + sum(math.log((self.c[k][f] + self.alpha) / (self.tot[k] + self.alpha * V))
                                    for f in feats(text) if f in self.vocab) for k in (0, 1)}
        return s[1] - s[0]

    def predict(self, text: str) -> int:
        return int(self.score(text) > self.threshold)

class Ensemble:
    def __init__(self, a, b, mode: str = "any"):
        self.a, self.b, self.mode = a, b, mode
        self.name = f"ensemble_{mode}"
    def predict(self, text: str) -> int:
        x, y = self.a.predict(text), self.b.predict(text)
        return int(x or y) if self.mode == "any" else int(x and y)
