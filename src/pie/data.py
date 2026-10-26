import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
DS = ROOT / "data" / "third_party" / "deepset-prompt-injections"

def load(split: str) -> list[dict]:
    return [json.loads(line) for line in (DS / f"{split}.jsonl").read_text().splitlines() if line.strip()]
