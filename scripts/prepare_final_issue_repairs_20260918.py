"""Emit reviewed task repairs as apply_patch input; never write task files itself.

Scientific authority: docs/claude/final_tasks_issue_reconfirmation_and_scoring_analysis_20260918.md.
This is a one-time migration from its reviewed pre-repair state, not a chemistry run.
"""
from __future__ import annotations

import difflib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODES = ('autonomous_research', 'paper_reproduction')
changes: dict[Path, str] = {}


def path(mode, pid, relative):
    return ROOT / 'tasks' / ('final_verified_' + mode) / ('paper_' + pid) / relative


def get(p):
    return changes.get(p, p.read_text())


def replace(p, old, new, count=1):
    text = get(p)
    assert text.count(old) == count, (str(p), old, text.count(old), count)
    changes[p] = text.replace(old, new)


def add_boundary(p, text):
    replace(p, '# Required scientific validation/investigation', text + '\n\n# Required scientific validation/investigation')


def edit_json(p, fn):
    doc = json.loads(get(p))
    fn(doc)
    changes[p] = json.dumps(doc, ensure_ascii=False, indent=2) + '\n'


def main():
    p = path('paper_reproduction', '0dc85595cab7bc0a', 'agent_input/task.md')
    replace(p, 'These calculations should be interpreted alongside the exclusive dibenzo[a,o]picene product boundary while separating thermodynamic and electronic support from direct photochemical or kinetic proof.',
            'Use the calculated candidate comparisons to determine the supported channel and product selectivity, separating thermodynamic and electronic support from direct photochemical or kinetic proof.')

    for mode in MODES:
        p = path(mode, '6e09640463562644', 'agent_input/task.md')
        replace(p, 'Public experimental band positions and assignments are in', 'Public experimental band positions, units and neutral band labels are in')
        add_boundary(p, 'The band labels a-f are identifiers only, not assignments to an atomic group or shell. The input file retains its legacy filename but contains measured peak positions only. Determine mode identities from computed displacements and spectra; determine any change in ion-pair arrangement by comparing the full n=1-5 series, without assuming its onset.')
        bands = path(mode, '6e09640463562644', 'agent_input/data/inputs/experimental_band_assignments.json')
        def remove_assignments(doc):
            for b in doc['bands'].values():
                assert 'assignment' in b
                del b['assignment']
        edit_json(bands, remove_assignments)
        if mode == 'paper_reproduction':
            replace(p, 'The authors propose that sequential hydration retains a contact Ba–OH ion-pair arrangement for n=1–2, while growth of the water network initiates reorganization toward a solvent-shared ion-pair arrangement beginning at n=3.',
                    'The authors propose that growth of the hydration network can reorganize a contact Ba–OH ion-pair arrangement toward a solvent-shared arrangement. Test this candidate mechanism across the full hydration series and determine whether and where a transition is supported.')
            replace(p, 'with particular attention to competing n=3 structures representing nondissociated and Ba···OH-separated arrangements.',
                    'including competing nondissociated and Ba···OH-separated arrangements at each size where chemically meaningful.')
            replace(p, 'Compare at least the n=1–5 structural trend and the n=3 alternatives.',
                    'Compare the n=1–5 structural trend and the competing arrangements at each size.')

        p = path(mode, '1b285cf9f763f2cf', 'agent_input/task.md')
        replace(p, 'with explicit site, magnetic and finite-.', 'with explicit site assignments, magnetic states and geometry comparisons for the defined fixed cells.')
        if mode == 'paper_reproduction':
            replace(p, 'Compare the undoped UC-1 environment with the Li/F co-substituted UC-2 environment and the further Si-substituted UC-3 environment.',
                    'The source study compares an undoped host with Li/F and then Si substitutions. In this benchmark adaptation, compare the Fe-activated UC-1 baseline (without Li/F/Si co-substitution) with the Li/F co-substituted UC-2 and further Si-substituted UC-3, using the exact compositions below; UC-1 is not Fe-free.')
            replace(p, 'across plausible site and charge-compensation arrangements.',
                    'across plausible relative substitution sites within the fixed compositions and neutral-cell electronic-compensation convention specified below.')

        p = path(mode, '94e7481ded3b6a75', 'agent_input/task.md')
        if mode == 'autonomous_research':
            replace(p, 'without relying on an external paper or a preselected computational protocol.',
                    'using the public primary comparison protocol below without relying on an external paper.')
            replace(p, 'Choose and justify an executable method/software and report it exactly. No author route, candidate ranking, target value, or expected direction is supplied.',
                    'Independently plan the preparation, execution and analysis; choose executable software implementing the primary protocol and report it exactly. No author-specific candidate ranking, target value, or expected direction is supplied.')
        else:
            replace(p, 'while reporting.', 'with the method and spatial-analysis definition reported explicitly.')
            replace(p, 'You may choose the executable quantum-chemical method and software, but state them exactly and do not claim that a method-independent value was obtained.',
                    'You may choose software implementing the primary comparison protocol below and supplementary analysis methods; report them exactly. The primary absolute energies and thermochemistry are protocol-specific.')

        p = path(mode, '221aafe4bd916a11', 'agent_input/task.md')
        replace(p, 'at 298 K', 'at 298.15 K', count=2)
        add_boundary(p, 'Primary barrier definition: ΔG‡ = G(TS) - G(2a) - G(CO2), in kcal/mol, using the separately validated reactant species as the zero (not a preassociated complex). Use implicit acetonitrile and a consistent 298.15 K, 1 atm standard-pressure harmonic thermochemistry convention for every term. Report the electronic-energy level and thermal correction separately; if using higher-level single points, apply the same composite-energy definition to all species. A 1 M standard-state barrier or a barrier relative to a preassociated complex may be reported separately, with an explicit conversion to the primary definition. This definition does not prescribe a numerical barrier or a unique search method.')
        ref = path(mode, '221aafe4bd916a11', 'evaluation/verified_computation_reference.md')
        replace(ref, '"geometry_or_source": "SI-recovered candidate; managed Gaussian evidence under artifacts/gaussian_batch/TS2_2a_si_recovered_ts_optfreq_summary.json",',
                    '"geometry_or_source": "SI-recovered TS optimization followed by successful standalone frequency calculation; frequency/Gibbs evidence: artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_standalone_freq_repair_hpc20/stdout.log (the early optfreq summary alone does not contain complete frequencies)",')
        replace(ref, '## Successful calculation chain', '## Selected barrier convention (clarified 2026-09-18)\n\nThe archived 19.8719700 kcal/mol branch uses G(TS) = -2324.733530 Eh from the successful standalone frequency output, G(2a) = -2136.233723 Eh from `artifacts/gaussian_batch/2a_reactant_optfreq/stdout.log`, and G(CO2) = -188.531475 Eh from `artifacts/gaussian_batch/author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20/stdout.log`. Each raw thermochemistry block specifies 298.150 K and 1 atm. The barrier is their stoichiometric difference; no separate 1 M correction was applied. This historical low-basis verification branch is not the SI high-basis single-point composite route. No new calculation or scientific target change is asserted.\n\n## Successful calculation chain')

        p = path(mode, '98b6f8a0352f72c2', 'agent_input/task.md')
        add_boundary(p, 'Primary radiative-lifetime definition: tau_rad(s) = 1.4999 / (f * wavenumber_cm_inverse**2), where f is dimensionless and wavenumber_cm_inverse is the numerical S1 excitation wavenumber in cm^-1; tau_rad(ns) = 1e9 * tau_rad(s). Use the energy and oscillator strength of the same identified vertical transition. This is the oscillator-strength-derived radiative lifetime, not the total lifetime including nonradiative decay. Do not add a refractive-index or local-field multiplier to this primary conversion; any different lifetime convention is a separate supplementary quantity. The excitation calculation itself includes the specified chloroform continuum.')
        replace(p, 'Derive the lifetime with a stated equation and units.', 'Derive the lifetime using the primary equation and units defined above.')
        ref = path(mode, '98b6f8a0352f72c2', 'evaluation/verified_computation_reference.md')
        replace(ref, 'tau_s = 1.4999/(f * E_cm^-2), with E in cm^-1;', 'tau_s = 1.4999/(f * wavenumber_cm_inverse**2), with the wavenumber numerical value in cm^-1 (notation clarified; historical values unchanged);')

        p = path(mode, '3316e45a74258fb7', 'agent_input/task.md')
        replace(p, 'S0 is the optimized ground state; S1 and T1 are the lowest computed singlet and triplet excited states.',
                    'S0 is the optimized ground state; S1 and T1 are the lowest vertical singlet and triplet excitations evaluated at that same S0 geometry using the same electronic-structure level and environment. The primary ΔE_ST is their vertical energy difference, not the difference between separately relaxed excited-state minima.')
        replace(p, 'Compute and identify S1/T1 on a validated structure,', 'Compute and identify vertical S1/T1 on the same validated S0 structure,')

        p = path(mode, '988bc12ae3768679', 'agent_input/task.md')
        add_boundary(p, 'Result identity contract: use name="2a-acid" and name="2a-base", each exactly once in the structures array. Array order is arbitrary; all state tables and brightest-state selectors are matched by name, never by array position. Keep each record with its own charge, multiplicity and source geometry.')
        schema = path(mode, '988bc12ae3768679', 'agent_input/submission_schema.json')
        def identity_schema(doc):
            arr = doc['result_schema']['properties']['structures']
            arr['description'] = 'Exactly one 2a-acid and one 2a-base record; order is arbitrary and names identify objects.'
            arr['items']['properties']['name']['enum'] = ['2a-acid', '2a-base']
            arr['allOf'] = [{'contains': {'type': 'object', 'required': ['name'], 'properties': {'name': {'const': name}}}, 'minContains': 1, 'maxContains': 1} for name in ['2a-acid', '2a-base']]
        edit_json(schema, identity_schema)
        rules = path(mode, '988bc12ae3768679', 'evaluation/scoring_rules.json')
        def identity_rules(doc):
            for r in doc['rules']:
                if r['reference_id'].endswith('process_inputs'):
                    r['expected'] += ' Exactly one record named 2a-acid and one named 2a-base must be present; duplicates or unknown names do not establish coverage.'
                for suffix, name in [('result_acid', '2a-acid'), ('result_base', '2a-base')]:
                    if r['reference_id'].endswith(suffix):
                        r['binding']['fields'] = ['$.structures[*]']
                        r['binding']['comparison'] = 'match the complete structure record by its exact name, independent of array order; then compare state identity and values'
                        r['expected'] = f'Select only the structure record with name="{name}" (exactly one); never infer identity from array position. ' + r['expected']
        edit_json(rules, identity_rules)

        for pid, kp in [('d2d08c91f34da1cb', 'ar_result_physical_interpretation' if mode == MODES[0] else 'pr_result_state_shifts'), ('f9d09d28c7d9adaa', 'kp_ar_angle_beta1' if mode == MODES[0] else 'kp_pr_angle_beta1')]:
            def link(doc, kp=kp):
                assert len(doc['items']) == 1
                ids = doc['items'][0]['supporting_key_point_ids']
                assert kp not in ids
                ids.append(kp)
            edit_json(path(mode, pid, 'evaluation/reference_conclusions.json'), link)
        def dedup_final(doc):
            duplicate = 'c_' + mode + '_final_rule'
            redundant = next(r for r in doc['rules'] if r['rule_id'] == duplicate)
            assert any(r['rule_id'] != duplicate and {k:v for k,v in r.items() if k != 'rule_id'} == {k:v for k,v in redundant.items() if k != 'rule_id'} for r in doc['rules'])
            doc['rules'] = [r for r in doc['rules'] if r['rule_id'] != duplicate]
        edit_json(path(mode, 'f9d09d28c7d9adaa', 'evaluation/scoring_rules.json'), dedup_final)

    emit_patch()


def emit_patch():
    patch = ['*** Begin Patch']
    for p, new in sorted(changes.items()):
        old = p.read_text()
        if old == new:
            continue
        hunks = list(difflib.unified_diff(old.splitlines(keepends=True), new.splitlines(keepends=True), n=3))[2:]
        patch.append('*** Update File: ' + str(p.relative_to(ROOT)))
        for line in hunks:
            patch.append('@@' if line.startswith('@@') else line.rstrip('\n'))
    patch.append('*** End Patch')
    print(json.dumps({'files': [str(p.relative_to(ROOT)) for p in sorted(changes)], 'patch': '\n'.join(patch) + '\n'}))


def archive_patch():
    for mode in MODES:
        for p in sorted((ROOT / 'tasks' / ('final_verified_' + mode)).glob('paper_*/evaluation/verified_computation_reference.md')):
            text = p.read_text()
            stale = []
            for label, fn, key in [('Conclusion', 'reference_conclusions.json', 'conclusion_id'), ('Scoring-rule', 'scoring_rules.json', 'rule_id')]:
                match = re.search(r'^- ' + label + r' IDs: `([^`]+)`', text, re.M)
                if match:
                    doc = json.loads((p.parent / fn).read_text())
                    current = {x[key] for x in doc.get('items', doc.get('rules', []))}
                    stale.extend(set(match.group(1).split(', ')) - current)
            if stale:
                replace(p, '## Evaluator alignment',
                        '## Historical evaluator alignment (archived snapshot)\n\n'
                        '> Maintenance clarification (2026-09-18): this section and its rule/value correspondence record the evaluator at the time of the archived calculation, not the current scoring contract. Retired or renamed IDs here are historical, not active scoring requirements. The current five evaluator JSON files are authoritative. This clarification does not change the successful calculations, scientific values or historical logs. Inactive IDs in the header below: ' + ', '.join('`' + x + '`' for x in sorted(set(stale))) + '.')
    emit_patch()


def manifest_patch():
    sys.path.insert(0, str(ROOT))
    from evaluation.contracts.task_package import package_payload_entries, package_content_hash
    for mode in MODES:
        for p in sorted((ROOT / 'tasks' / ('final_verified_' + mode)).glob('paper_*/package_manifest.json')):
            doc = json.loads(p.read_text())
            entries = package_payload_entries(p.parent)
            digest = package_content_hash(entries)
            if digest != doc['package_content_sha256']:
                doc['entries'] = [e.model_dump(mode='json') for e in entries]
                doc['package_content_sha256'] = digest
                changes[p] = json.dumps(doc, ensure_ascii=False, indent=2) + '\n'
    emit_patch()


def point_binding_patch():
    for mode in MODES:
        p = path(mode, '988bc12ae3768679', 'evaluation/reference_key_points.json')
        def update(doc):
            for row in doc['items']:
                for suffix, name in [('result_acid', '2a-acid'), ('result_base', '2a-base')]:
                    if row['key_point_id'].endswith(suffix):
                        row['binding']['fields'] = ['$.structures[*]']
                        for field in ('expected', 'expected_result'):
                            if field in row:
                                row[field] = f'Select the unique record named {name}, never an array position. ' + row[field]
        edit_json(p, update)
    emit_patch()


if __name__ == '__main__':
    command = sys.argv[1] if len(sys.argv) > 1 else 'tasks'
    {'tasks': main, 'archives': archive_patch, 'manifests': manifest_patch, 'point-bindings': point_binding_patch}[command]()
