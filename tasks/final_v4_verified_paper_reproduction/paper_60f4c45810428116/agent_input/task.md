# Kinetic information in a microflow residence-time grid

## Scientific question

What kinetic information about benzyl chloromethyl sulfide 1a can be established from the supplied residence-time/temperature observations, and which rate, mechanism or optimum claims remain unidentifiable?

## Input files

- `data/inputs/kinetic_observations.json`: all 25 grid positions, including 23 non-clogged observations, two clogged positions, reactor dimensions and the original categorical entries.
- `data/inputs/systems.json`: chemical identities of the precursor, measured products and associated species.
- `data/inputs/observations.json` and `data/inputs/source_facts.json`: measurement definitions and flow/quench conditions.

## Scope

The system mixes 0.050 M 1a in THF at 10 mL/min with 0.30 M LiNp at 5 mL/min, followed by 0.30 M MeOH at 5 mL/min. R1 residence times span 0.002–6.3 s at −78–0 °C; post-capture residence is 2.4 s. Saturated aqueous NH4Cl completes quenching. GC with undecane measures 2a, 3a and recovered 1a after quench. Account for stream dilution when interpreting concentrations. Preserve trace, n.d., dash and clogging as reported; numerical detection limits, replicates and measurement variances are unavailable.

Study this 1a dataset. Select a quantitative representation and the assumptions needed for its interpretation. Other leaving groups, new experiments and full reactor CFD are outside scope. All rows are public, so any data split is retrospective.

## Author baseline for reproduction

The authors interpret the yield band as competition between generation and decomposition of a capturable active species (main pp3–4). Their two-dimensional linear radial-basis-function interpolation uses smoothing 0.2 and extrapolates the two clogged positions (SI pp5–6). Reproduce and assess this disclosed baseline, declaring unspecified coordinate/library/polynomial conventions and justified substitutions. Exact agreement with a uniquely specified author surface is not implied. The paper reports no independently calibrated elementary rates or fixed five-pool network. Its return-to-starting-material discussion for 1h/SPh does not specify the chemistry of 1a/chloride. Auxiliary redox calculations use Gaussian16, B3LYP-D3/6-311+G(d,p), SMD THF and a ferrocene reference (SI p19); they are not required to turn this grid into a kinetic analysis. Any new fitting or identifiability inference is your analysis, not a reported author result. The supplied table is the observation baseline; plotted labels differ at entries 3, 7 and 17.

## Required results

1. Explain the temperature/residence-time dependence of the measured products through a quantitative observation model, including what the post-quench measurements reveal about in-reactor behavior.
2. Report the effective rate information, bounds or identifiable combinations supported by your analysis, with units, conditions and the assumptions required for that interpretation.
3. Determine whether elementary formation, consumption and capture parameters or a microscopic network are uniquely determined. Support the answer with a specific identifiability argument and state its reach across the measured channels.
4. Determine what the sampled grid can establish about productive conditions and a continuous optimum, distinguishing measured points, interpolation and extrapolation.

## Submission

Submit `report/results.json` and `report/report.md` under the supplied schema and guide. Link executed analysis, inputs and numerical outputs. Only final scientific conclusions receive points. Beyond the disclosed author baseline, no particular model, software, number of fits or quantum calculation is required. Use public inputs and available tools plus general documentation; do not access private evaluation files or prior verification archives.
