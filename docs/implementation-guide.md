# Implementation guide
1. Build a labelled eval set from *your* traffic: direct prompts plus documents/tools outputs your agents read. Keep a public set for comparability.
2. Measure every candidate detector with precision, recall, FPR and confidence intervals; pick thresholds from the FPR your users can tolerate.
3. Normalise untrusted content (strip zero-width, decode obvious encodings) before detection.
4. Enforce least privilege on tools; require approval for writes. This held at 0 simulated successes in this lab even when detectors missed.
5. Mark untrusted content in prompts (datamarking/spotlighting).
6. Gate CI: no regression on the eval set; known misses stay as visible tests.
7. Re-measure when models or detectors change; track drift monthly.
