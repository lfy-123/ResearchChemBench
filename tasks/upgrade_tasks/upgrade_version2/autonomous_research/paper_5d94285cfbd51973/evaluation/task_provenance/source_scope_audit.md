# Source scope audit

{
  "paper_id": "paper_5d94285cfbd51973",
  "source_documents": [
    {
      "role": "main",
      "path": "papers/paper_5d94285cfbd51973/documents/main.pdf",
      "sha256": "9a4125a542a33af7128c39ebcf9df93cbe82923038415ed18e81bc77ca65e1a2",
      "material_type": "primary_article",
      "pdf_pages_1_based": [
        2,
        3,
        4,
        5,
        6,
        7
      ],
      "sections_figures_tables": "PDF pp2–3 synthesis/assay and SAR; pp4–7 DFT/frontier/MEP interpretation and its biological claims."
    },
    {
      "role": "si",
      "path": "papers/paper_5d94285cfbd51973/documents/supplementary_001.pdf",
      "sha256": "9c09e4819df88ab73a3551dca09e2c5b390e7a783dac0df4f633e06e5e227f0e",
      "material_type": "actual_supporting_information",
      "pdf_pages_1_based": [
        2,
        3,
        4,
        5,
        6,
        7,
        31,
        32,
        33,
        34,
        35,
        36,
        37,
        38,
        39,
        40,
        41,
        42
      ],
      "sections_figures_tables": "PDF pp3–7 identities; p31 TableS1 exact C.albicans column; pp31–40 source gas-phase coordinates; p41 TableS12 all-ten descriptors and printed formulas; p42 TableS13 calculated physicochemical properties."
    }
  ],
  "source_scope": "A bounded molecular-property/observed-activity subproblem in the source ten-compound study. Source docking and pharmacokinetic claims are background, not endpoints to reproduce or proof of the molecular-property relation.",
  "objective_source_mapping": {
    "main": "PDF pp2–3 synthesis/assay and SAR; pp4–7 DFT/frontier/MEP interpretation and its biological claims.",
    "si": "PDF pp3–7 identities; p31 TableS1 exact C.albicans column; pp31–40 source gas-phase coordinates; p41 TableS12 all-ten descriptors and printed formulas; p42 TableS13 calculated physicochemical properties."
  },
  "facts_and_constraints": [
    "There are ten compounds and three printed MIC levels in this single organism column.",
    "Individual assay replicates, standard deviations and a strain accession are not specified in the inspected TableS1/method record.",
    "No censoring symbol is printed beside the reported MIC values; do not silently convert1000 to >1000 or create a lower concentration endpoint."
  ],
  "identity_provenance": "Source main Scheme1 and SI pp3–7 chemical names/characterization establish the ten complete derivative graphs; SI pp31–40 supplies source optimized structures privately. No source descriptor value or activity-derived winner label is embedded in the public graphs.",
  "decisions_open": [
    "Choose molecular properties/models and a testable relationship to the reported activity.",
    "Choose statistical or comparative evidence that can distinguish a meaningful relationship from the limited sample structure.",
    "Decide whether the data support prediction, only descriptive association, or no reliable relationship, and revise claims accordingly."
  ],
  "removed_v1_requirements": [
    "Remove mandatory two-feature electronic model, fixed baseline features, ridge hyperparameter, LOOCV and permutation counts.",
    "Remove predefined ordinal bins and derived endpoint intervals; retain printed MIC values and finite-resolution limitations.",
    "Correct false implication that the authors studied onlyAZ9 and explicitly audit source descriptor formulas."
  ],
  "out_of_scope": "The available sample consists of the ten complete azetidine–pyridazine derivatives and one C. albicans MIC column from the source assay. The supplied neutral singlet graphs define the molecules; any additional state/environment approximation must be justified. Restrict biological conclusions to this assay and sample. Neither a molecular property nor an association in ten compounds proves a target-binding mechanism, cell permeability, clinical efficacy or general antimicrobial activity. Other organisms, docking targets and new analogue design are outside the required question.",
  "feasibility": "Ten chemically explicit graphs and an actual assay column suffice for a bounded computational/statistical investigation; a source gas-phase DFT route and cheaper graph-derived analyses are feasible options, depending on the claim. The toolbox provides Gaussian/ORCA/native routes and Python analysis after capability inspection. A future reference review can first audit source descriptor arithmetic and matching raw legacy outputs without launching new science.",
  "limitations": "No new all-ten quantum or statistical reference was produced. MIC replicate distributions/strain accession are absent in inspected records; the sample cannot establish broad predictive or causal biology. Source descriptor errors limit literal reuse. V2 judge calibration and environment isolation remain pending.",
  "source_scope_verified": true,
  "review_type": "Local relevant primary-text/figure review with explicit page mapping; no new scientific calculation."
}
