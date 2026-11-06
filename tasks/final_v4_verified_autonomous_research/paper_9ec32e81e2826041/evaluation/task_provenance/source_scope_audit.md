# Source and scope audit

{
  "paper_id": "paper_9ec32e81e2826041",
  "batch": 1,
  "source_documents": [
    {
      "path": "papers/paper_9ec32e81e2826041/documents/main.pdf",
      "sha256": "c494b9ed5388f0c6d968d8e80ce851426473aa9779a3c3930927445340195dec",
      "matches_audit": true,
      "declared_pages": 9,
      "material_type": "main_article",
      "pdf_pages_read_1_based": [
        3,
        4,
        5
      ]
    },
    {
      "path": "papers/paper_9ec32e81e2826041/documents/supplementary_001.pdf",
      "sha256": "dbb8ec5153da3d86acde2fd320f01cc1bae86bf16cebf2fd2cf835280933d7cb",
      "matches_audit": true,
      "declared_pages": 23,
      "material_type": "true_supporting_information",
      "pdf_pages_read_1_based": [
        3,
        4,
        13,
        14,
        15,
        16,
        21,
        22
      ]
    }
  ],
  "source_scope": {
    "objects": "One full80-atom neutral singlet Z-cAACCy, C35H43NZn; not Z-SIP or Z-IP.",
    "observations": "Main p3 different colorless/yellow crystals: diffuse-reflectance onset about430nm and visible band extending about500nm respectively. Main p4 both give same yellow solution.",
    "molecular_question": "Configuration/stability and absorption with possible Zn electronic involvement; distinct thermodynamic and optical claims need their own evidence.",
    "boundary": "Isolated molecular ground-state and vertical optical interpretation; experimental crystalline edge is not identical to an isolated transition. No crystal populations, full packing, phosphorescence/SOC/lifetimes or Z-IP photocatalysis."
  },
  "source_mapping": [
    {
      "kind": "experimental_facts",
      "source": "main p3 Figure1 diffuse reflectance; main p4 dissolution/NMR",
      "use": "Public color/onset/dissolution contrast; no crystal angles or causal orbital labels supplied."
    },
    {
      "kind": "identity",
      "source": "SI TablesS1–S2 pp13–15, corroborated by main Figure1 and old native graph maps",
      "use": "Complete neutral atom/bond graph; no coordinates. Independent distance-based adjacency matches archived native graph for both differently ordered structures; graphs were checked isomorphic."
    },
    {
      "kind": "author_geometry_and_orbital_interpretation",
      "source": "main pp3–5 Figures1–4",
      "use": "Private/PR83.1/23.9deg, coplanarity/C–Zn-p orbital and2.1/8.5%Zn4p interpretation."
    },
    {
      "kind": "source_protocol",
      "source": "SI p3 methods; p21 TablesS7–S9",
      "use": "PR PBE0/6-311+G** with/withoutD3BJ,300K and five singlet TD states; no assertion of universal correctness."
    },
    {
      "kind": "out_of_scope_source_work",
      "source": "SI p3 and p22 tripletZ-IP",
      "use": "Explicitly excludes importing Z-IP SOC or emission result to Z-cAACCy."
    },
    {
      "kind": "benchmark_extension",
      "source": "V1 partial follow-on designs and this plan",
      "use": "Matched cross-geometry energies/detailed decomposition are optional claim-specific diagnostics, not hidden requirements."
    }
  ],
  "agent_decisions": [
    "Generate configurations and choose what stability question is necessary for the optical interpretation without two supplied geometry families.",
    "Choose the electronic-response method and evidence needed to quantify, challenge or reject a Zn-role claim.",
    "Choose how to study any energetic or optical cause; no obligatory dispersion switch, fixed cross-energy grid or root count.",
    "Decide which differences are molecular and which remain confounded by experimental solid/solution environments."
  ],
  "limitations": [
    "V1 science status remains needs_work; there is no full reference binding or final accepted optical/stability matrix.",
    "Public graph supplies identity without source conformations; independent end-to-end AR construction/search feasibility has not been tested.",
    "The public optical data are approximate and lack digitized spectra/packing.",
    "Actual judge calibration, new-route reference completion and filesystem isolation remain pending; no new science jobs run."
  ],
  "baseline_packages": [
    {
      "mode": "autonomous_research",
      "path": "tasks/upgrade_tasks/upgrade_version1/autonomous_research/paper_9ec32e81e2826041",
      "package_content_sha256": "93da91ffecd20507ed9ed401900d1401a874c7025048e5ae410b18632e964ba1",
      "manifest_sha256": "9cb7daf37b52c5c1cf6971e5afe0c88249dc9b88b2efc3135a10001c1e0a83be"
    },
    {
      "mode": "paper_reproduction",
      "path": "tasks/upgrade_tasks/upgrade_version1/paper_reproduction/paper_9ec32e81e2826041",
      "package_content_sha256": "f7647ee76fd803c1764c6a202e83cf11dfd02bded21d41ce78b2ee3f9ab906a0",
      "manifest_sha256": "3baf628321ec54a31151d7e934464a3bed7b5e877e200fa25506af54b0373bf3"
    }
  ],
  "old_classification": {
    "original": "A",
    "v1": "B",
    "openness_target": "user_defined_C_open_research_not_historical_category_relabel"
  }
}
