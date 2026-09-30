# Source scope audit

{
  "paper_id": "paper_746e066c163800d8",
  "source_documents": [
    {
      "role": "main",
      "path": "papers/paper_746e066c163800d8/documents/main.pdf",
      "sha256": "2f0a280dbcadb2f19ed3222e4419f69854743c7440e834b3137b27c323643570",
      "material_type": "primary_article",
      "pdf_pages_1_based": [
        2,
        3
      ],
      "sections_figures_tables": "PDF p2 Fig.1 defines the helicene series; pp2–3 give geometry/response methodology and p3 equations15–18 define HRS and orientational averages."
    },
    {
      "role": "si",
      "path": "papers/paper_746e066c163800d8/documents/supplementary_001.pdf",
      "sha256": "6c9e2983aa14070df612bb3a6f6ca6a4c6d0394454f93d076a6b091e625d7403",
      "material_type": "actual_supporting_information",
      "pdf_pages_1_based": [
        16,
        26,
        37,
        40,
        41,
        42,
        43,
        44,
        45,
        46,
        47,
        48
      ],
      "sections_figures_tables": "PDF p16 TableS2 geometric definitions; p26 method comparison; p37 TableS9 functional sensitivity; pp40–48 full coordinate entries for the chosen structures."
    }
  ],
  "source_scope": "A four-member subset of the source computational helicene study, restricted to static molecular HRS and its structural interpretation. The source also treats optical/transport/dynamic properties, which are not required here.",
  "objective_source_mapping": {
    "main": "PDF p2 Fig.1 defines the helicene series; pp2–3 give geometry/response methodology and p3 equations15–18 define HRS and orientational averages.",
    "si": "PDF p16 TableS2 geometric definitions; p26 method comparison; p37 TableS9 functional sensitivity; pp40–48 full coordinate entries for the chosen structures."
  },
  "facts_and_constraints": [
    "The four objects differ in their carbon skeleton; their response ordering is not supplied as an experimental fact.",
    "The defined quantity is the molecular response under isotropic orientational averaging in the static limit."
  ],
  "identity_provenance": "The full molecular graphs correspond to main Fig.1 and SI Cartesian-coordinate entries for compounds 1,3,5,7; source coordinates were used privately to transcribe topology, not supplied as optimized answers.",
  "decisions_open": [
    "Select physically relevant geometries/models and the response method.",
    "Decide which structural features or other explanations deserve testing and choose discriminating evidence.",
    "Choose how much numerical/model validation is needed to support the observed ordering or a limited conclusion."
  ],
  "removed_v1_requirements": [
    "Remove the fixed 1→3 and5→7 attribution panels, preset common-core torsions, mandatory charge-transfer diagnostic and field-step count.",
    "Keep HRS definition and static frequency as the scientific observable, not as a prescribed computational algorithm."
  ],
  "out_of_scope": "Study the four complete supplied helicene identities as neutral singlet molecules in the gas-phase static limit (ω=0). This is a molecular response question: finite-frequency spectra, the other source derivatives, intermolecular packing and bulk device performance are outside the required scope. The graphs define connectivity and do not prescribe a geometry or response ordering. Any representation change must be justified against the complete source identities.",
  "feasibility": "Real source-level Gaussian opt/frequency and response artifacts exist for these identities, including a failed-attempt record and independent tensor analysis. A first future reference audit can reparse these artifacts, verify tensor conventions and review the supported scope. Gaussian/ORCA native routes and Python response processing are potential resources after checking installed capability. No new science was launched.",
  "limitations": "Existing validation covers an author-informed limited method/geometry route, not all admissible alternative explanations or correlated accuracy. Existing interventions do not uniquely identify a mechanism. V2 semantic calibration and private-file isolation remain pending.",
  "source_scope_verified": true,
  "review_type": "Local relevant primary-text/figure review with explicit page mapping; no new scientific calculation."
}
