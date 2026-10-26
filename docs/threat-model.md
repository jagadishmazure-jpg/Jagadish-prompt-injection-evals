# Threat model (OWASP LLM Top 10 focus)
| Risk | Scenario | Control | Gap |
|---|---|---|---|
| LLM01 direct injection | User tells the model to ignore rules | Detectors + gateway policy | Paraphrases evade heuristic |
| LLM01 indirect injection | Hidden instruction in an email or page | Normalise + detect + spotlight | NB over-flags documents |
| LLM06 excessive agency | Injected "call transfer_funds" | Tool allow-list, approval on writes | — |
| LLM02 disclosure | "Reveal your system prompt" | Heuristic pattern | No output-side check here |
