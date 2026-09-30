# Source scope audit

{
  "paper_id": "paper_9d091f4337662e78",
  "source_documents": [
    {
      "role": "main",
      "path": "papers/paper_9d091f4337662e78/documents/main.pdf",
      "sha256": "77662fc70c44424324935577c2f687f8dd7e380d928c34d07550ffaa7f64e2db",
      "material_type": "primary_article",
      "pdf_pages_1_based": [
        3,
        4,
        6,
        7
      ],
      "sections_figures_tables": "PDF pp3–4 structure elucidation and Figure2 compound1 experimental black ECD trace; p6 experimental compound1 data; p7 full ECD computational method."
    },
    {
      "role": "si",
      "path": "papers/paper_9d091f4337662e78/documents/supplementary_001.pdf",
      "sha256": "48e92302a3a0bbc6b0ed8d6db613911ea165365d2a2b5f87ac35fbd4954f0cfc",
      "material_type": "actual_supporting_information",
      "pdf_pages_1_based": [
        5
      ],
      "sections_figures_tables": "PDF p5 TableS1 lists16 computed conformers and source populations; it is private evidence for ensemble complexity, not public starting structures."
    }
  ],
  "source_scope": "A configurational assignment problem for only compound1, using known constitution and methanol ECD. The source assigned this centre by a computed/experimental spectral comparison; the new question permits evidence-supported ambiguity.",
  "objective_source_mapping": {
    "main": "PDF pp3–4 structure elucidation and Figure2 compound1 experimental black ECD trace; p6 experimental compound1 data; p7 full ECD computational method.",
    "si": "PDF p5 TableS1 lists16 computed conformers and source populations; it is private evidence for ensemble complexity, not public starting structures."
  },
  "facts_and_constraints": [
    "ECD was measured in methanol. The input contains93 digitized points from the black experimental curve, with plot-reading bounds.",
    "All supplied wavelengths are available at task start; no spectral band is a hidden prospective test.",
    "The compound constitution and alkene geometry are given, whereas atom17 absolute configuration remains the scientific target."
  ],
  "identity_provenance": "Main compound1 structure and Fig.1 establish constitution and E alkene; the unresolved centre is map17. Absolute labels and author conformer coordinates are excluded from public identity.",
  "decisions_open": [
    "Decide how to generate and evaluate stereochemical/conformational models without supplied author geometries.",
    "Choose how to connect computed or other physically justified evidence to the experimental ECD and quantify discrimination.",
    "Decide whether the sampled models and data support one assignment, an unresolved set or a narrower conclusion."
  ],
  "removed_v1_requirements": [
    "Remove R/S candidate enumeration and mandatory independently searched pair from the public input.",
    "Remove fixed qRRHO cutoffs, broadening widths, no-shift algorithm and spectral held-out partition.",
    "Retain the unassigned centre and E alkene as necessary identity facts; no author S label appears in AR."
  ],
  "out_of_scope": "Study compound 1 with its supplied constitution, known E alkene and one unresolved absolute stereocentre at atom map17. The neutral molecular identity has formula C24H24N2O4 and singlet multiplicity. Methanol is the ECD medium. The source experimental trace is approximate digitized data; it is not a calculated answer. Other natural products, synthesis and biological activity are outside this task. Any molecular model or stereochemical change must be related explicitly to this constitution.",
  "feasibility": "The source demonstrates a molecular conformer/TD-ECD route and the toolbox exposes native Gaussian/ORCA plus graph/Python workflows; optional sampling software must be checked in the actual tool catalog. First reuse checks can inspect known constitution, the93-point extraction and historical molecular outputs. Future expanded scientific work would need evidence sufficient for whichever representation/spectral strategy is chosen, without a mandated dual-search matrix.",
  "limitations": "No new full conformational or spectral reference has been calculated. Digitized experimental data have finite precision and lack original instrumental uncertainties. Source gas-phase populations/solution TD are model-dependent. V2 semantic judge calibration and execution isolation remain pending.",
  "source_scope_verified": true,
  "review_type": "Local relevant primary-text/figure review with explicit page mapping; no new scientific calculation."
}
