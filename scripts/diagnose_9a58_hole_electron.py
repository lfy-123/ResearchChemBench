"""Bounded postprocessing diagnostic on existing Gaussian wavefunctions.

No SCF, geometry optimization, TD eigensolve or evaluator mutation. New logs
live outside docs/verification, whose original records are read-only here.
"""
from pathlib import Path
import argparse
import datetime
import json
import os
import re
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'docs/verification/group_1/paper_9a58a1fa6ed7d780'
RECOVERY = SOURCE / 'provenance/local_recovery_20260918/BN_AkFlu_TD6_fullcoeff_resume_20260918'
SOFTWARE = ROOT / '.software_cache/installations/multiwfn/2026.7.15/Multiwfn_2026.7.15_bin_Linux_noGUI'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cutoff', type=float, default=.001)
    parser.add_argument('--grid', choices=(1, 2, 3), type=int, default=2)
    parser.add_argument('--states', type=int, nargs='+', default=[1, 2, 3, 4, 5, 6])
    args = parser.parse_args()
    assert 0 <= args.cutoff <= .01 and set(args.states).issubset(range(1, 7))
    out = ROOT / 'docs/claude/artifacts/9a58_root_cause_20260918' / (f'cross_{args.cutoff:g}_grid{args.grid}_states' + '-'.join(map(str,args.states)))
    out.mkdir(parents=True, exist_ok=False)
    (out / 'wavefunction.fchk').symlink_to(RECOVERY / 'fullcoeff.fchk')
    (out / 'td.log').symlink_to(RECOVERY / 'gaussian.log')
    settings = (SOFTWARE / 'settings.ini').read_text()
    settings = re.sub(r'(?m)^(\s*nthreads\s*=)\s*\d+', r'\g<1> 2', settings)
    settings = re.sub(r'(?m)^(\s*cfgcrossthres\s*=)\s*\S+', lambda m: m[1] + ' ' + str(args.cutoff), settings)
    (out / 'settings.ini').write_text(settings)
    menu = ['18', '1', 'td.log']
    for i, state in enumerate(args.states):
        if i:
            menu.append('1')
        menu += [str(state), '1', str(args.grid), '0', '0']
    menu += ['0', 'q']
    (out / 'commands.txt').write_text('\n'.join(menu) + '\n')
    start = time.monotonic()
    run = {'started_at': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'threads': 2,
           'source_wavefunction': str(RECOVERY / 'fullcoeff.fchk'),
           'source_excitation_log': str(RECOVERY / 'gaussian.log'),
           'cfgcrossthres': args.cutoff, 'grid_menu': args.grid, 'requested_states': args.states,
           'new_SCF_or_TD': False}
    print(str(out), flush=True)
    with (out / 'commands.txt').open() as stdin, (out / 'multiwfn.log').open('w') as stdout:
        try:
            result = subprocess.run([str(SOFTWARE / 'Multiwfn_noGUI'), 'wavefunction.fchk'],
                                    cwd=out, stdin=stdin, stdout=stdout, stderr=subprocess.STDOUT,
                                    env={**os.environ, 'OMP_NUM_THREADS': '2', 'MKL_NUM_THREADS': '2', 'OMP_STACKSIZE': '200M'}, timeout=1800)
            run['return_code'] = result.returncode
        except subprocess.TimeoutExpired:
            run['timed_out'] = True
            raise
        finally:
            run['elapsed_seconds'] = time.monotonic() - start
            (out / 'status.json').write_text(json.dumps(run, indent=2) + '\n')
    assert result.returncode == 0
    text = (out / 'multiwfn.log').read_text()
    patterns = {'Sr': r'Sr index \(integral of Sr function\):\s+([-+\d.]+)',
                'H_angstrom': r'H index:\s+([-+\d.]+) Angstrom',
                'D_angstrom': r'D index:\s+([-+\d.]+) Angstrom',
                't_angstrom': r't index:\s+([-+\d.]+) Angstrom',
                'HDI': r'Hole delocalization index \(HDI\):\s+([-+\d.]+)',
                'EDI': r'Electron delocalization index \(EDI\):\s+([-+\d.]+)',
                'hole_integral': r'Integral of hole:\s+([-+\d.]+)',
                'electron_integral': r'Integral of electron:\s+([-+\d.]+)'}
    states = []
    for block in re.split(r'Loading configuration coefficients of excited state\s+', text)[1:]:
        row = {'state': int(re.match(r'\d+', block)[0])}
        for key, pattern in patterns.items():
            match = re.search(pattern, block)
            assert match, (row['state'], key)
            row[key] = float(match[1])
        states.append(row)
    assert [r['state'] for r in states] == args.states
    payload = {'run': run, 'states': states, 'meaning': 'New postprocessing diagnostic, not a changed scientific target or a whole-paper PASS.'}
    (out / 'results.json').write_text(json.dumps(payload, indent=2) + '\n')
    print(json.dumps(payload), flush=True)


if __name__ == '__main__':
    main()
