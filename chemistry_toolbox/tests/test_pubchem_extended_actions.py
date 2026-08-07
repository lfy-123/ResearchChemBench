from __future__ import annotations

import sys
from types import SimpleNamespace

from chemistry_toolbox.src.backends import data


class _FakeResponse:
    def __init__(self, payload):
        self._payload = payload
        self.content = b"{}"

    def raise_for_status(self):
        return None

    def json(self):
        return self._payload


def _compound(cid: int = 2244):
    return SimpleNamespace(
        cid=cid,
        canonical_smiles="CC(=O)OC1=CC=CC=C1C(=O)O",
        isomeric_smiles="CC(=O)Oc1ccccc1C(=O)O",
        inchi="InChI=1S/C9H8O4",
        inchikey="BSYNRYMUTXBXSQ-UHFFFAOYSA-N",
        molecular_formula="C9H8O4",
        molecular_weight=180.16,
        iupac_name="2-acetyloxybenzoic acid",
        xlogp=1.2,
        tpsa=63.6,
        charge=0,
        complexity=212.0,
        h_bond_donor_count=1,
        h_bond_acceptor_count=4,
        rotatable_bond_count=3,
    )


def test_pubchem_identity_and_property_actions(monkeypatch):
    monkeypatch.setitem(
        sys.modules,
        "pubchempy",
        SimpleNamespace(get_compounds=lambda *_args, **_kwargs: [_compound()]),
    )
    identity = data.execute(
        "resolve_chemical_identity",
        "pubchem",
        {
            "inputs": {"query": {"identifier": "aspirin", "namespace": "name"}},
            "method_spec": {},
            "action_settings": {"require_unique": True, "max_records": 5},
        },
    )
    assert identity["status"] == "success"
    assert identity["result"]["identity"]["cid"] == 2244

    properties = data.execute(
        "retrieve_compound_properties",
        "pubchem",
        {
            "inputs": {"query": {"identifier": "2244", "namespace": "cid"}},
            "method_spec": {},
            "action_settings": {"properties": ["cid", "molecular_formula", "xlogp"], "max_records": 1},
        },
    )
    assert properties["status"] == "success"
    assert properties["result"]["records"] == [
        {"cid": 2244, "molecular_formula": "C9H8O4", "xlogp": 1.2}
    ]


def test_pubchem_similarity_and_substructure_searches_are_bounded(monkeypatch):
    captured = []

    def fake_get(url, **kwargs):
        captured.append((url, kwargs))
        return _FakeResponse({"IdentifierList": {"CID": [1, 2, 3]}})

    monkeypatch.setattr(data.httpx, "get", fake_get)
    similar = data.execute(
        "search_similar_compounds",
        "pubchem",
        {
            "inputs": {"query": {"identifier": "CCO", "namespace": "smiles"}},
            "method_spec": {},
            "action_settings": {"threshold": 90, "max_records": 3, "timeout_seconds": 10},
        },
    )
    assert similar["status"] == "success"
    assert similar["result"]["count"] == 3
    assert "fastsimilarity_2d/smiles/CCO/cids/JSON" in captured[0][0]
    assert captured[0][1]["params"]["MaxRecords"] == 3

    substructures = data.execute(
        "search_substructures",
        "pubchem",
        {
            "inputs": {"query": {"identifier": "c1ccccc1", "namespace": "smarts"}},
            "method_spec": {},
            "action_settings": {
                "max_records": 2,
                "match_stereo": False,
                "match_charges": False,
                "match_isotopes": False,
                "timeout_seconds": 10,
            },
        },
    )
    assert substructures["status"] == "success"
    assert "fastsubstructure/smarts/c1ccccc1/cids/JSON" in captured[1][0]
    assert captured[1][1]["params"]["Stereo"] == "ignore"


def test_pubchem_structure_retrieval_preserves_agent_coordinate_and_hydrogen_choices(monkeypatch):
    compound = SimpleNamespace(
        cid=702,
        charge=0,
        smiles="CCO",
        record={
            "atoms": {"aid": [1, 2, 3, 4], "element": [6, 6, 8, 1]},
            "bonds": {
                "aid1": [1, 2, 3],
                "aid2": [2, 3, 4],
                "order": [1, 1, 1],
            },
            "coords": [
                {
                    "aid": [1, 2, 3, 4],
                    "conformers": [
                        {
                            "x": [0.0, 1.5, 2.1, 2.8],
                            "y": [0.0, 0.0, 1.2, 1.2],
                            "z": [0.0, 0.1, -0.2, -0.3],
                        }
                    ],
                }
            ],
        },
    )
    captured = {}

    def fake_get_compounds(identifier, namespace, **kwargs):
        captured.update(identifier=identifier, namespace=namespace, kwargs=kwargs)
        return [compound]

    monkeypatch.setitem(
        sys.modules,
        "pubchempy",
        SimpleNamespace(get_compounds=fake_get_compounds),
    )
    result = data.execute(
        "retrieve_compound_structure",
        "pubchem",
        {
            "inputs": {"query": {"identifier": "702", "namespace": "cid"}},
            "method_spec": {},
            "action_settings": {
                "record_type": "3d",
                "hydrogen_policy": "omit",
                "max_records": 1,
                "require_unique": True,
            },
        },
    )
    assert result["status"] == "success"
    assert captured["kwargs"] == {"record_type": "3d"}
    structure = result["result"]["structures"][0]["structure"]
    assert [atom["element"] for atom in structure["atoms"]] == ["C", "C", "O"]
    assert structure["bonds"] == [
        {"atom_id_a": 1, "atom_id_b": 2, "order": 1},
        {"atom_id_a": 2, "atom_id_b": 3, "order": 1},
    ]
