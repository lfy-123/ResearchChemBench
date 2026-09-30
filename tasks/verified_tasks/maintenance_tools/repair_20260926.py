"""Emit a reviewable apply_patch patch for the approved nine-paper staged batch.

No filesystem writes, quantum calculations, or changes outside the explicit packages.
Run from repository root with the researchchembench Python environment.
"""
# One-time patch generator for the 940d3d04/5d18a199 baseline. Later targeted
# corrections supersede this draft: do not rerun it over maintained packages.
from pathlib import Path
import copy
import difflib
import json
import re
import sys

ROOT = Path('tasks/verified_tasks')
IDS = ['paper_d83e607f125440cc', 'paper_2877efc02814175d', 'paper_8fefc96b015c4577',
       'paper_9ec32e81e2826041', 'paper_1a47bc00fd63b2f5', 'paper_9132719dbf91c978',
       'paper_0e835b370ddd37b6', 'paper_2a71ffa4b0a90809', 'paper_72822e4ddb5d9b11']
changes = {}

def put(path, value):
    changes[path] = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, indent=2)+'\n'

def load(path):
    return json.loads(path.read_text())

def required(*names):
    return {'required': list(names)}

def nonempty():
    return {'type': 'string', 'minLength': 1}

def condition(field, value, then, otherwise=None):
    x={'if': {'required':[field], 'properties':{field:{'const':value}}},'then':then}
    if otherwise is not None:x['else']=otherwise
    return x

def clean_required(node):
    if isinstance(node, dict):
        if 'required' in node:
            node['required']=[n for n in node['required'] if n not in ('limitations','stopping_rule','stopping_criterion','stopping_basis','unresolved_alternatives')]
        for k,v in node.items():
            if k=='properties':
                for name,prop in v.items():
                    if name=='limitations':
                        prop.pop('minLength',None);prop.pop('minItems',None)
            clean_required(v)
    elif isinstance(node,list):
        for v in node:clean_required(v)

def unique_objects(array, field, names):
    array['minItems']=array['maxItems']=len(names)
    array['items']['properties'][field]={'enum':names}
    array['allOf']=[{'contains':{'required':[field],'properties':{field:{'const':n}}},'minContains':1,'maxContains':1} for n in names]

def bound_rule(rules, rid, expected=None, fields=None):
    r=next(x for x in rules if x['rule_id']==rid)
    if expected is not None:r['expected']=expected
    if fields is not None:r['binding']['fields']=fields
    return r

CONTENT = {
'd83': (
"Characterize sulfur Hirshfeld spin localization and the benzylic C–H dissociation energy of 4-(methylsulfanyl)benzyl alcohol radical cation (2g). Construct the 4-methoxybenzyl alcohol radical-cation comparator (2a) and calculate its like-defined dissociation energy. Interpret what the computed descriptors imply about oxidation behavior.",
"The author route examines radical-cation spin localization and homolytic benzylic H loss as possible explanations for differing alcohol oxidation behavior. Test these descriptors; no energetic ordering is supplied.",
"`data/inputs/2g_radical_cation_vacuum.xyz` supplies the 20-atom C8H10OS parent identity, not a dissociation product. Use gas phase, charge +1, multiplicity 2. Map the unique S atom and a C–H bond on CH2OH (not S–CH3). Independently construct 2a from its stated chemical identity; no external structure download is required. The primary BDE is the adiabatic electronic quantity D_e = E(relaxed dehydrogenated cation, +1 singlet) + E(H atom, neutral doublet) − E(relaxed parent, +1 doublet), in kJ/mol. Do not add zero-point or thermal corrections to this primary quantity; corrected quantities may be reported separately. Use a consistent electronic-structure protocol for both substrates and all fragments; disclose it. The spin observable is the dimensionless Hirshfeld atomic spin population, not a charge.",
"Establish the parent minimum with frequency or justified equivalent evidence, evaluate sulfur spin, and compute both BDEs from traceable energies and fragment identities. Report method, state, atom mapping, convergence and comparison; explain material conformer/model choices. Additional exploration is allowed. The AR investigation records its plan and calculations actually attempted, not a prescribed search-round count.",
"Submit `report/results.json` following `submission_schema.json`. `success` requires minimum validation, spin, both electronic BDEs and their comparison; `bounded_failure` records the failed stage, diagnostics and genuinely available partial results. Missing computations must not be replaced with assumed numbers."),
'2877': (
"Calculate and compare frontier-orbital gaps, chemical hardness and electrophilicity for the three supplied DQCS divalent-metal complexes, using a consistent electronic-descriptor definition.",
"The author route compares the electronic descriptors of the three 1:1 complexes to investigate how metal coordination affects electronic reactivity. Test that comparison without presupposing an ordering.",
"Use `data/inputs/cd_complex.xyz`, `co_complex.xyz` and `ni_complex.xyz` in that directory. Each has 65 centers, listed by atomic number and Cartesian coordinates in Å, and is the complete 1:1 complex. Charge/multiplicity are Cd (+2,1), Co (+2,2), Ni (+2,1). The primary solvent boundary is implicit DMSO; controlled alternatives may be reported separately. Do not add counterions or explicit solvent. These are given-object property calculations, not discovery of the supplied molecular identities. Optimization or a justified single point is permitted. Choose and document the model and frontier definition consistently. For orbital-based descriptors, gap = LUMO − HOMO, eta = gap/2, mu = (HOMO + LUMO)/2 and omega = mu²/(2 eta), with energies in eV. For open shells report the spin channel and avoid mixing unlike definitions; a justified alternative descriptor convention must be explicit and used consistently.",
"Check atom count, metal, charge and spin for each object; establish electronic convergence and provide calculation evidence. Report all three descriptors per successful object. Use exactly one main row each for object_id/metal `Cd`, `Co`, `Ni`, in any order. Failed objects retain their identity and actual diagnostics; additional attempts can be recorded separately. Compare only valid, like-defined observables.",
"Submit `report/results.json`. Each completed complex requires all three numerical observables and validation evidence. A failed complex uses `bounded_failure` and `observables.failure_reason`; this is not a completed cross-metal comparison. Describe the method and calculated ordering; no generic disclaimer or stopping statement is required."),
'9ec': (
"Calculate the signed 300 K Gibbs free-energy difference ΔG = G_coplanar − G_perpendicular between the two given conformational families of neutral singlet Z-cAAC^Cy, and interpret their relative stability.",
"The author route compares the two arrangements and examines dispersion contributions to conformational stability. Optimize and characterize the two states before comparing their free energies.",
"Use `data/inputs/perpendicular.xyz` and `data/inputs/coplanar.xyz`: each defines the same complete 80-atom C35H43NZn molecule, charge 0 and multiplicity 1. The conformer names identify families, not exact angles imposed on optimized geometries. The primary comparison is isolated-molecule PBE0-D3BJ/6-311+G(d,p) harmonic Gibbs energies at 300 K and 1 atm, including zero-point and thermal contributions. This shared measurement protocol defines the method-dependent observable; other methods may be additional controls, not substitutes for the primary result. No solvent, crystal packing or unprovided conformer search is required.",
"Verify both identities and retain labels `perpendicular` and `coplanar`, one main record each, in any order. Optimize and establish each local minimum, including frequency evidence and final geometry. Compute consistent Gibbs energies and ΔG in kJ/mol; retain source energies and conversion so the subtraction can be checked. Keep identity checks distinct from stationary-point checks. Additional attempts may be recorded separately.",
"Submit `report/results.json`. `complete` requires both validated minima, numerical free energies and signed ΔG; otherwise use `bounded_failure`, reporting available results and the actual failure reason without inventing energies. A general limitations statement is optional."),
'913': (
"Determine the Gibbs free-energy barrier for terminal H2 reductive elimination from the specified neutral singlet palladium dihydride INT-G, and assess the implication for the terminal catalyst-regeneration step.",
"The authors investigate a palladium-mediated pathway and test H2 loss from INT-G as the terminal regeneration step. Construct and validate that channel; do not assume its barrier.",
"`data/inputs/int_g.xyz` defines the complete 77-atom C39H34OP2Pd reactant, charge 0, multiplicity 1, with two terminal hydrides. Construct the transition structure and H2/Pd(0) endpoint yourself. The primary observable is G(TS) − G(INT-G), in kcal/mol, for implicit N,N-dimethylacetamide (DMAc), with consistent harmonic corrections at 298.15 K and 1 atm. State the geometry/frequency and solution-energy protocols and any composite-energy convention. The supplied reactant is not a TS or separated product; a bound H2 intermediate must not be mislabeled as separated H2. Methods may be chosen and disclosed; other environments are additional controls.",
"Validate the INT-G minimum, locate the H2-elimination saddle and establish one relevant imaginary mode. Provide IRC, mode-following, relaxed-scan or justified equivalent evidence connecting the reactant and H2/Pd(0) sides; identify any additional release step after a bound H2 state. Preserve ligand identity and atom balance. Record materially relevant attempts and traceable energies. Additional search is allowed without a fixed number of rounds.",
"Submit `report/results.json`. `success` requires stationary-point evidence, a numerical barrier with reference state and units, and connection evidence. Use `bounded_failure` with `failure_report.reason`, `attempted_search` and `available_diagnostics` when incomplete; unavailable success-only values can be omitted. Report genuine partial results without claiming the final result was obtained."),
'0e': (
"Determine and compare H–H activation free-energy barriers for neutral singlet silylenes 1 and V′ reacting with neutral singlet H2, using separated reactants as the reference for each system.",
"The authors compare a six-membered cyclic (alkyl)(amino)silylene and a known analogue as H2-activation platforms. Construct and test the H–H-cleavage pathways without assuming which is preferred.",
"Use `data/inputs/silylene_1_singlet.xyz` (55 atoms), `data/inputs/silylene_Vprime_singlet.xyz` (36 atoms), and `data/inputs/h2.xyz`. These are given reactant identities, not H2-activation TSs. All are neutral singlets. The primary physical boundary is implicit benzene, 298 K and 1 atm; apply the same stated method and Gibbs convention to both systems and separated H2. Barrier = G(TS) − G(silylene) − G(H2), in kcal/mol. Conformers and TS approaches are to be constructed by the agent; no author TS is supplied.",
"Optimize and characterize the reactants as minima. Locate H–H activation TSs, verify exactly one relevant imaginary mode, and establish reactant/product connection by IRC, constrained relaxation or a justified endpoint test. Use one main row for `system_id` = `1` and one for `V-prime`, in any order; record extra attempts separately. Report candidate evidence and comparable barriers, then determine the ordering from your results. No fixed two-round stopping rule is imposed.",
"Submit `report/results.json`. Set overall status to `complete` only when both rows are `validated_success`; each requires a validated reactant, TS/connection evidence and numerical barrier. Otherwise use `bounded_failure`, with each failed row's reason and available diagnostics. Missing frequency or barrier values may be omitted/null as permitted by the schema; do not fabricate them."),
'728': (
"Compare the relaxed closed-shell singlet and triplet states of neutral nanographene complex 4. Calculate their adiabatic electronic energy difference and determine which of these two states is lower.",
"The author route tests a closed-shell singlet assignment by separate optimization and comparison with a triplet calculation. Evaluate the two states without assuming their energetic ordering.",
"`data/inputs/complex_4.xyz` defines the complete 165-atom C87H72Cl2N2NiO complex. Use charge 0 and multiplicities 1 and 3, preserving chemical identity. The primary quantity is [E_triplet(relaxed) − E_singlet(relaxed)] in kcal/mol: optimize each state independently under the same declared model. A positive value means the singlet is lower; this definition supplies no expected sign. It is not a vertical same-geometry gap and contains no thermal/free-energy correction. Such controls may be reported separately.",
"Choose and document the method, basis, software and numerical settings. Check each state's multiplicity, electronic convergence and vibrational/equivalent stationary-point evidence. Retain both electronic energies in Hartree, the conversion, numerical gap and lower-state assignment, so they can be independently checked. The comparison concerns these specified states, not all possible electronic states or geometrical discovery.",
"Submit `report/results.json` and cited supporting files. `completed` requires both optimized validated states, their electronic energies, `gap_kcal_mol` and `lower_state`. Otherwise use `bounded_failure` with `failure_reason` and whatever diagnostics/results actually exist; unavailable energies are not mandatory. Optional extra attempts must not overwrite the two primary state records.")}

def task_text(parts, pr):
    objective,guidance,inputs,work,out=parts
    text='# Scientific objective\n\n'+objective+'\n\n'
    if pr:text+='# Author-provided scientific guidance\n\n'+guidance+'\n\n'
    return text+'# Public inputs and scientific boundaries\n\n'+inputs+' No paper, SI, evaluator, historical verification archive or general-web lookup is an agent input.\n\n# Required scientific validation/investigation\n\n'+work+'\n\n# Deliverables\n\n'+out+'\n'

COMMON_E = ('Evaluate real calculations and scientifically correct results; ordinary disclaimers, search-round counts and generic limitations are not scored. A truthful failure is a valid submission, not achievement of missing scientific results. Credit only actually supported components; extra failed attempts do not invalidate a successful main result. Verify identity, units, energy references and calculation evidence before numerical agreement. ')

for pid in IDS:
 for mode in ['autonomous_research','paper_reproduction']:
    p=ROOT/mode/pid
    if not p.is_dir():continue
    pr=mode=='paper_reproduction'; short=pid.split('_')[1]
    key=next((k for k in CONTENT if short.startswith(k)),None)
    if key:put(p/'agent_input/task.md',task_text(CONTENT[key],pr))
    schema=load(p/'agent_input/submission_schema.json');clean_required(schema)
    s=schema['result_schema'];s['$schema']='https://json-schema.org/draft/2020-12/schema';s.setdefault('type','object')
    props=s['properties']
    kp=load(p/'evaluation/reference_key_points.json');cs=load(p/'evaluation/reference_conclusions.json');sr=load(p/'evaluation/scoring_rules.json');cf=load(p/'evaluation/critical_failures.json')
    removed={x['conclusion_id'] for x in cs['items'] if x.get('claim_role')=='limitation'}
    cs['items']=[x for x in cs['items'] if x['conclusion_id'] not in removed]
    sr['rules']=[x for x in sr['rules'] if x.get('reference_id') not in removed]
    sr['scoring_policy']='dual_axis_100.scientific_results.v1'
    rules=sr['rules']; main=cs['items'][0]
    main['supporting_key_point_ids']=[x['key_point_id'] for x in kp['items']]
    for r in rules:
        if 'binding' in r:
            r['binding']['fields']=[f.replace('[]','[*]') for f in r['binding'].get('fields',[]) if not f.endswith('.limitations') and f!='$.limitations']
    if key=='d83':
        success=s['oneOf'][0];success['required']=list(dict.fromkeys(success['required']+['method']))
        success['properties']['method']={'type':'object','required':['software','model','solvent_boundary','population_method','bde_convention']}
        props['system']={'type':'object','properties':{'formula':{'const':'C8H10OS'},'charge':{'const':1},'multiplicity':{'const':2}}}
        main['expected']='Substantial sulfur Hirshfeld spin population and a higher electronic 2g benzylic C–H dissociation energy than 2a are correctly calculated and interpreted as descriptor-level oxidation evidence.'
        bound_rule(rules,'r_minimum','Zero imaginary frequencies or justified equivalent minimum evidence for the correct parent; failure does not earn successful minimum validation.', ['$.minimum_validation.imaginary_frequencies','$.minimum_validation.validation_statement','$.system'])
        bound_rule(rules,'r_spin')['unit']='dimensionless'
        bound_rule(rules,'r_conclusion',COMMON_E+main['expected'],['$.conclusion','$.comparison','$.method','$.spin_density','$.bde_2g','$.bde_2a_comparator'])
        route=(p/'paper_route.md').read_text().replace('HF-based benzylic','B3LYP electronic benzylic').replace('HF-based BDE calculation in vacuum','B3LYP electronic-energy differences in vacuum (the SI HF energy label is not a Hartree–Fock method specification)')
        put(p/'paper_route.md',route)
    elif key=='2877':
        a=props['complexes'];unique_objects(a,'object_id',['Cd','Co','Ni']);row=a['items'];obs=row['properties']['observables']
        row['allOf']=[condition('status','completed',{'properties':{'observables':required('homo_lumo_gap_eV','hardness_eV','electrophilicity_eV')}},{'properties':{'observables':required('failure_reason')}})]
        for metal in ['Cd','Co','Ni']:row['allOf'].append(condition('object_id',metal,{'properties':{'metal':{'const':metal}}}))
        obs['oneOf'][1]['properties']['failure_reason']=nonempty()
        main['expected']='Real like-defined results support gap and hardness Cd > Co > Ni, electrophilicity Ni > Co > Cd. These are electronic descriptors, not measured binding free energies.'
        bound_rule(rules,'r_state',fields=['$.state_checks','$.complexes'])
        bound_rule(rules,'r_trend',COMMON_E+main['expected'],['$.comparison','$.complexes','$.method'])
    elif key=='0e':
        props['status']={'enum':['complete','bounded_failure']};a=props['systems'];unique_objects(a,'system_id',['1','V-prime']);row=a['items']
        minimum=row['properties']['minimum'];minimum['required']=['optimized','evidence'];minimum['properties']['imaginary_frequencies']={'type':['integer','null'],'minimum':0}
        row['properties']['barrier']['type']=['number','null'];row['required']=['system_id','minimum','ts_search','outcome_status']
        row['oneOf'][0]['required']+=['barrier']
        row['oneOf'][0]['properties']['minimum']={'required':['imaginary_frequencies'],'properties':{'optimized':{'const':True},'imaginary_frequencies':{'const':0}}}
        row['oneOf'][0]['properties']['ts_search']={'properties':{'candidates_validated':{'minimum':1}}}
        s['allOf']=[condition('status','complete',{'properties':{'systems':{'items':{'properties':{'outcome_status':{'const':'validated_success'}}}}}},{'properties':{'systems':{'contains':{'properties':{'outcome_status':{'const':'bounded_failure'}}}}}})]
        main['statement']=main['expected']='Validated H–H activation barriers from separated reactants are lower for silylene 1 than for V-prime. The comparison must be supported by the two corresponding TSs and a common method/Gibbs convention.'
        bound_rule(rules,'r_final',COMMON_E+main['expected'],['$.systems','$.comparison','$.conclusion','$.method'])
        bound_rule(rules,'r_barriers',fields=['$.systems','$.method'])
    elif key=='913':
        props['system']['properties']['charge']={'const':0};props['system']['properties']['multiplicity']={'const':1}
        s['oneOf']=[{'properties':{'status':{'const':'success'},'barrier':{'properties':{'value_kcal_mol':{'type':'number'}}}},'required':['stationary_point','barrier','connection_evidence']}, {'properties':{'status':{'const':'bounded_failure'}},'required':['failure_report']}]
        for v in props['failure_report']['properties'].values():v['minLength']=1
        main['expected']='Real minimum, H2-elimination saddle and connection evidence support a very small terminal barrier and corresponding regeneration-step interpretation.'
        bound_rule(rules,'r_kp_ts',fields=['$.stationary_point','$.connection_evidence','$.investigation'])
        bound_rule(rules,'r_final',COMMON_E+main['expected'],['$.conclusion','$.barrier','$.method','$.connection_evidence'])
        for f in cf['items']:
            if f['failure_id']=='cf_answer_only':f['condition']='A numerical barrier is asserted without traceable calculations, method, units or an identified reference state.'
    elif key=='728':
        state=s['$defs']['state'];state['required']=['multiplicity','method'];state['properties']['failure_reason']=nonempty()
        props['system']['properties']['charge']={'const':0}
        for name,mult in [('singlet_state',1),('triplet_state',3)]:
            props['states']['properties'][name]={'allOf':[{'$ref':'#/$defs/state'},{'properties':{'multiplicity':{'const':mult}}}]}
        props['failure_reason']=nonempty()
        s['allOf']=[condition('status','completed',{'required':['gap_kcal_mol','lower_state'],'properties':{'states':{'properties':{n:{'required':['energy_hartree','optimized','convergence','stationarity'],'properties':{'optimized':{'const':True}}} for n in ['singlet_state','triplet_state']}}}},required('failure_reason'))]
        main['expected']='Traceable relaxed-state electronic energies give a positive Et−Es gap and lower closed-shell singlet in this two-state comparison.'
        bound_rule(rules,'r_gap',COMMON_E+main['expected']+' Check subtraction and Hartree-to-kcal/mol conversion.', ['$.status','$.states','$.gap_kcal_mol','$.lower_state','$.conclusion.claim'])
        bound_rule(rules,'r_final',COMMON_E+main['expected'],['$.conclusion.claim','$.states','$.gap_kcal_mol','$.lower_state'])
        for f in cf['items']:
            if f['failure_id']=='cf_unvalidated_claim':f['condition']='A definitive state ordering is asserted without corresponding electronic-state, convergence and stationary-point evidence.'
    elif key=='9ec':
        a=props['structures'];unique_objects(a,'label',['perpendicular','coplanar']);row=a['items'];row['properties']['stationary_point']['required']=['status']
        for k,v in [('charge',0),('multiplicity',1)]:row['properties']['input_validation']['properties'][k]={'const':v}
        row['properties']['method']['properties']['temperature_K']={'const':300}
        props['comparison']['oneOf'][1]['required'].append('failure_reason');props['comparison']['oneOf'][1]['properties']['failure_reason']=nonempty()
        complete_row={'properties':{'stationary_point':{'required':['frequency_evidence','imaginary_frequency_count'],'properties':{'imaginary_frequency_count':{'const':0},'frequency_evidence':nonempty()}},'free_energy':{'required':['value_kJ_mol','source_or_diagnostic']}}}
        s['oneOf']=[{'properties':{'status':{'const':'complete'},'structures':{'items':complete_row},'comparison':{'properties':{'status':{'const':'complete'}}}}}, {'properties':{'status':{'const':'bounded_failure'},'comparison':{'properties':{'status':{'const':'bounded_failure'}}}}}]
        for item in kp['items']:
            if item['key_point_id'].endswith('process_inputs'):item['statement']=item['expected']='Two uniquely labeled 80-atom C35H43NZn conformers have consistent chemical identity, charge 0, multiplicity 1 and input-to-result mapping.'
            elif item['key_point_id'].endswith('process_validation'):item['statement']=item['expected']='Both distinct conformers are optimized minima with frequency evidence and consistently computed primary-protocol Gibbs energies at 300 K.'
        prefix='pr' if pr else 'ar'
        bound_rule(rules,f'r_{prefix}_process_inputs',kp['items'][0]['expected'],['$.structures[*].label','$.structures[*].input_file','$.structures[*].input_validation'])
        bound_rule(rules,f'r_{prefix}_process_validation',kp['items'][1]['expected'],['$.structures[*].stationary_point','$.structures[*].method','$.structures[*].free_energy'])
        main['expected']='The primary PBE0-D3BJ/6-311+G(d,p), 300 K gas-phase harmonic Gibbs comparison supports near-isoenergetic conformers. Check the signed subtraction and distinct optimized identities; do not apply this claim blindly to dispersion-free control calculations.'
        bound_rule(rules,f'r_{prefix}_final_conclusion',COMMON_E+main['expected'],['$.conclusion','$.comparison','$.structures'])
        if not pr:
            for alias in ['coplanar_zcaac_cy.xyz','perpendicular_zcaac_cy.xyz']:changes[p/'agent_input/data/inputs'/alias]=None
    elif short.startswith('1a'):
        text=(p/'agent_input/task.md').read_text()
        text=text.replace('common catalyst-bound precursor','common Gibbs-energy reference (the same selected catalyst-bound precursor energy for both channels; reverse paths may reach different precursor conformers)')
        # Retain source-specific substrate/catalyst/experiment; replace only administrative stopping prose.
        text=re.sub(r' Stop when[^\n]*?(?=\n|$)','',text)
        text=text.replace('and limitations','').replace('and limitation statements','').replace('and a limitation statement','')
        text+='\nCompleted results require one validated main candidate for each channel, `ortho_4_hydroxybenzofuran` and `para_6_hydroxybenzofuran`, with frequency and IRC/equivalent connection evidence and common-reference Gibbs barriers. Use the same precursor Gibbs energy for both barrier subtractions; different precursor conformers reached by reverse paths are allowed if their relation to that reference is explained. Failed or additional candidates may be retained, but are not substitutes for a missing successful channel. In early failure, omit unavailable frequencies/paths and give `failure_reason`; general disclaimers and stopping statements are optional.\n'
        put(p/'agent_input/task.md',text)
        candidates=props['candidates'];candidates['minItems']=0;row=candidates['items'];row['required']=['candidate_id','channel','structure_identity','validation_status']
        row['properties']['failure_reason']=nonempty()
        valid=required('gibbs_barrier_kcal_mol','imaginary_frequency_cm-1','validation_evidence','frequency_evidence','irc_evidence')
        row['anyOf']=[valid,required('failure_reason')]
        s['oneOf'][0]['properties']['candidates']={'allOf':[{'contains':{'allOf':[{'properties':{'channel':{'const':channel}}},valid]}} for channel in ['ortho_4_hydroxybenzofuran','para_6_hydroxybenzofuran']]}
        props['failure_report']['required']=['failed_channels','attempted_candidate_ids','reason'];props['failure_report']['properties']['reason']=nonempty();props['failure_report']['properties']['attempted_candidate_ids']['minItems']=0
        main['expected']='Two validated first-cyclization channels give lower ortho than para barrier on the same reference and support the observed regioselectivity. The experimental input alone is not computational evidence.'
        bound_rule(rules,'r_final',COMMON_E+main['expected'],['$.conclusion.claim','$.candidates','$.barrier_comparison','$.system'])
        for f in cf['items']:
            if f['failure_id']=='cf_fabricated_failure':f['condition']='A reported result is fabricated, or a failed/incomplete channel is represented as a validated successful channel.'
    elif short.startswith('2a'):
        text=(p/'agent_input/task.md').read_text()
        hypothesis="The authors qualitatively interpret this donor as a rigid, atropisomeric structure arising from steric crowding by I and F; independently test that hypothesis computationally."
        if '# Author-provided scientific guidance' not in text:text=text.replace(hypothesis,'').replace('# Public inputs','# Author-provided scientific guidance\n\n'+hypothesis+'\n\n# Public inputs')
        text=text.replace('Report the thermal treatment and its limitations explicitly.','Report the thermal treatment, including how negative and low-frequency modes enter the thermochemistry.')
        text=text.replace('Stop when the interval is covered, the profile maximum is identified, and additional refinement changes the extracted barrier by no more than 1.0 kcal mol−1 or you explain why that criterion cannot be met and provide a bounded limitation.','Report the quantitative sensitivity of the extracted barrier to the control you performed; a generic disclaimer is not a sensitivity calculation.')
        text=text.replace('sensitivity, conclusion and limitations','sensitivity and conclusion').replace('achieved coverage and a scientifically specific limitation','achieved coverage and the specific reason it is incomplete')
        put(p/'agent_input/task.md',text)
        props['scan_states']['minItems']=0
        s['oneOf'][0]['properties']['scan_states']={'minItems':5,'contains':{'properties':{'converged':{'const':True}},'required':['converged','gibbs_relative_kcal_mol']},'minContains':5}
        s['oneOf'][0]['properties']['barrier_result']=required('barrier_kcal_mol','reference_state','maximum_state_id','extraction_method','profile_coverage')
        # Substantive failed-stage reason remains mandatory; it is not a disclaimer.
        failure=props['barrier_result']['oneOf'][1];failure['required']=['barrier_status','profile_coverage','failure_reason'];failure['properties']['failure_reason']=nonempty()
        s['oneOf'][1]['required']=['failure_summary','conclusion']
        s['oneOf'][0]['properties']['sensitivity']=required('test_description','result','barrier_change_kcal_mol')
        for x in kp['items']:
            if x['key_point_id']=='kp_limits':x['statement']=x['expected']='A concrete numerical sensitivity/robustness test reports its effect on the constrained-scan barrier and identifies the quantity actually computed.'
        bound_rule(rules,'r_limits', 'Assess the actual control and numerical barrier change, not generic caveats.', ['$.sensitivity','$.barrier_result'])
        bound_rule(rules,'r_final',COMMON_E+main['expected'])
    put(p/'agent_input/submission_schema.json',schema)
    for name,obj in [('reference_key_points',kp),('reference_conclusions',cs),('scoring_rules',sr),('critical_failures',cf)]:put(p/f'evaluation/{name}.json',obj)

# Specialized answer-structure repair: fresh radical geometry from chemical graph only.
from rdkit import Chem
from rdkit.Chem import AllChem, rdMolDescriptors, rdDetermineBonds
import networkx as nx
smiles='CCOC(=O)C(F)(F)C[CH]CN(Cc1ccccc1)S(=O)(=O)c1ccc(C)cc1'
mol=Chem.AddHs(Chem.MolFromSmiles(smiles))
assert rdMolDescriptors.CalcMolFormula(mol)=='C21H24F2NO4S' and mol.GetNumAtoms()==53
params=AllChem.ETKDGv3();params.randomSeed=20260926
assert AllChem.EmbedMolecule(mol,params)==0
assert AllChem.UFFOptimizeMolecule(mol,maxIters=1000)==0
xyz=Chem.MolToXYZBlock(mol).splitlines();xyz[1]='Independent graph-embedded radical starter; charge 0; multiplicity 2; angstrom; not a stationary point'
xyz='\n'.join(xyz)+'\n'
def graph(m):
    g=nx.Graph();g.add_nodes_from((a.GetIdx(),{'element':a.GetSymbol()}) for a in m.GetAtoms());g.add_edges_from((b.GetBeginAtomIdx(),b.GetEndAtomIdx()) for b in m.GetBonds());return g
source_path=ROOT/'paper_reproduction/paper_8fefc96b015c4577/agent_input/data/inputs/intermediate_B.xyz'
if not source_path.exists():source_path=ROOT/'paper_reproduction/paper_8fefc96b015c4577/evaluation/author_results/intermediate_B.xyz'
source=Chem.MolFromXYZBlock(source_path.read_text());rdDetermineBonds.DetermineConnectivity(source)
assert nx.is_isomorphic(graph(source),graph(mol),node_match=lambda a,b:a['element']==b['element'])
for mode in ['autonomous_research','paper_reproduction']:
 p=ROOT/mode/'paper_8fefc96b015c4577';pr=mode=='paper_reproduction'
 oldnames=['intermediate_B','ts2','ts2_prime'] if pr else ['state_reference','state_candidate_1','state_candidate_2']
 for name in oldnames:
    f=p/f'agent_input/data/inputs/{name}.xyz';private=p/f'evaluation/author_results/{name}.xyz'
    put(private,(f if f.exists() else private).read_text());changes[f]=None
 put(p/'agent_input/data/inputs/radical_starter.xyz',xyz)
 identity={'formula':'C21H24F2NO4S','charge':0,'multiplicity':2,'smiles':smiles,'coordinates':'radical_starter.xyz','atom_index_base':1,'radical_atom_1based':10,'bonds':[{'atoms_1based':[b.GetBeginAtomIdx()+1,b.GetEndAtomIdx()+1],'order':b.GetBondTypeAsDouble()} for b in mol.GetBonds()]}
 put(p/'agent_input/data/inputs/system.json',identity)
 inputs='`data/inputs/system.json` defines the complete C21H24F2NO4S radical by SMILES, explicit connectivity and atom mapping; `data/inputs/radical_starter.xyz` is an independently graph-generated 53-atom initial conformation in Å, not an optimized minimum or TS. Use charge 0, multiplicity 2. Locate and validate the reference minimum and cyclization saddles yourself. The primary model is an isolated molecule with implicit DMSO, using consistent harmonic Gibbs energies at 298.15 K and 1 atm. State software, method, basis, dispersion and thermochemical settings. Other conditions may be controls. Photocatalyst, zinc acetate, explicit solvent and subsequent oxidation/aromatization are outside this cyclization comparison.'
 objective='Determine the competing intramolecular aryl-cyclization pathways of the supplied radical and their Gibbs barriers relative to its uncyclized minimum. Construct the transition-state candidates and establish the energetic ordering from real calculations.'
 guide='The author route compares closure onto the benzyl-tethered aryl ring (label `ts2`) with closure onto the arenesulfonyl aryl ring (`ts2_prime`), using the uncyclized radical minimum (`intermediate_B`) as their common energy reference. This guidance specifies the channels, not their geometry or energetic preference.'
 work='Optimize the radical reference and locate the two distinct aryl-cyclization saddles. Validate zero imaginary modes for the reference and one relevant mode for each saddle. Retain final geometries, input-to-output atom mapping and the forming C–C atom pair; inspect the negative mode to verify the assigned ring closure. IRC/endpoint following may strengthen the assignment but is not mandatory. Compute ΔG‡ = G(saddle) − G(reference) consistently in kcal/mol. Independent conformer and TS searches are allowed; do not infer a transition structure from an input filename.'
 out='Submit `report/results.json` and the geometry/calculation evidence it cites. '+('Use state keys `intermediate_B`, `ts2`, `ts2_prime` and barrier fields `barrier_ts2`, `barrier_ts2_prime`; `barrier_difference` means ts2_prime minus ts2.' if pr else 'Use `state_reference`, `state_candidate_1`, `state_candidate_2`; the candidate numbering is arbitrary, not ranked. Record each forming C–C pair and channel identity so evaluation can map the results chemically. `barrier_candidate_1`/`barrier_candidate_2` follow your labels; `barrier_difference` means candidate_2 minus candidate_1.')+' `complete` requires all three validated states and numerical barriers. Otherwise use `bounded_failure` with available evidence and a specific reason; unavailable numerical results may be omitted. Extra attempts may be recorded separately.'
 put(p/'agent_input/task.md',task_text((objective,guide,inputs,work,out),pr))
 schema=json.loads(changes[p/'agent_input/submission_schema.json']);s=schema['result_schema'];props=s['properties']
 props['method']['properties']['charge']={'const':0};props['method']['properties']['multiplicity']={'const':2}
 for name in oldnames:
    st=props['states']['properties'][name];st['required']=['identity','validation_status','validation_evidence'];st['properties']['failure_reason']=nonempty();st['properties']['geometry_file']=nonempty()
    if name!=oldnames[0]:st['properties']['forming_bond_1based']={'type':'array','minItems':2,'maxItems':2,'uniqueItems':True,'items':{'type':'integer','minimum':1,'maximum':53}}
 props['comparison']['oneOf'][1]['properties']['failure_reason']=nonempty()
 successstates={name:{'required':['energy','energy_unit','imaginary_frequency_count','geometry_file']+(['forming_bond_1based'] if i else []),'properties':{'imaginary_frequency_count':{'const':int(i>0)}}} for i,name in enumerate(oldnames)}
 s['allOf']=[condition('status','complete',{'properties':{'states':{'properties':successstates},'comparison':required(*props['comparison']['oneOf'][0]['required'])}}, {'properties':{'comparison':required('failure_reason')}})]
 put(p/'agent_input/submission_schema.json',schema)
 sr=json.loads(changes[p/'evaluation/scoring_rules.json']);rules=sr['rules'];cs=json.loads(changes[p/'evaluation/reference_conclusions.json']);kp=json.loads(changes[p/'evaluation/reference_key_points.json'])
 match='Map each saddle by molecular connectivity and forming-bond/negative-mode evidence: benzyl-tethered aryl closure corresponds to private TS2, arenesulfonyl aryl closure to private TS2-prime. Never map by closest energy or by arbitrary candidate number. '
 bound_rule(rules,'r_trace',match+'Check optimized geometries, common-reference Gibbs subtraction and traceable calculation evidence.', ['$.states','$.method','$.comparison'])
 for rid,channel in [('r_b1','benzyl-tethered aryl'),('r_b2','arenesulfonyl aryl')]:
    r=bound_rule(rules,rid,match+f'Compare the {channel} barrier with this rule target only after chemical identity is established.')
    r['binding']['fields']=['$.states','$.comparison'];r['binding']['comparison']='chemical identity mapping followed by absolute difference; semantic review required'
 final='Correctly mapped benzyl-tethered aryl closure has the lower common-reference barrier than arenesulfonyl aryl closure; both values and their subtraction are supported by validated saddles.'
 cs['items'][0]['statement']=cs['items'][0]['expected']=final
 bound_rule(rules,'r_conc',COMMON_E+match+final,['$.states','$.comparison','$.conclusion'])
 if not pr:bound_rule(rules,'r_order',match+final,['$.states','$.comparison','$.conclusion'])
 for x in kp['items']:
    if x['key_point_id'] in ['kp_res_order','kp_res_difference']:x['expected']=final
    if x['key_point_id']=='kp_proc_trace':x['expected']=match+'Common-reference energies and all optimized identities are traceable.'
 for n,obj in [('scoring_rules',sr),('reference_key_points',kp),('reference_conclusions',cs)]:put(p/f'evaluation/{n}.json',obj)
 cf=json.loads(changes[p/'evaluation/critical_failures.json'])
 for f in cf['items']:
    if f['failure_id']=='cf_identity':f['condition']='A successful comparison mixes chemical identities, omits a required channel, or lacks a recoverable mapping between the public molecular graph and optimized structures. Reordering atoms with an explicit valid map is allowed.'
 put(p/'evaluation/critical_failures.json',cf)
 info=load(p/'task_info.json');info['difficulty_reasons']=['Independent construction, optimization and frequency/mode validation of two competing cyclization saddles from a radical starter.'];info['data']=[{'path':'data/inputs','description':'Neutral doublet radical identity, connectivity and an independently graph-generated 53-atom initial geometry; no author TS coordinates.'}];put(p/'task_info.json',info)
 route=(p/'paper_route.md').read_text().replace('neutral closed-shell molecular model','neutral doublet radical molecular model')
 route+='\n## Current public/private boundary (2026-09-26)\n\nThe original SI geometries are private author_results only. Public input is a fresh ETKDGv3/UFF radical starter generated from the chemical graph, not a perturbed author endpoint. Historical author-informed Opt/Freq and negative-mode analysis validate the same two cyclization observables; they do not constitute blind replay from the new public starter. No new IRC requirement or coordinate-RMSD scoring is introduced.\n'
 put(p/'paper_route.md',route)
 put(p/'evaluation/task_provenance/independent_starter_preparation.json',{'date':'2026-09-26','smiles':smiles,'method':'RDKit ETKDGv3 then UFF(maxIters=1000)','seed':20260926,'formula':'C21H24F2NO4S','atom_count':53,'charge':0,'multiplicity':2,'radical_atom_1based':10,'source_role':'Main Scheme 3/SI pp34,36-37 define uncyclized radical identity. Author coordinates used only for a post-construction connectivity cross-check, never to embed/align/perturb/rank the starter.','checks':{'embedding_success':True,'UFF_converged':True,'element_labeled_connectivity_matches_source_B':True},'verification_boundary':'No quantum calculation or independent-starter replay was run. Private author Opt/Freq/mode evidence supports the required observables, not convergence of an arbitrary search.'})

patch='*** Begin Patch\n'
for path,new in changes.items():
    if len(sys.argv)>1 and not all(part in str(path) for part in sys.argv[1:]):continue
    old=path.read_text() if path.exists() else None
    if new==old:continue
    if new is None:patch+='*** Delete File: '+str(path)+'\n';continue
    if old is None:patch+='*** Add File: '+str(path)+'\n'+'\n'.join('+'+l for l in new.splitlines())+'\n';continue
    diff=list(difflib.unified_diff(old.splitlines(),new.splitlines(),n=3,lineterm=''))[2:]
    patch+='*** Update File: '+str(path)+'\n'+'\n'.join('@@' if l.startswith('@@') else l for l in diff)+'\n'
print(json.dumps(patch+'*** End Patch'))
