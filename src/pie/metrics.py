import math

def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (0.0, 0.0)
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))

def confusion(y, p):
    tp = sum(a == 1 and b == 1 for a, b in zip(y, p)); fp = sum(a == 0 and b == 1 for a, b in zip(y, p))
    fn = sum(a == 1 and b == 0 for a, b in zip(y, p)); tn = sum(a == 0 and b == 0 for a, b in zip(y, p))
    return tp, fp, fn, tn

def report(y, p) -> dict:
    tp, fp, fn, tn = confusion(y, p)
    prec = tp / (tp + fp) if tp + fp else 0.0
    rec = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
    return {"tp": tp, "fp": fp, "fn": fn, "tn": tn, "precision": round(prec, 3), "recall": round(rec, 3),
            "f1": round(f1, 3), "fpr": round(fp / (fp + tn), 3) if fp + tn else 0.0,
            "recall_ci95": [round(x, 3) for x in wilson(tp, tp + fn)]}
