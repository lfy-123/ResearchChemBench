# Scientific objective

Independently test the authors' qualitative hypothesis that bisulfate radical can abstract hydrogen from methane in concentrated sulfuric acid. Determine a defensible solution-phase free-energy barrier for the elementary HSO4• + CH4 HAT event and identify the resulting radical/product-side state. The scored object is the validated HAT transition structure and its barrier relative to the submitted reactant reference state; the authors' winning geometry and numerical result are not provided.

# Public inputs and scientific boundaries

Use `data/inputs/system_specification.json`. It uniquely fixes CH4, neutral doublet HSO4•, neutral singlet H2SO4, the 98% sulfuric-acid continuum, 298.15 K, and the single-elementary-step boundary. You may generate 3-D conformers and transition-state guesses. Do not use the paper, SI, general web, or hidden source coordinates. Do not claim experimental kinetics. Report the charge, multiplicity, atom mapping, and standard-state convention used.

# Required scientific validation/investigation

Generate and deduplicate a finite set of chemically distinct reactant-complex and H-transfer TS hypotheses, retaining identity and provenance for each. Optimize the selected minima and saddle candidates with a defensible electronic-structure method, validate minima by zero imaginary frequencies and TS candidates by exactly one imaginary frequency whose displacement is H transfer from methane to the radical oxygen framework, and verify connectivity by an IRC or an equivalent reactant/product displacement analysis. Refine at least the selected stationary points consistently and quantify method/conformer sensitivity. The calculation is complete when one candidate passes all stationary-point and connectivity tests or when no candidate can be validated; in the latter case report the failed candidates and limiting reason. Stop after the stated candidate-generation strategy is exhausted and additional guesses are duplicates or fail validation; report coverage and limitations.

# Deliverables

Write `report/results.json` with candidate identities, validation evidence, selected barrier in kcal/mol, product-side structure, uncertainty/sensitivity, conclusion, and either `completed` or a truthful bounded-failure status. Include enough coordinates or structure identifiers for independent checking. A successful result must identify the validated TS and both reference states; a bounded failure must include attempted candidates and failure diagnostics. Do not copy source-paper text.
