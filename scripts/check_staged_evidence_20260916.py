#!/usr/bin/env python3
"""Read-only scientific postprocessing; emits patches only for private records."""
import argparse
import csv
import json
import re
from pathlib import Path
import staged_task_repair_20260916 as r
from finish_staged_repairs_20260916 import reference_note


def seven_a():
    from rdkit import Chem
    from rdkit.Chem import rdDetermineBonds
    import networkx as nx
    root=r.ROOT/'docs/verification/group_2/paper_a3968806251093cd'
    obj=r.load(r.packages('a3968')[0]/'agent_input/data/inputs/molecule.json')
    target=Chem.AddHs(Chem.MolFromSmiles(obj['smiles']))
    def graph(m):
        g=nx.Graph();g.add_nodes_from((a.GetIdx(),{'element':a.GetSymbol()}) for a in m.GetAtoms());g.add_edges_from((b.GetBeginAtomIdx(),b.GetEndAtomIdx()) for b in m.GetBonds());return g
    gt=graph(target);records=[]
    for path in sorted(root.rglob('*')):
        if path.suffix not in ('.log','.out','.xyz','.sdf','.com','.gjf') or not path.is_file():continue
        s=path.read_text(errors='replace');xyz=None;mol=None
        if path.suffix=='.xyz':xyz=s
        elif path.suffix=='.sdf':mol=Chem.MolFromMolBlock(s.split('$$$$')[0],removeHs=False)
        elif path.suffix in ('.log','.out'):
            matches=list(re.finditer(r'(?:Standard|Input) orientation:\s*\n\s*-+\n.*?\n\s*-+\n(.*?)\n\s*-+',s,re.S))
            if matches:
                rows=[line.split() for line in matches[-1][1].splitlines()]
                try:xyz=str(len(rows))+'\nlast output geometry\n'+'\n'.join(Chem.GetPeriodicTable().GetElementSymbol(int(t[1]))+' '+' '.join(t[3:6]) for t in rows)+'\n'
                except (ValueError,RuntimeError):continue
        else:
            m=re.search(r'^\s*-?\d+\s+\d+\s*\n((?:(?:[A-Za-z]{1,2}|\d+)\s+[-\d.]+\s+[-\d.]+\s+[-\d.]+\s*\n)+)',s,re.M)
            if m:
                lines=m[1].strip().splitlines();xyz=f'{len(lines)}\ninput geometry\n'+'\n'.join(lines)+'\n'
        if xyz:
            mol=Chem.MolFromXYZBlock(xyz)
            if mol:rdDetermineBonds.DetermineConnectivity(mol)
        if not mol:continue
        isomorphic=nx.is_isomorphic(gt,graph(mol),node_match=lambda a,b:a['element']==b['element'])
        records.append({'path':path.relative_to(r.ROOT).as_posix(),'atoms':mol.GetNumAtoms(),'correct_element_connectivity_graph':isomorphic,'normal_termination_in_log':'Normal termination of Gaussian' in s,'scope':'last recoverable geometry; element-labelled graph comparison, not only molecular formula'})
    good=[x for x in records if x['correct_element_connectivity_graph']]
    evidence={'question':'Do the available historical structures/output geometries belong to corrected 7a?','matching_method':'RDKit distance connectivity (or SDF bonds) vs full source-labelled graph; element-labelled graph isomorphism, all H included; no target fit','records_checked':len(records),'matching_records':len(good),'correct_object_successful_logs':[x['path'] for x in good if x['normal_termination_in_log']],'records':records,'limitation':'Files with no recoverable Cartesian geometry are not identity-certified by this check; no original verification files changed.'}
    for p in r.packages('a3968'):
        r.save(p/'evaluation/task_provenance/identity_evidence_check_20260916.json',evidence)
        reference_note(p,f'追加存量身份检索：已检查 group_2 本篇目录下 {len(records)} 份可恢复 XYZ/SDF/输入/日志末态的原子连接图，符合修正后 7a 完整元素标记图的记录为 {len(good)}；其中正常终止正确对象日志 {len(evidence["correct_object_successful_logs"])} 份。详情在 task_provenance/identity_evidence_check_20260916.json。不能以错位置异构体的正常终止或 132 实频认证当前 7a；没有新计算。')
        r.note(p,f'已扩大检索至包含被 Git 忽略的历史日志/输入：{len(records)} 份有几何记录，正确对象匹配 {len(good)} 份。当前正确对象验证缺口不能靠修改 reference/名称消除；未更改 group 或发起重算。')


def spectrum():
    import numpy as np
    from scipy.signal import find_peaks
    p=r.packages('80cc1')[0]
    rows=list(csv.DictReader((p/'agent_input/data/inputs/experimental_spectrum.csv').open()))
    a=np.array([[float(z['wavenumber_cm_minus_1']),float(z['action_signal_arb_unit'])] for z in rows]);a=a[np.argsort(a[:,0],kind='stable')]
    x=np.unique(a[:,0]);y=np.array([a[a[:,0]==i,1].mean() for i in x]);gx=np.arange(19400.,20101.);gy=np.interp(gx,x,y)
    idx,_=find_peaks(gy,prominence=.02,distance=25);peaks=gx[idx]
    src=r.ROOT/'docs/verification/group_1/paper_80cc1ffb2cf73fc5/artifacts/fc_closure_20260914/fc_analysis.json';fc=json.loads(src.read_text())['base']
    sticks=[t for t in fc['transitions'] if 19400<=19444+t['relative_cm1']<=20100]
    matches=[]
    for t in sticks:
        pred=19444+t['relative_cm1'];k=int(np.argmin(abs(peaks-pred)));obs=float(peaks[k]);matches.append({'FC_transition':t['final'],'calculated_relative_cm1':t['relative_cm1'],'aligned_calculated_cm1':pred,'strength':t['strength'],'nearest_selected_experimental_cm1':obs,'residual_cm1':pred-obs})
    evidence={'kind':'postprocessing of existing FC outputs and newly supplied source experiment, NOT a new FC/quantum calculation','source_fc':src.relative_to(r.ROOT).as_posix(),'experimental_source':'published black measured trace in SI Figure S1, vector extraction','alignment':{'experimental_origin_cm1':19444,'existing_calculated_00_cm1':fc['origin_cm1'],'derived_translation_cm1':19444-fc['origin_cm1'],'absolute_detachment_accuracy_claimed':False},'diagnostic_peak_rule':'For this audit only: sort vertices, average repeated x, linear interpolate on 1 cm-1 grid, scipy find_peaks prominence 0.02 signal units and minimum separation 25 cm-1. Public raw vector vertices are unchanged. This is not a new evaluator threshold or fitted measurement uncertainty.','observed_selected_peaks_cm1':[float(i) for i in peaks],'matches':matches,'matching_limitations':'All archived FC transitions within the window are listed. Nearest-peak association is diagnostic, not a unique physical assignment; unmodeled observed bands remain. No universal all-peak agreement or absolute energy accuracy is asserted.','existing_physical_progression':{'reference_mode_number':3,'scaled_frequency_cm1':85.9573,'huang_rhys':fc['huang_rhys']['3']},'interpretation':'Existing FC evidence supports a prominent relative in-plane progression and some higher-window features, while substantial observed features/intensity differences remain. This is the approved bounded Z1-only claim, not full experimental spectrum reconstruction.'}
    table='| FC branch | Aligned calculated cm⁻¹ | Nearest selected experimental cm⁻¹ | Difference cm⁻¹ |\n|---|---:|---:|---:|\n'+''.join(f'| {z["FC_transition"]} | {z["aligned_calculated_cm1"]:.3f} | {z["nearest_selected_experimental_cm1"]:.1f} | {z["residual_cm1"]:+.3f} |\n' for z in matches)
    text='补入的实验来自 SI Fig S1 独立黑色实测向量线，不是拟合或理论曲线。本次仅解析既有 FC 结果：0–0=18926.1908 cm⁻¹ 与实验最低峰 19444 cm⁻¹ 作相对零点对齐，得到本次后处理平移 517.8092 cm⁻¹（不作为公开常数）。没有重算 FC、没有拟合新的金标/容差。\n\n以下为全部窗口内已存 FC 跃迁的最近实验突出峰诊断，不是唯一逐峰归属；实验选峰规则及所有 13 个实验突出峰见 task_provenance/experimental_comparison_20260916.json。\n\n'+table+'\n前四个低能进动和部分高窗特征与实验呈有限对应；19748、19844、19920 等强实验特征及强度差异仍不能全部由 Z1 唯一解释。保留 mode3 对应物理位移/HR=1.20932 的历史证据与未归属限制，不宣称全部峰吻合、绝对脱附能准确或双异构体拟合已验证。旧文中“尚无公开实验数据”的描述是当时状态，由本段补齐当前输入。'
    for p in r.packages('80cc1'):
        r.save(p/'evaluation/task_provenance/experimental_comparison_20260916.json',evidence);reference_note(p,text)
        r.note(p,'完成存量 FC 与新增纯实验曲线的相对对齐后处理；全部窗口内已存跃迁均列出，未匹配强峰/强度差异保留。支持获准的突出特征/物理进动有限结论，不把 Z1-only 写成全谱或绝对脱附能验证。')


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('batch',choices=['seven_a','spectrum']);a=ap.parse_args();globals()[a.batch]();r.emit()
