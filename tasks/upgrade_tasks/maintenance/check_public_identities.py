"""Parent audit of public mapped molecular identities, without geometry jobs."""
from __future__ import annotations
import argparse
from collections import Counter
import json
from pathlib import Path
import re
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

ROOT = Path(__file__).resolve().parents[3]
DEST = ROOT / 'tasks/upgrade_tasks'
COORD = DEST / 'coordination_20260927'


def formula_atoms(formula):
    if not isinstance(formula, str) or not re.fullmatch(r'(?:[A-Z][a-z]?\d*)+(?:[+-]\d*)?', formula):
        return None
    result = Counter()
    for element, count in re.findall(r'([A-Z][a-z]?)(\d*)', formula):
        result[element] += int(count or 1)
    return result


def inspect(pids):
    results = []
    def scan(node, file, location):
        if isinstance(node, dict):
            value = node.get('mapped_smiles')
            if isinstance(value, str):
                row = {'file': str(file.relative_to(ROOT)), 'location': location, 'id': node.get('id', node.get('system_id')), 'failures': []}
                params = Chem.SmilesParserParams()
                params.removeHs = False
                mol = Chem.MolFromSmiles(value, params)
                if mol is None:
                    row['failures'].append('Mapped SMILES does not parse/sanitize')
                else:
                    maps = [a.GetAtomMapNum() for a in mol.GetAtoms()]
                    if not all(maps) or len(maps) != len(set(maps)):
                        row['failures'].append('Atom maps absent, zero or duplicated')
                    actual = rdMolDescriptors.CalcMolFormula(mol)
                    row.update(computed_formula=actual, atom_count=mol.GetNumAtoms(), formal_charge=Chem.GetFormalCharge(mol))
                    wanted = formula_atoms(node.get('formula'))
                    if wanted is not None and wanted != formula_atoms(actual):
                        row['failures'].append('Formula mismatch: declared ' + node['formula'])
                    charge = node.get('charge', node.get('formal_charge'))
                    if isinstance(charge, int) and charge != Chem.GetFormalCharge(mol):
                        row['failures'].append(f'Charge mismatch: declared {charge}')
                    row['note'] = 'Checks graph parse, formula, charge and map uniqueness only; not stereochemical source equivalence or minimum stability.'
                results.append(row)
            for key, value in node.items():
                scan(value, file, location + '/' + str(key))
        elif isinstance(node, list):
            for index, value in enumerate(node):
                scan(value, file, location + '/' + str(index))
    for pid in pids:
        public = DEST / 'autonomous_research' / pid / 'agent_input/data'
        for file in public.rglob('*.json'):
            try:
                scan(json.loads(file.read_text()), file, '')
            except (OSError, json.JSONDecodeError) as exc:
                results.append({'file': str(file.relative_to(ROOT)), 'failures': [repr(exc)]})
    failed = [r for r in results if r['failures']]
    return {'status': 'failed' if failed else 'passed', 'papers': len(pids), 'mapped_graphs': len(results), 'failed_graphs': len(failed), 'scientific_reference_validation': False, 'results': results}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--batch', type=int, action='append')
    parser.add_argument('--output', type=Path, default=COORD / 'parent_public_identity_report.json')
    args = parser.parse_args()
    spec = json.loads((ROOT / 'docs/evalution/update/upgrade_guidance_review_manifest_20260927.json').read_text())
    pids = [r['paper_id'] for r in spec['records'] if not args.batch or r['batch'] in args.batch]
    report = inspect(pids)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'results'}))
    for row in report['results']:
        if row['failures']:
            print(json.dumps(row, ensure_ascii=False))
    raise SystemExit(bool(report['failed_graphs']))
