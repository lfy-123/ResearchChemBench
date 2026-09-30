# Source scope audit

{
  "paper_id": "paper_46f6118697c6397c",
  "source_documents": [
    {
      "role": "main",
      "path": "papers/paper_46f6118697c6397c/documents/main.pdf",
      "sha256": "4633e67606dc23badd9f553b89ec95d96540bd4fa637876897ae830a4e31901c",
      "material_type": "primary_article",
      "pdf_pages_1_based": [
        2,
        3,
        4
      ],
      "sections_figures_tables": "PDF p2 Scheme1 and Fig.2 establish substitutions; Table1/Fig.3 report solution spectra; p3 reports compound2 solvent observations; pp3–4 give DFT/TD interpretation."
    },
    {
      "role": "si",
      "path": "papers/paper_46f6118697c6397c/documents/supplementary_001.pdf",
      "sha256": "d25723e53953f2a507b014af89f62abe1f1c229886d0090fd80943b24dd21cfa",
      "material_type": "actual_supporting_information",
      "pdf_pages_1_based": [
        10,
        14,
        16
      ],
      "sections_figures_tables": "PDF p10 crystallographic provenance; p14 absorption data; p16 computational details specify DFT-D3BJ and begin TD tables."
    }
  ],
  "source_scope": "Four source B2N6 molecules and their solution absorption, within the source structure/optics investigation. Competing molecular explanations remain open; fixed-core intervention is not a source requirement.",
  "objective_source_mapping": {
    "main": "PDF p2 Scheme1 and Fig.2 establish substitutions; Table1/Fig.3 report solution spectra; p3 reports compound2 solvent observations; pp3–4 give DFT/TD interpretation.",
    "si": "PDF p10 crystallographic provenance; p14 absorption data; p16 computational details specify DFT-D3BJ and begin TD tables."
  },
  "facts_and_constraints": [
    "Absorption maxima are wavelengths of the largest measured molar absorption coefficient, not prescribed TD root numbers.",
    "Compound2 absorption showed no significant change across the source solvent series; the source does not supply a numerical detection threshold for that statement."
  ],
  "identity_provenance": "Main Scheme1 and Fig.2, SI synthetic/crystallographic records and privately inspected source CIF/topology establish the complete B2N6 derivative identities. The public mapped graphs carry connectivity, not author optimized coordinates.",
  "decisions_open": [
    "Select the molecular and solvent models that can address the measured spectra.",
    "Choose the state/structure evidence and any comparisons needed to explain substituent-associated differences.",
    "Determine how source ambiguities, model approximations or solution alternatives limit attribution."
  ],
  "removed_v1_requirements": [
    "Remove mandatory relaxed/common-core matrix, preassigned N6 orbital fractions and fixed effect-partition formula.",
    "Keep the covalent OTf identity and experimental spectra; do not silently simplify compound2 to free counterions."
  ],
  "out_of_scope": "Use the four complete supplied neutral singlet molecular identities and dichloromethane absorption observations. Compound2 contains four covalently attached B–O–SO2CF3 groups; it is not a bare B2N6 ion accompanied by four free triflate counterions. Any alternative model of solution composition must be explicitly justified and balanced. Restrict conclusions to molecular solution absorption. Solid-state emission, electrochemical decomposition and device performance are not required endpoints.",
  "feasibility": "The source explicitly reports Gaussian DFT/TD calculations for all four and supplies complete molecular structures. Registered Gaussian/ORCA native spectroscopy and Python analysis provide plausible routes after capability inspection. Future reference work can first reconcile source main/SI numbers and reparse matching raw legacy outputs; novel claim-specific evidence remains separately pending.",
  "limitations": "Source main/SI excitation values and dispersion labels differ; neither alone calibrates model error. No instrument threshold for solvent-insensitivity is given. The open explanation has not been independently scientifically or semantically calibrated, and runtime isolation remains pending.",
  "source_scope_verified": true,
  "review_type": "Local relevant primary-text/figure review with explicit page mapping; no new scientific calculation."
}
