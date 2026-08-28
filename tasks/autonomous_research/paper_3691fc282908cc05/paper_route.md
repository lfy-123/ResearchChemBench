# Private paper route

## 1. Scientific objective and author claim

The paper tests oxidatively induced concerted C(sp2)-C(sp2) reductive elimination of biphenyl from a MePDI-supported Ti(IV) diaryl model.

## 2. System and model boundary

[(MePDI)TiPh2] reacts with I2 in benzene continuum; the mechanistic sequence includes iodinated intermediates, an elimination TS, [(MePDI)TiI]I3 and iodide coordination.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize and frequency-check structures | intermediates, TS, products | ORCA 6.0.0 | PBE0-D4/def2-TZVP, RIJCOSX, CPCM benzene | geometries and thermal corrections | ev_doc_cd1f6ecb5575_000676_5606f2184091 |
| 2 | Refine energies | optimized structures | ORCA | PBE0-D4/def2-TZVPP, CPCM benzene | electronic energies | ev_doc_cd1f6ecb5575_000676_5606f2184091 |
| 3 | Assemble profile | energies and corrections | thermochemical analysis | Gibbs energies | barrier/profile | ev_doc_cd1f6ecb5575_000687_2a8f667de35c |

## 4. Validation and analysis protocol

The TS has one imaginary mode, reported as -338.32 cm−1. The barrier is measured from [(MePDI)TiPh2I]I3 to the elimination TS.

## 5. Private reference results

The published activation barrier is 19.9 kcal/mol. Table S8 gives a TS relative Gibbs energy of -5.256 kcal/mol and intermediate value -25.237 kcal/mol relative to the overall reference, corresponding to 19.981 kcal/mol.

## 6. Limitations and interpretation boundaries

This is a truncated molecular model and a single computational treatment; the barrier is not an experimental rate measurement.
