# Scientific objective

Characterize how NIR-IND's conformational freedom in glycerol affects its lowest strong singlet absorption and electronic transition character. Independently generate and discriminate plausible conformers within the public torsional boundary, identify a validated absorption endpoint, and assess its relationship to the measured glycerol absorption maximum of 631 nm. Generate and test your own explanations for the relationship between conformation and electronic transition character.

# Public inputs and scientific boundaries

The public file `data/inputs/nir_ind_identity.json` defines NIR-IND as the singly charged C24H29N2+ hemicyanine cation with the supplied isomeric SMILES, singlet multiplicity, and glycerol as the implicit solvent. The searchable conformational boundary is the donor–acceptor dihedral between the mean planes of the 4-(dimethylamino)phenyl donor ring and indole acceptor ring, with 0° and 90° as mandatory starting families; additional angles or stereoisomeric variants are allowed only when explicitly defined and covered in the report. Report the signed angle convention and actual optimized values. The measured glycerol absorption maximum, 631 nm, is the public experimental comparison endpoint. Choose and disclose your own software, electronic-structure model, solvation treatment and numerical settings. Use this instruction and the supplied molecular identity as the scientific inputs; model the cation in implicit glycerol.

# Required scientific validation/investigation

Propose a finite candidate-generation strategy covering both mandatory torsional families and any additional candidates you claim are needed. Record candidate identity, starting torsion, optimized torsion, connectivity, and deduplication rationale. Advance candidates only after a true-minimum check (frequency analysis or a scientifically justified equivalent), and report failed candidates and diagnostics. For each retained candidate, calculate singlet vertical excitations, identify the state used as the absorption endpoint, oscillator strength, wavelength, and leading orbital/configuration contribution. Compare the selected endpoint or ensemble of endpoints with 631 nm and distinguish computed evidence from interpretation. Completion requires documented coverage of both mandatory families, validated state-resolved results, and a stopping rule grounded in candidate-family exhaustion or a reproducible method/resource limitation. If completion is blocked, submit the bounded-failure branch with all attempted candidates, diagnostics, coverage and the scientifically meaningful limitation.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include the proposed search strategy, candidate and validation records, excitation records, selected endpoint, quantitative deviation from 631 nm, your independently reasoned mechanistic/electronic conclusion, and limitations.
