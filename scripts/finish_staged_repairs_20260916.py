#!/usr/bin/env python3
"""Emit bounded, approved task-package corrections as apply_patch; no jobs."""
import argparse
import copy
import json
import re
import staged_task_repair_20260916 as r


def reference_note(p, text):
    path=p/'evaluation/verified_computation_reference.md'
    if text not in r.read(path):r.put(path,r.read(path)+'\n\n## 2026-09-16 当前输入与历史计算的关系\n\n'+text+'\n')


def move_private(p, name):
    old=p/'agent_input/data/inputs'/name
    dst=p/'evaluation/author_results'/name
    if old.exists():
        assert not dst.exists() or dst.read_text()==old.read_text()
        r.put(dst,old.read_text());r.put(old,None)


def helicene():
    for p in r.packages('746'):
        move_private(p,'experimental_torsion_boundary.json')
        path=p/'agent_input/task.md';s=r.read(path)
        s=s.replace('the arithmetic mean, in degrees, of five individual inner-rim dihedrals','the mean of the absolute values, in degrees, of five individual inner-rim dihedrals')
        s=s.replace('the measured compound-5 mean torsion used only for structural calibration is supplied in `data/inputs/experimental_torsion_boundary.json`.','no experimental target angle is supplied. The evaluator, not the Agent, performs the comparison with its private experimental reference.')
        s=s.replace('their arithmetic mean','their mean absolute value')
        s=s.replace('arithmetic mean, uncertainty','mean absolute torsion, uncertainty').replace('use only the supplied measured calibration boundary if comparing with experiment.','no experimental target angle is supplied. The evaluator handles the private experimental comparison; the Agent reports its calculation and limitations.')
        s=s.replace('use one consistent signed or absolute convention, and state the arithmetic-mean formula','retain the signed values in a declared dihedral convention, and report mean_torsion_deg = sum(abs(phi_i))/5')
        s=s.replace('Interpret agreement with the experimental boundary only as a structural calibration, not universal proof of the method.','Interpret the calculated structure with its limitations. No access to the private experimental number is required; the evaluator compares the result as a structural calibration, not universal proof of the method.')
        r.put(path,s)
        r.instruction(p,'The XYZ is an independently embedded, unoptimized starter, not an author-optimized endpoint. `data/inputs/compound5_identity.json` supplies the mapped graph and the inner-rim chain [1,66,65,64,63,62,61,59]. Use its five consecutive quadruples, preserving the given molecular identity and source-labelled handedness; if you reorder atoms, supply a complete map back to these IDs. No optimized torsion magnitude was used to generate the starter. On bounded failure, unavailable imaginary-mode counts may be null with diagnostics; never use zero for unknown. A complete result with no frequency count must instead supply auditable equivalent minimum-test evidence in validation.equivalent_minimum_evidence.')
        path=p/'agent_input/submission_schema.json';obj=r.load(path);rs=obj['result_schema'];v=rs['properties']['validation']
        v['properties']['imaginary_modes'].update(type=['integer','null'],minimum=0)
        v['properties']['equivalent_minimum_evidence']={'type':'string','minLength':1}
        rs['properties']['failure_diagnostics']['minLength']=1
        rs['oneOf'][0]['properties']['candidate']={'properties':{'converged':{'const':True}}}
        rs['oneOf'][0]['properties']['validation']={'anyOf':[{'properties':{'imaginary_modes':{'type':'integer','minimum':0}},'required':['imaginary_modes']},{'properties':{'equivalent_minimum_evidence':{'type':'string','minLength':1}},'required':['equivalent_minimum_evidence']}]}
        rs['properties']['mean_definition']['description']='mean(abs(phi_i)) over the five fixed inner-rim quadruples; individual value_deg values remain signed.'
        r.save(path,obj)
        path=p/'task_info.json';obj=r.load(path);obj['data']=[x for x in obj['data'] if not x['path'].endswith('experimental_torsion_boundary.json')]
        if not any(x['path'].endswith('compound5_identity.json') for x in obj['data']):obj['data'].append({'path':'data/inputs/compound5_identity.json','description':'Mapped molecular graph and five inner-rim selectors; independent unoptimized XYZ starter, no target angle.'})
        obj['difficulty_reasons']=[x.replace('torsion definition','torsion extraction').replace('define the five torsions','extract the five specified torsions') for x in obj['difficulty_reasons']];r.save(path,obj)
        path=p/'paper_route.md';r.put(path,r.read(path).replace('the supplied starting geometry is the reported Cartesian structure.','the historical verification used the reported Cartesian structure; the current public geometry is independently embedded from its discrete identity and does not contain the endpoint coordinates.'))
        r.private_contract(p,'The primary metric is mean(abs(phi_i)) over the five consecutive quadruples of [1,66,65,64,63,62,61,59], with signed individual values and mapping retained. Unknown frequencies are not zero; completed minima require real frequency or equivalent evidence. The experiment is private: the evaluator compares the submitted mean with 27.0 degrees and its scope-limited interpretation; do not require the Agent to quote or access that withheld number.')
        if p.parent.name=='paper_reproduction':
            path=p/'evaluation/reference_key_points.json';obj=r.load(path)
            for x in obj['items']:
                if x['key_point_id']=='pr_result_calibration':x['expected']='The evaluator compares the submitted calculated mean with its private experimental 27.0-degree reference, considering validation and limitations. The Agent is not required to know, quote or compare that hidden number.'
            r.save(path,obj)
            path=p/'evaluation/scoring_rules.json';obj=r.load(path)
            for x in obj['rules']:
                if x['rule_id']=='pr_r5':
                    x['expected']='Evaluator-side comparison with the private experimental boundary, with a validated calculated structure and appropriately limited interpretation; no Agent access to the experimental number is expected.'
                    x['binding']['fields']=['$.mean_torsion_deg','$.validation','$.interpretation','$.limitations']
            r.save(path,obj)
        reference_note(p,'历史成功几何的五角按 mean(abs(phi)) 重提取为 27.09676855°，收紧优化检查为 27.09673780°，支持原 27.1±2° 金标。公开 XYZ 已改为 topology-only ETKDG 初始结构；原终态及实验 27.0° 只存 author_results。历史作者路线证据继续有效，但未声称从该新 starter 重做 Opt/Freq。')
        r.note(p,'已同步五角平均绝对值、完整图/原子映射、实验比较移交 evaluator；失败允许未知频率 null，成功必须有真实频率或等效最小值证据。实验边界文件从公开侧移入 author_results，可恢复；原数值/容差不变。')


def phosphorus():
    for p in r.packages('ef266'):
        path=p/'agent_input/task.md';s=r.read(path)
        s=re.sub(r'PA rows 1–51 come from.*?independently generated starter\.', 'All three XYZ files are independent topology-only, unoptimized embeddings. The companion *_identity.json files give the complete mapped graphs; atom-map IDs equal the one-based XYZ rows. No author endpoint fragment, optimized contact distance or target charge was used to build these starters.',s)
        r.put(path,s)
        path=p/'paper_route.md';s=r.read(path)
        s=s.replace('The public task supplies the full source-defined graph and explicitly labels the generated missing-fragment coordinates; they are not attributed to the author.','The current public task supplies the complete graphs and independently embedded starters for all three species. Historical partial-SI reconstruction is archived separately and is not the present public input.')
        r.put(path,s)
        path=p/'evaluation/task_provenance/structure_provenance.json'
        if path.exists():
            obj=r.load(path);obj['current_status']='Historical partial-SI preparation, superseded 2026-09-16. Current public coordinates are fully independently embedded; consult *_independent_preparation.json.';r.save(path,obj)
        r.instruction(p,'Use the explicit mapped graphs to establish P, each oxygen and every N-ethyl alpha/beta hydrogen; do not infer bond connectivity or charge solely from starter distances. The free, PO and PA systems contain 46, 56 and 61 atoms. All are net-neutral singlets; the PO and PA graphs explicitly retain the phosphonium/oxygen formal-charge separation. Relax the unoptimized geometry before interpreting distances or charges.')
        reference_note(p,'现有真实计算验证的是完整 free/PO/PA 模型（46/56/61 原子）的作者路线，不是当前新生成的 starter。2026-09-16 三份公开坐标全部由完整图独立嵌入；历史 SI/补全坐标保留于 author_results。保持接触定义、ADCH、signed ESP 和金标不变；未进行新量化计算。')
        r.note(p,'三个完整图/式/电荷和原子映射已核对，公开说明不再声称保留 SI 片段；保留现有接触、ADCH 与 ESP 指标。旧 structure_provenance 已明确标记历史，不再代表当前公开起点。')


def iron():
    for p in r.packages('44f'):
        path=p/'agent_input/task.md';s=r.read(path).replace('an 87-atom Cartesian geometry from SI Table S10','an independently embedded, unoptimized 87-atom Cartesian starter')
        r.put(path,s)
        r.instruction(p,'`data/inputs/1H_start_identity.json` gives the complete mapped graph: Fe1/Fe2 are rows 1/2; peroxo O3-O4 coordinates to Fe1/Fe2, respectively; O5 is the bridging mu-oxo. N6–N9 coordinate Fe1 and N10–N13 coordinate Fe2. Preserve the full susan ligand and this specified core identity, but optimize all distances; no Fe-Fe covalent bond or endpoint separation is imposed. The initial coordinates are not a minimum and must not be read as a Mössbauer or spin-energy result. Report the broken-symmetry initialization/local-spin evidence, not a closed-shell singlet substitution.')
        path=p/'agent_input/data/inputs/system.json';obj=r.load(path);obj['identity_note']='Atom IDs are one-based XYZ rows: Fe1/2; O3-O4 peroxo, O3->Fe1 and O4->Fe2; O5 mu-oxo bridges both. N6–9->Fe1 and N10–13->Fe2; complete graph in 1H_start_identity.json. No Fe-Fe covalent bond is prescribed.';obj['geometry_status']='independent topology-only unoptimized starter';r.save(path,obj)
        path=p/'task_info.json';obj=r.load(path)
        for x in obj['data']:x['description']=x['description'].replace('from SI Table S10','independently embedded from the defined graph').replace('SI-derived','independently embedded')
        r.save(path,obj)
        reference_note(p,'历史作者 Table S10 终态仅存 author_results/1H_start.xyz；当前独立 topology-only starter 明确区分 O3–O4 过氧与 O5 μ-oxo，并排除不合理短的非键合 O···O。保留已验证的 BS/HS、Fe···Fe 和 Mössbauer 计算及校准协议；没有重算新起点，也没有把构建几何写成已收敛结构。')
        r.note(p,'补完整 susan/过氧/μ-oxo 配位图及明确原子身份；独立嵌入使用通用配位和排斥边界，不用作者 Fe···Fe 距离。保留 +2 BS singlet、MeCN、HS 和 Mössbauer 协议，不把模型变成闭壳层。')


def insertion():
    p=r.packages('d796')[0]
    refs={
        'INT2A-quartet':{'file':'INT2A_quartet.xyz','Fe':36,'hydride_H':37,'terminal_alkyne_C':49,'terminal_alkyne_H':50,'substituted_alkyne_C':51,'substituent_CH2':52,'N_donor_plane':[5,14,21],'tert_butyl_quaternary_C':23},
        'INT2B-quartet':{'file':'INT2B_quartet.xyz','Fe':22,'hydride_H':23,'terminal_alkyne_C':35,'terminal_alkyne_H':36,'substituted_alkyne_C':37,'substituent_CH2':38,'N_donor_plane':[5,14,20],'tert_butyl_quaternary_C':55}}
    channels=[]
    for letter,ref,hydrogen_to in [('A','INT2A-quartet','terminal_alkyne_C'),('B','INT2A-quartet','substituted_alkyne_C'),('C','INT2B-quartet','terminal_alkyne_C'),('D','INT2B-quartet','substituted_alkyne_C')]:
        d=refs[ref];metal_to='substituted_alkyne_C' if hydrogen_to=='terminal_alkyne_C' else 'terminal_alkyne_C'
        channels.append({'label':'TS3'+letter+'-quartet','reference':ref,'approach_face':'same ligand face as the alkyne in '+d['file'],'hydride_transfer_to':hydrogen_to,'alkenyl_Fe_bond_to':metal_to,'bond_changes_in_reference_atom_ids':{'break':[[d['Fe'],d['hydride_H']]],'form':[[d['hydride_H'],d[hydrogen_to]]]},'bond_order_change':'alkyne C#C to alkenyl C=C; eta2 alkyne coordination becomes Fe-C to the non-hydrogenated carbon','required_mapping':'Use this reference XYZ order for your generated candidates, or provide explicit source-to-output atom mapping. Channel labels refer to chemistry/face, not which output energy is obtained.'})
    r.save(p/'agent_input/data/inputs/reaction_channels.json',{'atom_indexing':'one-based per-reference XYZ row; the two reference orders differ','atom_count':68,'charge':0,'multiplicity':4,'model':'L10-supported Fe hydride plus 4-phenyl-1-butyne; disilane is reaction context, not an extra constituent of these 68-atom insertion models','reactant_role':'given coordinated reactants, not target transition states','references':refs,'channels':channels,'face_definition':'Keep the ligand stereochemistry of each reference. The two supplied reactants encode the upper/lower ligand faces. To explore the other regiochannel on the same face, reorient the alkyne within that face; no author TS distance, torsion or product geometry is supplied. A face can be tracked by the signed scalar product of alkyne-midpoint minus Fe with the normal of the ordered N_donor_plane; report atom mapping and any change during refinement.','geometry_requirements':'Generate TS guesses independently from reactants and these proposed bond changes, then optimize and validate. No forming/breaking bond lengths or angles are prescribed.'})
    for label in 'ABCD':move_private(p,'TS3'+label+'_quartet.xyz')
    path=p/'agent_input/task.md';s=r.read(path)
    s=s.replace('Using the four supplied, labeled quartet starting geometries for TS3A-quartet, TS3B-quartet, TS3C-quartet, and TS3D-quartet, compute','Using the four proposed quartet insertion channels TS3A-quartet, TS3B-quartet, TS3C-quartet, and TS3D-quartet defined in `data/inputs/reaction_channels.json`, independently construct and locate their transition states and compute')
    start=s.index('The directory `data/inputs` contains four XYZ files')
    end=s.index('Refine and frequency-validate these references',start)
    s=s[:start]+'The public inputs are `reaction_channels.json` and the given coordinated-reactant geometries `INT2A_quartet.xyz` and `INT2B_quartet.xyz` in `data/inputs`. Both references are 68-atom, neutral quartet (multiplicity 4) models. The channel file defines atom roles, face and the two alternative alkyne insertion regiochannels per reactant. Preserve each reference atom order or supply an explicit mapping. No transition-state or product coordinates are supplied. '+s[end:]
    s=s.replace('the four named inputs','the four named proposed channels').replace('For every one of the four named candidates, perform','For every one of the four named channels, construct TS guesses from the mapped reactant and proposed bond changes, and perform').replace('all four supplied labels','all four defined labels').replace('belongs to the named 68-atom input','belongs to the named channel and its mapped 68-atom reactant model')
    r.put(path,s)
    r.instruction(p,'For the primary author-route comparison, optimize and compute frequencies at gas-phase M06L with SDD on Fe and 6-31G(d) on other atoms, and evaluate solvent electronic energies with M06L/6-311+G(d,p)-SDD and IEFPCM(THF). Use 298.15 K thermal terms and the stated two-thirds entropy convention: Gsol = Esol + Hcorr - (2/3)*(Hcorr-Gcorr). Hcorr and Gcorr are thermal corrections from the same low-level frequency calculation, not total energies. Other protocols are separately disclosed sensitivity. Report the local INT2 reference for each channel; do not add the dihydrodisilane molecule to these insertion models. An unavailable frequency count may be null only for an unvalidated failed candidate, with notes explaining the missing stage. Retain all genuinely computed imaginary frequencies.')
    path=p/'agent_input/submission_schema.json';obj=r.load(path);cand=obj['properties']['candidates']['items'];cand['properties']['input_provenance']['properties']['file']['description']='Public reactant file plus independently generated TS-guess artifact, not a supplied author TS file.'
    cand['properties']['frequency_validation']['properties']['imaginary_frequency_count'].update(type=['integer','null'],minimum=0)
    cand.setdefault('allOf',[]).extend([{'if':{'properties':{'frequency_validation':{'properties':{'imaginary_frequency_count':{'type':'null'}}}}},'then':{'properties':{'frequency_validation':{'properties':{'validated':{'const':False}}},'notes':{'type':'string','minLength':1}}}},{'if':{'properties':{'frequency_validation':{'properties':{'validated':{'const':True}}}}},'then':{'properties':{'frequency_validation':{'properties':{'imaginary_frequency_count':{'const':1}}}}}}]);r.save(path,obj)
    # This legacy package duplicates its result schema at top level.
    obj['result_schema']['properties']['candidates']['items']=copy.deepcopy(cand)
    r.save(path,obj)
    path=p/'task_info.json';obj=r.load(path);obj['data']=[{'path':'data/inputs','description':'Two given neutral quartet 68-atom INT2 reactants and four mapped insertion-channel definitions. TS coordinates are not public; construct guesses independently.'}];obj['difficulty_reasons'][0]='Four fixed chemical channels require independently generated TS guesses, successful searches and consistent local-reference frequency/free-energy validation.';r.save(path,obj)
    r.private_contract(p,'Current public inputs are INT2 reactants and mapped chemical channels, not author TS coordinates. A/C transfer hydride to terminal alkyne C and retain Fe at substituted C; B/D transfer hydride to substituted C and retain Fe at terminal C. A/B share INT2A face/reference, C/D INT2B. Source TS atom orders differ: compare roles through mappings, not bare indices. Preserve all four channels and local zeros. Missing frequency evidence cannot be zero or a validated TS; exactly one relevant imaginary mode remains required. Existing historical IRC MaxPoints outcomes are limitations, not newly imposed endpoint-minimum requirements.')
    reference_note(p,'2026-09-16 四个 SI TS 文件从 agent_input 移入 author_results；公开仅保留两个已给定 INT2 与 reaction_channels.json。正文 pp9–10/Fig6 和 SI 结构角色共同确认：A/C 为氢迁移至端位碳、B/D 至取代碳，A/B 与 C/D 分属两反应物配位面。旧 TS 原子顺序各异，不能按同一行号盲比。历史 20 阶段作者路线和局部势垒仍有效；未从当前公开反应物重新搜索 TS。八条历史 IRC 达 MaxPoints 的限制保留。')
    r.save(p/'evaluation/task_provenance/channel_mapping_check.json',{'source':'main.pdf pp9–10 Fig6; SI Cartesian TS3A–D quartet and INT2A/B tables','author_TS_roles_1based':{'A':{'Fe':36,'H':37,'terminal_C':49,'substituted_C':51},'B':{'Fe':36,'H':37,'terminal_C':50,'substituted_C':49},'C':{'Fe':22,'H':23,'terminal_C':35,'substituted_C':36},'D':{'Fe':22,'H':23,'terminal_C':36,'substituted_C':35}},'public_mapping':'uses INT2 order, not differing source TS orders','no_endpoint_distances_published':True})
    r.note(p,'四份 TS 终态已从公开侧移入 author_results，可恢复；新增无目标几何/能量的四路线及原子角色。保留两 INT2 反应物、quartet、局部零点和原势垒；PR 提供无答案热化学路线，失败未知频率不填零。')


def consistency():
    for p in r.packages('5ea49'):
        if p.parent.name=='paper_reproduction':
            path=p/'agent_input/task.md';s=r.read(path).replace('The numerical values, result direction, paper software, model chemistry, and ordered paper protocol are not supplied.','The numerical values and result direction are not supplied; the primary method is specified below.').replace("Choose and justify an electronic-structure method suitable for neutral heteroaromatic organic molecules without attempting to identify the paper's method.",'Use the primary method specified below and document implementation and numerical settings.')
            r.put(path,s)
            path=p/'task_info.json';obj=r.load(path);obj['difficulty_reasons'][-1]='The primary model chemistry is supplied, while conformer generation, validation, numerical choices and sensitivity must be justified.';r.save(path,obj)
        else:r.instruction(p,'Independent method selection does not change the definitions of orbital energies or waive numerical accuracy. Report method/conformer dependence and limitations; results from every defensible method are not asserted to be identical.')
    for prefix in ['6f9a','46a9c']:
        for p in r.packages(prefix):
            if p.parent.name=='paper_reproduction':
                path=p/'task_info.json';obj=r.load(path);obj['difficulty_reasons']=['The molecular object and primary comparison protocol are fixed; the Agent must construct geometries, validate calculations, retain the stated measurement/state identity, and document numerical and coverage limitations.'];r.save(path,obj)
    for p in r.packages('a3968'):
        path=p/'agent_input/task.md';s=r.read(path).replace('A calculation is complete when both models have converged structures, validation evidence, and all extractable rows or a documented row-specific failure.','A complete calculation requires both models to have converged, validated structures and all 47 required rows per model; missing rows or failed models must be reported as bounded_failure, not as complete.')
        r.put(path,s)
        path=p/'task_info.json';obj=r.load(path)
        for x in obj['data']:x['description']='Correct source-labelled neutral C20H17ClN6OS thione graph, complete label mapping, 47 pure SCXRD comparison rows and selectors; no author calculated geometry columns.'
        r.save(path,obj)
    for prefix in ['d2d08','e31cc','d8e54','c23cf','80cc1']:
        for p in r.packages(prefix):
            for xyz in (p/'agent_input/data/inputs').glob('*.xyz'):
                lines=r.read(xyz).splitlines();lines[1]='Given source-optimized object for the stated property/initial-state task; not an independently generated or undiscovered geometry';r.put(xyz,'\n'.join(lines)+'\n')
            path=p/'task_info.json';obj=r.load(path)
            for x in obj['data']:
                if x['path'].endswith('.xyz') and 'given source-optimized' not in x['description']:x['description']+=' This is a given source-optimized object, not an independent geometry-discovery input.'
            r.save(path,obj)
            r.note(p,'按已批准边界保留 source-optimized 给定对象/初态；统一 XYZ 注释和 task_info，不称其为独立生成或待发现几何。待求性质/中间关键点仍由 agent 计算，未公开结果或排名。')
    reviewed={
        'a0f6':'定向复核 raw 核+电子电荷二阶矩、完整张量、原点、DÅ 及拟合面法向；不替换为 traceless。既有 66 实频和 -111.07681064 DÅ 证据限于孤立 M3，不升级器件结论。现有定义无需改变。',
        'a389':'定向复核公开 3a 为反应物、两指定 [3,3]/[5,5] TS/IRC 支路与局部热化学基准。历史 GoodVibes entropy-only Grimme qRRHO（无 Head-Gordon 焓修正）及两势垒保留；未加入未知通道/端点要求。',
        '46f':'定向复核 SI Table S3 的 3.8436 eV/322.58 nm/f=0.4243 自洽；evidence_map 已记录正文 4.33 eV 冲突，无需换金标。完整 CIF/四 triflate 保留；轨道按物理身份而非程序固定编号，未增加其他化合物的因果对照。',
        'd8e54':'定向复核给定 81 原子 La +1/singlet、水/298 K/1 M 及 Ganti−Gsyn；历史两端点各 237 实频、4.393821 kcal/mol 仍对应当前固定对象。未扩大全局构象范围。',
        'c23cf':'定向复核给定 C58H42Si2/102 原子及 CHCl3，300 实频、TD20/735.93 nm/f1.2539 支持模型吸收；不硬编码轨道 209→210，不要求新增 NTO 或实验长链/聚集模型。',
        '5d942':'定向复核 AZ9 正确 53 原子图、conventional IP/EA/η/μ/χ/ω 算术和有限构象/基组敏感性；保留 9 minima/611 候选证据，不将有限搜索宣称全局证明，不推断生物活性。'}
    for prefix,text in reviewed.items():
        for p in r.packages(prefix):r.note(p,text)


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('batch',choices=['helicene','phosphorus','iron','insertion','consistency']);args=ap.parse_args();globals()[args.batch]();r.emit()
