# ADR 0001: Treat detectors as signals; enforce with tool permissions
Status: accepted. Evidence in this repo: detector recall on the public split is well below 1.0, and indirect FPR is high, while a tool allow-list blocked all simulated attacks. Decision: permissions and approvals are the enforcement boundary; detectors feed alerts and risk scores.
