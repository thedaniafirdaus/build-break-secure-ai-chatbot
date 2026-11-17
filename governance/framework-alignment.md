# Framework alignment: NIST AI RMF and ISO/IEC 42001

This shows how Brightwell Home's AI governance artefacts are **aligned with** the NIST AI Risk Management Framework (AI RMF 1.0) and ISO/IEC 42001:2023. It is a self-assessed mapping for a fictional company. It is **not** a certification or audit: ISO/IEC 42001 certification needs an accredited body to audit a full AI management system.

**Artefacts**
- [AI Use-Case Register](ai-use-case-register.csv): 10 AI uses with tier, risks, controls, owner and review date
- [Responsible AI Use Policy](responsible-ai-use-policy.md): one-page staff policy
- [Leadership report](../REPORT.md) and red-team results in the [README](../README.md): risk assessment and testing of the customer-service agent (AI-01)

## Mapping

| NIST AI RMF function | What Brightwell has | Evidence | ISO/IEC 42001 (aligned with) |
|---|---|---|---|
| **Govern** — policies, accountability, culture | Plain-English AI policy; named owner for every use; AI Lead and quarterly AI Review Group; blame-free reporting; rules for third-party tools | Policy §1–5; register *Owner* column | Clause 5.2 AI policy; 5.3 roles and responsibilities; 7.3 awareness; Annex A.2 (AI policy), A.3 (internal organisation), A.10 (third parties) |
| **Map** — know your AI and its context | Inventory of 10 AI uses, including vendor features and shadow AI; data and personal-data flags; who is affected; risk tiers with written criteria | Register columns *Team*, *AI tool or vendor*, *Data used*, *Personal data*, *Risk tier*; policy §4 | Clause 4.1 context; 6.1.2 AI risk assessment; 6.1.4 AI system impact assessment; Annex A.4 (resources), A.5 (impact assessment), A.7 (data) |
| **Measure** — test and track | Red-team of AI-01 with 13 attacks mapped to OWASP LLM Top 10; before/after results (v1 6/12 succeeded or partial → v2 0/12); 5×5 risk scores; security event log; bias and false-positive checks planned for AI-03 and AI-06 | README results table; REPORT.md risk scores; register *Controls* | Clause 9.1 monitoring and measurement; Annex A.6 (AI system life cycle: verification, validation, event logs) |
| **Manage** — treat, monitor, respond | Controls recorded per use; human approval for high-impact decisions; residual risks accepted with owners; incident reporting route; review dates by tier | Register *Controls* and *Review date*; policy §3–4; REPORT.md residual risks | Clause 6.1.3 / 8.3 AI risk treatment; 10 improvement; Annex A.8 (information for users), A.9 (responsible use of AI systems) |

## Gaps (what a full ISO/IEC 42001 system would still need)

- Formal AI management system scope and objectives (clauses 4.3, 6.2)
- Statement of Applicability for the Annex A controls
- Completed impact assessments and DPIAs for the medium and high uses (AI-03 is the priority)
- Internal audit and management review records (clauses 9.2, 9.3)
- Staff training delivered and recorded (clause 7.2)
- Supplier due-diligence records for vendor AI features (AI-03, AI-05, AI-06)
