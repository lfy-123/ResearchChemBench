# Heterobiaryl P(V) benchmark curation audit

- Source archive SHA-256: `8eabaa038742516b013e3b80301b9d420e98400a8e74d06f8246e06c8a806330`
- Public anonymous archive SHA-256: `97fa402aec3fa9191d0352485c7c4a8c77415d47d7c917dcb1cc0548f04d495d`
- Public archive size: 71388896 bytes
- Public archive entries: 298 (240266644 uncompressed bytes)
- Computational record files: 198
- Starting structures: 27
- Candidate systems: {'P0': 17, 'P1': 25, 'P2': 24}
- Integrity and anonymity scans: passed

## Corrections and fairness decisions

1. The protonation NMR observation points to Fig. S12 in the paper text; the supplied task package incorrectly cited Figs. S17-S18. The public evidence table is corrected.
2. All explicit Action/backend/software recommendations were removed from tested task prompts.
3. The author archive contains 66 frequency records, 66 large-basis single-point records, and 66 correlated single-point records, but no archived IRC trajectory, population trajectory, or explicit C-O transition-state record.
4. The correlated single-point records took roughly 5-8 wall-clock hours each in the author archive. Requiring all 66 to be recomputed inside a normal Agent evaluation would test budget rather than scientific orchestration. The anonymous records are therefore supplied as auditable input, while independent recalculation remains available to the Agent.
5. Published rounded free energies and the 353.15 K, 1 M GoodVibes 4.3 recomputation are stored separately.
6. The five subtasks and end-to-end task use rubric scoring. No exact tool name or unique invocation order is part of the public question or hidden scoring requirement.
