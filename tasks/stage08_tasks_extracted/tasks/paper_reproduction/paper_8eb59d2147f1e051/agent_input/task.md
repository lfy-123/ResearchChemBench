# Scientific objective

Determine, by independent computational investigation, how the Li2S decomposition kinetics differ between Fe3Se4 and Fe2NiSe4 surfaces. Establish a defensible barrier for each host, compare their ordering and difference, and decide what kinetic conclusion is supported by the calculations. If multiple surface or endpoint models remain plausible, discriminate them and state the residual ambiguity. Generate and test your own mechanistic explanations and pathways.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors attribute changes in sulfur-conversion kinetics to Ni-modified electronic structure and charge redistribution at Fe/Se/Ni sites, which alter adsorbate–surface interactions.

**Candidate route or mechanism.**
Consider surface-assisted Li–S bond cleavage in adsorbed Li2S as the candidate decomposition event, with Ni-modified charge transfer as a possible explanation for a host-dependent barrier.

**Discriminating evidence.**
The authors use spin-polarized DFT and climbing-image nudged elastic band calculations to compare decomposition minimum-energy paths. Density-of-states and charge-density-difference analyses for adsorbed Li2S provide complementary evidence for the proposed electronic origin of any kinetic difference.

# Public inputs and scientific boundaries

`data/inputs/system_definition.json` identifies Fe3Se4 by ICSD 96-153-7571 and Fe2NiSe4 by ICSD 97-004-2505. Li2S is a neutral endpoint species; report the chosen spin multiplicity. The physical scope is periodic slabs made from those records with an intact adsorbed Li2S initial state and a same-atom, same-charge adsorbed decomposition final state. The barrier is the maximum energy on the validated minimum-energy path minus the initial-state energy. The modeled system comprises the periodic host slab and adsorbate; do not add rGO, solvent or electrolyte, or infer macroscopic electrochemical performance. Justify and record the chosen surface, termination, software, functional and pathway.

# Required scientific validation/investigation

Propose plausible surface terminations, adsorption placements, decomposition products and paths within a declared low-index and chemical-identity boundary. Generate a finite candidate set, deduplicate equivalent candidates, and state how candidates advance or are rejected. Relax and validate every primary endpoint for stoichiometry, charge, surface identity, convergence and stability. Validate each retained path by reporting endpoint energies, image count, path convergence, maximum-energy image and any alternative path tested. Completion requires two host-specific primary barriers plus coverage and a conclusion that distinguishes robust ordering from model-dependent uncertainty. Stop when the declared candidate set is exhausted, or report bounded failure with attempted candidates and the unresolved scientific stage; do not manufacture a discovery narrative from an incomplete search.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include the independent hypothesis space, candidate and path records, validated barriers in eV, ordering/difference, mechanistic conclusion, limitations and completion status. A bounded-failure branch is valid only if it preserves the attempted-candidate and evidence fields needed to assess what was actually investigated.
