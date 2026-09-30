#!/usr/bin/env python3
"""Emit reviewed apply_patch edits only; no writes, jobs or quantum calculations.

Run a named batch, inspect/apply its emitted patch. Source evidence and approval
are recorded in tasks/verified_tasks/MAINTENANCE_REPORT.md section 10.
"""
import argparse
import difflib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'tasks/verified_tasks'
CHANGES = {}
FILTER = ''
IDS = {p.name[6:11]: p.name for p in (BASE/'paper_reproduction').glob('paper_*')}


def packages(prefix):
    if FILTER and not prefix.startswith(FILTER) and not FILTER.startswith(prefix):
        return []
    paper = next(v for v in IDS.values() if v.startswith('paper_'+prefix))
    return [p for mode in ('autonomous_research','paper_reproduction') if (p:=BASE/mode/paper).is_dir()]


def read(path):
    return CHANGES.get(path, path.read_text() if path.exists() else '')


def put(path, content):
    CHANGES[path] = content


def load(path):
    return json.loads(read(path))


def save(path, obj):
    put(path, json.dumps(obj, ensure_ascii=False, indent=2)+'\n')


def replace(path, old, new):
    s = read(path)
    if old not in s:
        if new in s:
            return
        raise ValueError(f'Missing anchor in {path}: {old[:90]}')
    put(path, s.replace(old, new))


def instruction(p, paragraph):
    path = p/'agent_input/task.md'
    if paragraph not in read(path):
        replace(path, '# Deliverables', paragraph+'\n\n# Deliverables')


def note(p, text):
    path = p/'evaluation/task_provenance/maintenance_audit.md'
    marker = '## 已批准修复记录（2026-09-16）'
    s = read(path)
    if text in s:
        return
    if marker in s:
        put(path, s+'\n- '+text+'\n')
    else:
        put(path, '# 当前实施状态\n\n'+marker+'\n\n'+text+'\n\n本包仍在 verified_tasks；未新增量化计算，未批准迁移。下方保留审批前历史，若与本节冲突以本节为准。\n\n---\n\n'+s)


def private_contract(p, text, select=lambda x: True):
    for name, key in [('reference_key_points.json','items'),('reference_conclusions.json','items'),('scoring_rules.json','rules')]:
        path=p/'evaluation'/name
        obj=load(path)
        for item in obj[key]:
            if not select(item):
                continue
            if name=='scoring_rules.json':
                binding=item.setdefault('binding',{})
                old=binding.get('comparison','')
                if text not in old:
                    binding['comparison']=old+' '+text
            elif isinstance(item.get('expected'),str):
                if text not in item['expected']:
                    item['expected']+=' '+text
            else:
                old=item.get('statement','')
                if text not in old:
                    item['statement']=old+' '+text
        save(path,obj)


def contracts():
    for p in packages('d2d08'):
        instruction(p,'Match S0/S1 physical modes using atom-mapped displacement or local-coordinate evidence before interpreting shifts; equal integer mode numbers alone do not establish correspondence. Retain mixed modes, mode reordering, near-zero shifts and supported exceptions. Missing experimental peaks remain missing and never contribute zero errors.')
        if p.parent.name=='paper_reproduction':
            path=p/'evaluation/reference_key_points.json'; obj=load(path)
            for x in obj['items']:
                if x['key_point_id']=='pr_result_state_shifts':
                    x['statement']='Test the source trend of xanthene-associated redshifts and carboxyphenyl-associated blueshifts after physical displacement matching; this is not a universal rule for every numbered or mixed mode.'
                    x['expected']='Evidence-based finite trends, with supported exceptions, mode exchanges, mixed character and near-zero changes explicitly retained. Correct exceptions must not be marked wrong solely for violating the generalization.'
            save(path,obj)
            private_contract(p,'Frequency shifts refer to physically matched displacements, not integer labels. Mixed modes and supported exceptions are valid; no universal red/blue direction or strict maximum error below 3 cm-1 is implied.',lambda x: any(w in json.dumps(x) for w in ('shift','final','trend')))
        note(p,'已确认保留给定两态结构；明确位移匹配、换序、混合/近零模式及实验缺测处理，PR 趋势不再强制每一模式同向。既有两态频率证据保留。')

    for p in packages('6f9a'):
        task=p/'agent_input/task.md'
        if p.parent.name=='paper_reproduction':
            instruction(p,'The primary comparison protocol is B3LYP-D3(BJ)/6-31G(d,p), IEFPCM acetonitrile geometry optimization and frequency validation, followed on each corresponding optimized complete-system geometry by M06-2X-D3/def2-TZVP with SMD acetonitrile and Mulliken population analysis. Equivalent software implementations are allowed. Select conformers by a declared structural/energy policy, not their charge agreement. Other protocols are sensitivity results, not interchangeable primary reference charges.')
            private_contract(p,'Primary numeric charges require the stated two-level complete-system Mulliken protocol and correct atom environments; do not apply this gold to other population schemes or a differently defined system.')
        else:
            replace(task,'If you use one starting geometry, justify why broader coverage is immaterial for this fixed comparison.','If you use one starting geometry, justify that finite scope, report checks actually performed, and explicitly retain unresolved conformer/ion-pair uncertainty; do not claim untested broader coverage is immaterial.')
            replace(task,'Stop when the fixed systems are covered and additional conformers no longer change the reported scientific conclusion under your stated criterion; report residual uncertainty rather than inventing certainty.','Stop after the declared finite coverage/budget is exhausted or the stated convergence criterion is met, and report the evidence and residual uncertainty. Untested sensitivity is a limitation, not evidence of robustness.')
            private_contract(p,'A single-conformer result establishes only that comparison. Score sensitivity only where actually tested; disclosing uncertainty is not evidence of invariance or a substitute for missing sensitivity.',lambda x: any(w in json.dumps(x).lower() for w in ('sensitiv','coverage','robust','final')))
        note(p,'PR 补无答案两层级 Mulliken 主协议；AR 单构象不再被要求证明全构象不变性，未做敏感性仍不能取得稳健性证据分。原量和容差未改。')

    for p in packages('5ea49'):
        path=p/'agent_input/submission_schema.json'; obj=load(path)
        cand=obj['result_schema']['properties']['candidates']['items']
        freq=cand['properties']['stationary_point_test']['properties']['imaginary_frequency_count']
        freq['type']=['integer','null']
        freq['description']='Null only when no frequency/Hessian outcome is available; candidate diagnostics must explain why. A selected successful minimum requires an actual validated stationary-point result.'
        cand.setdefault('allOf',[]).append({'if':{'properties':{'stationary_point_test':{'properties':{'imaginary_frequency_count':{'type':'null'}},'required':['imaginary_frequency_count']}},'required':['stationary_point_test']},'then':{'properties':{'diagnostics':{'type':'string','minLength':1}}}})
        save(path,obj)
        instruction(p,'For a failed/uncomputed candidate, use null for an unavailable imaginary-frequency count and explain the missing stage in diagnostics; retain actual counts whenever computed. A successful selected minimum must have genuine stationary-point evidence. Never substitute zero for unknown. The selected candidate ID must resolve to that validated candidate.')
        if p.parent.name=='paper_reproduction':
            instruction(p,'Use gas-phase B3LYP/6-311+G(d,p) for the primary optimized-geometry/frontier-orbital comparison; retain the specified E molecular identity. Other methods may be reported separately as sensitivity. Choose representative valid minima by the declared energy/structure policy, not by orbital agreement with an external answer.')
        private_contract(p,'Uncomputed candidate frequencies may be null with diagnostics, but the selected successful minimum must resolve to real stationary-point evidence. Unknown is not zero; candidate or selected-ID inconsistency is not success.')
        note(p,'修复候选级未求 Hessian 的 null/诊断表示；成功选中候选仍要求真实验证。PR 主协议选正文直接计算描述的 B3LYP/6-311+G(d,p)；另一处 6-31+G(d,p) 属原文冲突，未因本地数值选择方法。')

    for p in packages('e31cc'):
        private_contract(p,'Check the existing numeric tolerance jointly with positive E(beta)-E(alpha), alpha lower, and consistency with both submitted absolute electronic energies. A small negative value inside the numerical interval does not reproduce the reference ordering; do not change the original tolerance or weights.',lambda x: any(w in json.dumps(x).lower() for w in ('energy','relative','final','con_ar')))
        note(p,'已确认两给定 cis 异构体；私有规则联合核对数值、符号、两绝对电子能和能序，不将答案能序加入公开输入，未改原容差。')

    for p in packages('b3367'):
        if p.parent.name!='autonomous_research':
            note(p,'保留既有 PR 作者待检验 β-scission 路线和原势垒；核对同支原子/能量零点，不扩充通道或重算。')
            continue
        path=p/'evaluation/scoring_rules.json'; obj=load(path)
        for r in obj['rules']:
            if r['rule_id']=='ar_r4':
                r['binding']['comparison']='Apply 9.07 +/- 2 kcal/mol ONLY to an atom-balanced, frequency/path-validated acetophenone + ethyl radical channel, verified by mapped product connectivity and cleavage, not a channel label alone. For a different valid beta-scission channel this numeric reference is inapplicable, not a numerical failure: judge its result from the actual mapped TS/reactant energies, thermal convention, connection evidence and within-scope comparison, without inventing a new reference barrier. A coincidentally matching number for the wrong channel is not evidence for the source channel. This is an expert rule, not an implemented JSON predicate.'
        save(path,obj)
        private_contract(p,'The AR objective remains open-channel within the declared finite search: a different validated channel is not automatically wrong for differing from the author. Evaluate identity, atom/spin balance, TS connection, common free-energy convention and comparative evidence; no claim of global optimality follows from the single historical source channel.',lambda x: x.get('rule_id')!='ar_r4')
        note(p,'按最新批准保留 AR 开放通道成功范围（覆盖旧方案收紧建议）；作者势垒只对指定化学通道适用，其他真实有效通道由证据评价，不修改全局评分权重或伪造数字金标。')

    for p in packages('46a9c'):
        task=p/'agent_input/task.md'
        s=read(task).replace('do not assume their geometry, software, model chemistry, state ordering, or numerical result.','do not assume their geometry, state ordering, or numerical result; the primary reproduction protocol below defines the quantitative comparison.')
        put(task,s)
        instruction(p,'Use an implicit acetonitrile environment; excluding solvent molecules means no explicit solvent, not gas phase. Examine the low-lying sextet excited-state manifold, report at least the three largest oscillator strengths, and select the largest-f physical state in that manifold for the primary analysis. Resolve near degeneracy/state mixing with reported physical character and coverage, never by closeness to a charge-transfer target or by a fixed software state number. The common primary IFCT convention is a Mulliken-like transition-density decomposition into three disjoint fragments: all four Cl ligands, Fe, and the complete TEA+ cation. LMCT means Cl -> Fe and MLCT Fe -> Cl. Normalize over all fragment-to-fragment channels (including local channels); report the full matrix/normalization in supporting analysis. Other partitions/population schemes are sensitivity only.')
        if p.parent.name=='paper_reproduction':
            instruction(p,'Primary author-route protocol: B3LYP-D3(BJ), SDD basis/ECP for Fe and 6-31G(d) for other atoms, SMD(MeCN) optimization/frequencies; M06-D3, Fe SDD and other-atom 6-311+G(d,p), implicit MeCN for 30 sextet TD states. Use the highest-f selection rule above, not an author state index. Disclose the solvent-response implementation and equivalent software settings.')
        path=p/'agent_input/data/inputs/catalyst_system.json'; obj=load(path)
        obj['environment']={'solvent':'acetonitrile','representation':'implicit continuum','explicit_solvent':False}
        obj['measurement_protocol']={'representative_state':'highest oscillator strength in the documented low-lying sextet manifold; retain top three and full examined list','IFCT':'Mulliken-like transition-density fragment decomposition','fragments':['all four Cl','Fe','complete TEA+'],'LMCT':'Cl -> Fe','MLCT':'Fe -> Cl','normalization':'all fragment-to-fragment channels including local channels','state_index_is_not_an_answer':True}
        save(path,obj)
        private_contract(p,'Compare only the highest-f physical state in the covered low-lying sextet manifold, using implicit MeCN and the declared Cl/Fe/TEA+ Mulliken-like IFCT partition with all-channel normalization. State numbering is not invariant. Other schemes/states are sensitivity, not the same gold. Do not choose a state by closeness to 62.4/4.3%.')
        note(p,'明确隐式 MeCN、最高 f 选态和三片段 Mulliken-like IFCT。SI S34–S35 最高 f 原则在现有 TD30 输出选择 state20；既有 state20 IFCT 63.541/3.820% 可供核查，不把 state22 历史输出改名。布居口径为负责人批准的 benchmark 约定，不冒称原文唯一规定。')
        path=p/'evaluation/verified_computation_reference.md'
        put(path,read(path)+'\n\n## 当前获准的选态口径（非新增计算）\n\nSI S34–S35 按最高振子强度选择代表态，而非固定编号。现有 TD30 的最大 f 在 state20；既有 `docs/verification/group_4/paper_46a9ca0dab36dd9e/provenance/ifct_closure_20260915.json` 索引保留其 Mulliken-like LMCT=63.541%、MLCT=3.820%，满足原数值范围。此前分析 state22 的历史仍按其真实编号保留，不能当成按最高 f 规则选出的主态。本次没有新 TD/IFCT 计算；主布居口径为负责人批准的比较定义。\n')


def seven_a():
    import fitz
    mapped='[CH3:10][c:9]1[n:22][n:21](-[c:6]2[cH:5][cH:4][cH:3][cH:2][cH:1]2)[c:7]([O:27][c:11]2[cH:12][cH:13][c:14]([Cl:29])[cH:15][cH:16]2)[c:8]1[CH:17]=[N:23][N:24]1[C:18](=[S:28])[NH:25][N:26]=[C:19]1[CH3:20]'
    doc=fitz.open(ROOT/'papers/paper_a3968806251093cd/documents/supplementary_001.pdf')
    rows=[]
    for page,kind,unit in [(7,'bond','Angstrom'),(8,'angle','degree'),(9,'torsion','degree')]:
        lines=[s.strip().replace('–','-') for s in doc[page].get_text().splitlines()]
        seen=set()
        for i,s in enumerate(lines):
            if not re.fullmatch(r'(?:Cl|[CONS])\d+(?:-(?:Cl|[CONS])\d+){1,3}',s) or s in seen: continue
            val=lines[i+1]; m=re.fullmatch(r'(-?\d+\.\d+)\((\d+)\)',val)
            assert m,(s,val)
            rows.append((kind,s,float(m[1]),int(m[2])*10**(-len(m[1].split('.')[1])),unit,f'SI Table S{page-6}, PDF page {page+1}',val));seen.add(s)
    assert len(rows)==47 and sum(x[0]=='bond' for x in rows)==13
    import csv as csv_module
    import io
    buffer=io.StringIO()
    writer=csv_module.writer(buffer,lineterminator='\n')
    writer.writerow(['kind','selector','experimental_value','reported_standard_uncertainty','unit','source','source_notation'])
    writer.writerows(rows)
    csv=buffer.getvalue()
    for p in packages('a3968'):
        path=p/'agent_input/data/inputs/molecule.json'; obj=load(path)
        obj['smiles']=mapped;obj['smiles_representation']='Explicit atom-mapped graph; atom-map numbers are stable graph IDs, not coordinate row numbers.'
        obj['identity_definition']='Pyrazole ring N1-N2-C9-C8-C7: N1-phenyl(C6), C7-O1-chlorophenyl(C11), C8-C17 imine, C9-C10 methyl. Triazole thione ring N4-C18(S1)-N5(H)-N6-C19(C20). Preserve this connectivity, neutral charge and singlet state.'
        save(path,obj)
        path=p/'agent_input/data/inputs/atom_map.json';obj=load(path)
        obj['label_to_atom_map_number']={**{f'C{i}':i for i in range(1,21)},**{f'N{i}':20+i for i in range(1,7)},'O1':27,'S1':28,'Cl1':29,'Cl2':29}
        obj['alias_note']='Cl1 in SI Table S1 and Cl2 in Tables S2/S3 and the main structural description denote the same single chlorine attached to C14. They are not two atoms.'
        obj['label_convention']='Map these source labels through the mapped SMILES atom IDs to your submitted coordinate rows; preserve all 47 unique selectors (13 bonds, 23 angles, 11 torsions).'
        save(path,obj);put(p/'agent_input/data/inputs/experimental_geometry.csv',csv)
        task=p/'agent_input/task.md';s=read(task)
        s=s.replace('crystal coordinates and all experimental values are withheld.','crystal coordinates and author-computed geometry columns are withheld; pure SCXRD measurements are supplied in `data/inputs/experimental_geometry.csv`.')
        s=s.replace('against the withheld crystallographic reference','against the supplied experimental geometry table')
        s=s.replace('explicit Kekule spelling; same thione C=S connectivity','source-label atom mapping; neutral thione C=S connectivity')
        put(task,s)
        instruction(p,'Compute MAE and RMSE separately for bond lengths, angles and torsions on the 13/23/11 unique rows. Use the minimum absolute circular difference for torsions. Report row coverage and preserve missing rows as failures, not zero error. Do not combine Angstrom and degree errors into an undeclared overall score or invent weights to favor a model. If the per-kind comparisons do not support an unambiguous overall preference, report the mixed/undetermined result. Model or row failures may use null metrics with explicit reasons and counts; complete results require both validated models and every required comparison.')
        if p.parent.name=='paper_reproduction':
            instruction(p,'For the primary reproduction comparison use B3LYP and CAM-B3LYP, each with 6-311+G(d,p), for the isolated gas-phase neutral singlet thione. Other methods are supplementary, not replacements for this primary pair. No model ranking is supplied.')
        path=p/'agent_input/submission_schema.json';obj=load(path);rs=obj['result_schema']
        for key in ('observables','metrics'): rs['properties'][key]['minItems']=0
        for key in ('mae','rmse'): rs['properties']['metrics']['items']['properties'][key]['type']=['number','null']
        rs['properties']['failure_reason']={'type':'string','minLength':1}
        rs.setdefault('allOf',[]).extend([
            {'if':{'properties':{'status':{'const':'complete'}}},'then':{'properties':{'observables':{'minItems':94},'metrics':{'minItems':6,'items':{'properties':{'mae':{'type':'number'},'rmse':{'type':'number'},'n_rows':{'minimum':1}}}},'models':{'items':{'properties':{'converged':{'const':True},'stationary':{'const':True}}}}}}},
            {'if':{'properties':{'status':{'const':'bounded_failure'}}},'then':{'required':['failure_reason']}}
        ]);save(path,obj)
        private_contract(p,'Require the corrected source-labeled 7a graph; old positional-isomer results cannot certify it. Compute 13/23/11 unique-row metrics separately with circular torsion differences. Do not combine unlike units or manufacture a global winner. Preserve the source model hypothesis, but an overall ranking unsupported by the correct-object per-kind evidence is unresolved rather than an automatic success. Complete comparisons require all rows for both valid models; failures may have null metrics with diagnostics.')
        ref=p/'evaluation/verified_computation_reference.md'
        put(ref,'# 当前证据适用性：正确 7a 尚未由下方历史链认证\n\n正文 PDF p4 明确 pyrazole N1–N2–C9–C8–C7 的取代位置。此前两条主要成功 Opt/Freq 与 7a_repaired 模型属于不同位置异构体。当前已按正文/SI修复公开图和47行纯SCXRD比较输入，但这不改变旧计算对象。下方保留历史步骤供追溯，不是正确7a的成功验证；未经正确对象存量证据复核，不得使用旧PASS认证当前任务。没有新增计算、没有修改group原记录。\n\n---\n\n'+read(ref))
        note(p,'已按正文 p4/SI S1–S3 修正 pyrazole 取代图、重建标签到图原子的映射；Cl1/Cl2 为 C14 上同一氯的来源别名。补纯实验47行及原文括号不确定度，删除公开侧要求对隐藏值算误差的矛盾；PR 明确方法对。旧错对象链暂不能认证修正后任务，整体优劣仍不造跨单位权重。')


def z1():
    import fitz
    doc=fitz.open(ROOT/'papers/paper_80cc1ffb2cf73fc5/documents/supplementary_001.pdf'); ds=doc[0].get_drawings()
    curve=ds[1165]; assert len(curve['items'])==949 and curve['color']==(0.,0.,0.) and curve['fill'] is None
    x0=ds[3]['items'][0][1].x;x1=ds[19]['items'][0][1].x
    y0=ds[90]['items'][0][1].y;y1=ds[96]['items'][0][1].y
    points=[curve['items'][0][1]]+[item[2] for item in curve['items']]
    rows=[(19300+(v.x-x0)*800/(x1-x0),(y0-v.y)*.15/(y0-y1)) for v in points]
    rows=[(x,y) for x,y in rows if 19400<=x<=20100]
    assert len(rows)>750
    csv='wavenumber_cm_minus_1,action_signal_arb_unit\n'+''.join(f'{x:.4f},{y:.7f}\n' for x,y in rows)
    data_note={'data_kind':'Published experimental black polyline recovered from vector Figure S1, SI PDF page 1; not original detector data, fitted Gaussian peaks or a theoretical FC curve.','source_doi':'10.1039/d5cp04796j','units':{'x':'cm^-1','y':'arbitrary action signal'},'source_columns':'Black measured action trace only; blue fit and red continuum fit excluded.','digitization':'Affine calibration from printed vector tick positions (19300,20100 cm^-1; 0.00,0.15 signal). Vertices and repeated x values retained; no interpolation, smoothing or invented uncertainty bars.','precision_note':'Decimal formatting reflects PDF vector extraction, not experimental precision. Noise, sampling and line-rendering limitations remain; any peak picking must state its rule.','experimental_alignment_origin_cm_minus_1':19444,'alignment':'Use observed lowest resonance as relative zero and own calculated 0-0 as calculated zero. This does not predict absolute detachment energy.','point_count':len(rows)}
    for p in packages('80cc1'):
        put(p/'agent_input/data/inputs/experimental_spectrum.csv',csv)
        save(p/'agent_input/data/inputs/experimental_spectrum_metadata.json',data_note)
        path=p/'agent_input/data/inputs/problem_definition.json';obj=load(path)
        obj['experimental_data']='experimental_spectrum.csv';obj['experimental_metadata']='experimental_spectrum_metadata.json'
        obj['relative_alignment']={'experimental_origin_cm_minus_1':19444,'calculated_origin':'own calculated 0-0 transition','fixed_author_calculated_shift':None,'scope':'Z1-only; relative spacings/features, not absolute detachment accuracy or multi-isomer fitting'};save(path,obj)
        task=p/'agent_input/task.md';s=read(task)
        s=s.replace('The public package contains no numerical experimental peak trace; do not invent observed peak positions. If pointwise observations are unavailable, report that limitation and compare calculated coverage and relative progression qualitatively.','The public package supplies the measured black trace extracted from the published vector figure in `experimental_spectrum.csv`, with extraction limitations in its metadata. Compare relative prominent features using a declared peak-selection rule, retaining unmatched peaks and noise limitations.')
        s=s.replace('and `data/inputs/problem_definition.json`.','and `data/inputs/problem_definition.json`, together with the experimental spectrum CSV and metadata.')
        s=s.replace('Compare available observations or explain why pointwise matches cannot be extracted','Compare the supplied experimental observations and explicitly explain any unresolved or unreliable matches')
        s=s.replace('compare available observations (or explain why pointwise matches cannot be extracted)','compare the supplied experimental observations, retaining unmatched features and any unreliable matches')
        put(task,s)
        instruction(p,'Use the experimental lowest-resonance origin (19444 cm^-1) as the relative observed zero and your own calculated 0-0 transition as the relative calculated zero. Determine the required translation from your calculation; no author-computed translation is supplied. Compare the prominent spacings/features, not absolute detachment accuracy; this is the Z1-only comparison, not a two-isomer fit. Identify active modes by physical displacement/FC evidence rather than a mandatory integer index. Do not claim unavailable observations or fabricate error bars. An evidence-based disagreement is a legitimate submission, but is not automatically a successful reproduction of the reference interpretation.')
        private_contract(p,'The public experimental black trace is now available (vector Fig S1 extraction, not raw detector data or the fitted curve). Compare Z1-only relative spectra after the declared observed-origin/calculated-0-0 alignment. No absolute-origin accuracy, all-peak agreement, or fixed software mode number is required. Identify the physical in-plane-bending mode by displacement/FC evidence. Honest disagreement can earn evidence/process credit but is not automatically reproduction of the reference result; never fabricate experimental matches.')
        note(p,f'保留获准的 Z1 anion；从 SI Fig S1 的独立黑色实验向量路径提取 {len(rows)} 个窗口顶点，排除蓝色拟合、红色背景和理论曲线，不用理论结果制造实验峰。按坐标刻度还原，保留重复x及噪声，非原始探测数据。公开相对零点与比较规则，无作者计算移位；未新增量化计算。')
        path=p/'evaluation/task_provenance/experimental_extraction.json'
        save(path,{'source':'papers/paper_80cc1ffb2cf73fc5/documents/supplementary_001.pdf','page':1,'drawing_index':1165,'line_segments':949,'black_stroke':[0,0,0],'fill':None,'x_tick_page_coordinates':[x0,x1],'x_tick_values':[19300,20100],'y_tick_page_coordinates':[y0,y1],'y_tick_values':[0,.15],'public_vertices':len(rows),'no_theoretical_curve':True,'no_fitted_background':True,'source_conflict':'SI p1 prose detachment value 16400 is inconsistent with its plot and main text; not adopted as an input threshold. Main text observed lowest resonance 19444 used only as approved alignment datum.'})


def emit():
    parts=[]
    for path,new in CHANGES.items():
        old=path.read_text() if path.exists() else None
        rel=path.relative_to(ROOT).as_posix()
        if old==new: continue
        if new is None:
            parts.append('*** Delete File: '+rel+'\n')
        elif old is None:
            parts.append('*** Add File: '+rel+'\n'+''.join('+'+s+'\n' for s in new.splitlines()))
        else:
            diff=list(difflib.unified_diff(old.splitlines(),new.splitlines(),n=3,lineterm=''))[2:]
            parts.append('*** Update File: '+rel+'\n'+'\n'.join('@@' if s.startswith('@@') else s for s in diff)+'\n')
    print('*** Begin Patch\n'+''.join(parts)+'*** End Patch')


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('batch',choices=['contracts','seven_a','z1']);ap.add_argument('--paper',default='');args=ap.parse_args()
    FILTER=args.paper
    globals()[args.batch]();emit()
