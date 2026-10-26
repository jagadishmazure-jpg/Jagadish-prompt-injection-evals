# Training module: measuring prompt-injection defences
**Audience:** AI and security engineers, 1 day.
## Learning objectives
1. Distinguish direct and indirect injection and map them to OWASP LLM01.
2. Compute precision, recall, FPR and a Wilson interval, and explain why n matters.
3. Train a simple classifier without leaking test data.
4. Explain distribution shift (chat prompts vs documents) using this repo's numbers.
5. Argue why tool permissions beat detectors as the primary control.
## Labs
| # | Lab | Done when |
|---|---|---|
| 1 | Run the eval and read every row | Can explain NB vs heuristic trade-off |
| 2 | Sweep NB threshold (-5..5) and plot FPR vs recall | Table added to results |
| 3 | Add 6 new indirect attacks (e.g. markdown image exfil link) | Tests updated; metrics regenerated |
| 4 | Add a homoglyph normaliser | Decoded recall improves without new FPs |
| 5 | Write a known-miss test for an attack you cannot catch | Documented in Limitations |
## Capstone
Add a third detector (any local model or a hosted shield if approved), report it on the same split with CIs, and recommend a layered defence for a fictional insurer's claims agent with numbers.
