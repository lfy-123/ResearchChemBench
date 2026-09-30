# Source scope audit

{
  "paper_id": "paper_0a62b797f51de2c0",
  "source_documents": [
    {
      "role": "main",
      "path": "papers/paper_0a62b797f51de2c0/documents/main.pdf",
      "sha256": "8faf62fe4d34371ac12d6c414dec1a19ecd0a08656bd4a9d692b3d0dd08f3b4a",
      "material_type": "primary_article",
      "pdf_pages_1_based": [
        2,
        4,
        5
      ],
      "sections_figures_tables": "PDF p2 Scheme1c visually inspected for backbone and cyano positions; p4 Fig.2 photophysical observations; p5 Fig.3a specifies three repeats and discusses molecular charge descriptors versus material observations."
    },
    {
      "role": "si",
      "path": "papers/paper_0a62b797f51de2c0/documents/supplementary_001.pdf",
      "sha256": "cec193840ebff26c59e3ce19abee827e02a953fafc2b62ce34761586a0039b8d",
      "material_type": "actual_supporting_information",
      "pdf_pages_1_based": [
        6
      ],
      "sections_figures_tables": "PDF p6 computational details: B3LYP geometry, CAM-B3LYP dipoles, Multiwfn/VMD ESP; no source recipe for a length-holdout or regioisomer intervention."
    }
  ],
  "source_scope": "A molecular-model subset of the source cyano-functionalized conjugated-polymer study. Three source substitution patterns and finite fragments are retained; full polymer photocatalysis, synthesis and novel regioisomer design are excluded.",
  "objective_source_mapping": {
    "main": "PDF p2 Scheme1c visually inspected for backbone and cyano positions; p4 Fig.2 photophysical observations; p5 Fig.3a specifies three repeats and discusses molecular charge descriptors versus material observations.",
    "si": "PDF p6 computational details: B3LYP geometry, CAM-B3LYP dipoles, Multiwfn/VMD ESP; no source recipe for a length-holdout or regioisomer intervention."
  },
  "facts_and_constraints": [
    "All three backbones have alternating para-phenylene/2,5-thiophene connectivity. Nitrile substitutions occupy the available thiophene beta positions as shown in the graphs.",
    "The source molecular study represents the polymer by three-repeat fragments; actual material morphology and end-group distributions are not encoded here.",
    "Material PL observations are contextual and occur at a different scale from isolated molecular descriptors."
  ],
  "identity_provenance": "Source main Scheme1c and synthesis pp2–3 specify para-phenylene/2,5-thiophene with0,1,2 beta-cyano substituents; Fig.3a p5 explicitly discusses three-repeat molecular fragments. Supplied graphs are benchmark graph transcriptions with explicit H caps, not imported source optimized geometries.",
  "decisions_open": [
    "Choose a model and evidence that can distinguish meaningful substitution-dependent charge behaviour from representation artifacts.",
    "Decide which electronic or excited-state observables are needed for the proposed explanation.",
    "Allocate validation to consequential approximations and determine the molecular-to-material limit of the answer."
  ],
  "removed_v1_requirements": [
    "Remove mandatory n1/n2/n3 matrix, novel reversed-CN regioisomer, fixed45° torsions and n3 holdout.",
    "Remove prescribed ESP surface threshold and obligatory NTO centroid/overlap algorithm.",
    "Restore the actual source three-repeat molecular scope and identify H caps as modeling choices."
  ],
  "out_of_scope": "The source systems alternate para-phenylene and2,5-linked thiophene, with zero, one or two cyano groups on thiophene3/4 positions. The supplied neutral singlet graphs are explicit H-terminated three-repeat fragment encodings of the source Fig.3a molecular scope. They are not experimental polymer chains, measured end groups, or author optimized coordinates. Any changed representation must preserve a documented relationship to the source connectivity. Limit the scientific answer to the finite molecular contribution; solid-state transport, photocatalytic rates and yields cannot be inferred quantitatively from isolated molecular descriptors alone.",
  "feasibility": "The complete finite graph inputs are chemically explicit and the source reports a Gaussian geometry/dipole/ESP route for three-repeat structures. Registered Gaussian/ORCA and Python analysis may support agent-chosen molecular studies after checking software availability. First future reference work should verify graph/cap correspondence and reuse any matching raw artifacts before calculating missing fragment properties.",
  "limitations": "There is no new independently validated three-repeat response reference, no measured molecular end-group distribution, and no calibrated conversion from molecular descriptors to bulk charge dynamics. The public lifetimes lack raw decay/error data and are contextual. Semantic calibration and runtime isolation remain pending.",
  "source_scope_verified": true,
  "review_type": "Local relevant primary-text/figure review with explicit page mapping; no new scientific calculation."
}
