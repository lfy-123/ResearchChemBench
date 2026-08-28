# Scientific objective

Determine, by independent computation, how the meta-ring halogen (Cl, Br, or I) changes the periodic electronic band gap and band-edge character of three isostructural quasi-1D pyridinium lead bromide crystals. Establish the ordering/trend across the named materials and assess whether a defined structural descriptor explains it. Do not assume a mechanism or author interpretation; propose plausible explanations only when supported by your calculations.

# Public inputs and scientific boundaries

Use `data/inputs/crystal_records.json`. The objects are exactly the 300 K experimental CCDC records 2499860 (Cl), 2499862 (Br), and 2499861 (I), each P21/c with Z=4. The CCDC connector is an allowed controlled database input; no paper, SI, general-web search, or unpinned substitute structure may be used. Preserve identity, charge/protonation, occupancy, cell and coordinates from each record. The measured object is the electronic band gap of each periodic crystal and its band-edge character. SOC may be computed directly or represented by a clearly labelled validated approximation, but the two must not be conflated.

# Required scientific validation/investigation

Choose and justify a periodic electronic-structure method, relativistic treatment, pseudopotential/basis, k-point sampling, smearing/occupancy, convergence and band-path or mesh. For each named object, demonstrate numerical stability of the reported gap against at least one relevant numerical setting, inspect band dispersion, and support orbital character with projected DOS, projections, or a justified alternative. Define any structural descriptor before testing it and retain object identity for every comparison. Completion requires validated results for all three objects or a bounded-failure report with exact failed object, attempts, evidence and consequence. Stop when all three objects meet the validation criteria, or when the chosen method/resource boundary makes further work non-informative; report coverage, alternative hypotheses considered, and limitations.

# Deliverables

Submit `report/results.json` plus cited computational artifacts under paths declared in the JSON. Include per-object identity, method summary, gap, uncertainty/stability estimate, directness, edge locations, orbital-character evidence, validation status, structural comparison, independently reasoned conclusion and limitations. If bounded failure is used, include the failed-object branch and do not fabricate missing values.
