"""One-time evidence patch generator, retained as maintenance provenance.

Later targeted edits supersede this draft. Do not rerun it over maintained
packages; use test_20260926.py for read-only regression.
"""
from pathlib import Path
import json,re,difflib,sys
ROOT=Path('tasks/verified_tasks')
changes={}
def put(p,x):changes[p]=x if isinstance(x,str) else json.dumps(x,ensure_ascii=False,indent=2)+'\n'
def read(p):return json.loads(p.read_text())
DETAILS={
'd83':('SI S6、Tables S8/S10/S13/S16，PDF pp34–36；正文的氧化机理解释。','保留2g已知母体输入和2a自行构建；明确气相绝热电子断键能，+1 doublet母体/+1 singlet去氢片段/中性doublet H，排除主结果中的ZPE/热修正；修复HF方法误写、最低点字段绑定和普通停止/免责声明门槛。','母体/片段四份OptFreq、H单点和Hirshfeld单点共6步骤；S=0.400976，2g/2a电子BDE=198.527743115/172.594617223 kJ/mol。', 'PR历史结果可直接匹配新schema；AR旧结果缺investigation，只作为同一科学量的验证证据，不补造自主规划。格式测试里的AR investigation是明确标注的synthetic外壳，不是新验证。'),
'2877':('可读正文位于group_2/source_data/user_supplied_20260925，正文§2.3/p2、§3.8/Table1/p8；SI Tables S1–S3/pp11–13。','保留给定三配合物性质比较；绑定Cd/Co/Ni唯一对象及正确自旋，规范gap/eta/omega定义；删除legacy metadata追问及c_limits，将有效状态/收敛证据接回c_trend。','三对象189个正模；Co稳定性→优化频率→终态稳定性链存在。gap Cd/Co/Ni=1.980716805/1.515946328/1.238934416 eV；eta同序、omega反序。','仅以当前定性序关系评分，不新增逐数值靶；给定结构不是待发现答案。不将电子描述符等同结合自由能。'),
'8fef':('正文p4/Scheme3；SI p34方法、pp36–41 B/TS2/TS2′坐标。','按负责人要求把三份作者坐标移至evaluation/author_results；公开SMILES/连接图和ETKDGv3(seed20260926)+UFF独立生成的自由基初态，0/2，53原子。两TS须自行构建。AR候选编号不含作者通道，私有规则按真实连接/成键模式映射，不按能量挑身份；PR提供两通道指导但不提供胜者。主比较DMSO/298.15K/1atm。','原始B/两TS均重新OptFreq；153模分别0/1/1个虚频，TS模式−470.6863/−476.5989 cm⁻¹，成键模式对应C22–C45和C5–C22（历史原子顺序）。势垒13.253000092/19.257010740，差6.004010648 kcal/mol，目标13.08/19.25/6.17各±1.5未改。','历史作者知情验证支持相同驻点和能垒可计算，不是新公开初态的盲测成功。未新增强制IRC；现有负模位移证据有效。author_results仅作私有结构参考，未新增RMSD评分。公开初态只做化学身份/连通性/数值几何检查，未运行QM。'),
'9ec':('SI p3 PBE0-D3BJ/6-311+G**方法、Tables S1/S2 pp13–15、Table S7 p21。','明确主量为含D3BJ的源协议、气相300K/1atm harmonic Gibbs；其他方法仅作另报控制。区分身份与驻点两个过程项，绑定两个不同构象。AR仅去掉两份重复文件名，coplanar.xyz和perpendicular.xyz完整保留。','两构象各234正模，G为−3191.525824/−3191.525806 Eh，差−0.047258993 kJ/mol；对应SI含色散−0.1。','SI不含色散为+4.8，不能把任意方法结果强行按近等能评分；现已明示源主协议，不新增−0.1硬容差。构象名称定义给定比较对象，不要求独立发现其几何。'),
'1a47':('正文pp1,4；SI p59方法、p60 Fig.S3、p61 TableS5。','更正ortho/para相对于游离酚OH，而不是醚氧；两攻击碳相对醚连接位都是邻位。保留解释已知实验选择性的任务角色。明确同一G零点不要求两条反向IRC到完全相同前驱构象；完成分支覆盖两通道，早期失败允许没有未算出的频率/IRC。删除c_limitation。','15份原生日志及有效IRC前缀→真实自由优化端点；TS虚频−267.4872/−285.8447，势垒19.355178322/26.883378107，para−ortho=7.528199785 kcal/mol，符合7.6±1.5。','不把IRC步数上限前缀当已收敛端点；后继真实OptFreq补全。只处理存在的PR，不补造AR；公开实验方向用于解释，不是未知选择性盲测。'),
'913':('SI p10方法、p12终端H2释放路线和坐标。','保留完整INT-G已知反应物，要求自建TS；明确DMAc、298.15K/1atm以及INT-G共同零点；绑定success与真实势垒/驻点/连接，取消泛泛停止/局限要求。','14个有效步骤：INT-G/TS优化频率与MN15单点、双向IRC、端点和后续H2释放/分离片段。TS−478.5853，G势垒0.764432041 kcal/mol，符合0.9±2.0。','结合H2中间体不等于分离H2，原档案已保存额外释放证据；不需要重算。方法路径是作者知情验证，不是AR搜索轨迹。'),
'0e83':('正文pp3–5方法/Table2与SI相应H2活化通道。','保留两个完整已知silylene+H2反应物，无作者TS；明确苯/298K/1atm、分离反应物零点；绑定1/V-prime唯一对象，完成须两套真实TS/路径/势垒。私有结论明确1势垒低于V′，不公开排序，不增加数值硬靶；删c_limit/两轮停止规则。','17个有效步骤覆盖两个最低点、H2、两TS、IRC/四端点、稳定性；势垒33.065984223/47.132236592 kcal/mol，方向符合正文32.9/47.4。','未完成分支仅提交实际已算部分，不得作为完整排序成果；合法额外尝试不影响主结果。'),
'2a71':('SI p60方法、pp68–69的受限F–C–C–I扫描和约31 kcal/mol。','保留PR受限剖面目标，成功至少五个不同有效状态、起点与近零端、真实势垒和实质敏感性。取消c_limitation；kp_limits保留为实际数值敏感性检查，不只是声明。原31±1靶和容差未改。','15电子扫描状态/6 Gibbs点，主势垒30.003737993；独立近零29.946634631，低频50/100处理29.731694702/29.327035556；自由起点90正模，受限切向89维曲率检查支持受限驻点。','待负责人决定评分口径/参考容差，暂不建议发布。主结果离30下界仅0.003737993，极小实现差异就翻转判分；既有实算并非缺失，不以扩大容差或替换gold自动解决，不重算、不迁移。'),
'728':('SI pp10–11两态分别优化/频率及分层基组、正文p4，SI复合物4坐标pp99–100。','保留给定复合物的两态性质比较；明确分别弛豫后的电子Et−Es而非垂直或G能差；完成必须有两电子能/gap/lower_state，评分绑定实际数值与证据，不按免责声明给分。','ORCA3份有效日志覆盖singlet Opt+Freq及triplet OptFreq。两态无负模，Et−Es=+32.219903 kcal/mol，支持闭壳层singlet较低。','不将B3LYP32.22声称为BP8625.1逐值复现；现行只评分方向，不新增数值容差或额外电子态搜索。')}

def strings(n,optional=False):
    if isinstance(n,dict):
        if n.get('type')=='string' and not optional:n.setdefault('minLength',1)
        for k,v in n.items():
            if k=='properties':
                for name,prop in v.items():strings(prop, optional or name in ['limitations','stopping_rule','stopping_criterion','stopping_basis','unresolved_alternatives'])
            else:strings(v,optional)
    elif isinstance(n,list):
        for v in n:strings(v,optional)

for p in sorted(ROOT.glob('*/*')):
 if not (p/'task_info.json').is_file():continue
 key=next(k for k in DETAILS if p.name.startswith('paper_'+k));source,repair,ev,boundary=DETAILS[key]
 schema=read(p/'agent_input/submission_schema.json');s=schema['result_schema'];strings(s)
 if key=='8fef':
    for name,st in s['properties']['states']['properties'].items():
        st['properties']['atom_mapping']={'type':'array','minItems':53,'maxItems':53,'uniqueItems':True,'items':{'type':'integer','minimum':1,'maximum':53},'description':'For each output-geometry row, give the corresponding 1-based input radical_starter.xyz atom index.'}
        s['allOf'][0]['then']['properties']['states']['properties'][name]['required'].append('atom_mapping')
    text=(p/'agent_input/task.md').read_text().replace('input-to-output atom mapping','`atom_mapping` (one public-input atom index per output-geometry row)')
    put(p/'agent_input/task.md',text)
 elif key=='2a71':s['properties']['scan_states']['uniqueItems']=True
 elif key=='1a47':
    for branch in s['oneOf'][0]['properties']['candidates']['allOf']:
        branch['contains']['allOf'][0]['properties']['imaginary_frequency_cm-1']={'type':'number','exclusiveMaximum':0}
 if key=='d83':
    good=s['oneOf'][0]['properties']
    if 'investigation' in good:good['investigation']['properties']={'plan':{'type':'string','minLength':1},'models_or_conformers':{'type':['array','string'],'minItems':1,'minLength':1},'coverage':{'type':'string','minLength':1}}
 put(p/'agent_input/submission_schema.json',schema)
 # Update current rule mapping, preserving all historical raw step/value sections.
 ref=p/'evaluation/verified_computation_reference.md';text=ref.read_text()
 text=text.replace('## 4. 当前模式 evaluator 的逐项对应','## 4. 入库时 evaluator 对应快照（历史；修订后的关联见第7节）')
 text=text.replace('## 5. 归档判断、已知差异及后续整理','## 5. 入库时判断及已知差异（历史记录；处理结果见第7节）')
 if key=='8fef':
    text=text.replace('AR 公共文件使用','入库时 AR 公共文件曾使用').replace('当前任务将进一步 IRC/位移列为可行时的增强验证','历史题面把进一步 IRC/位移列为可行时的增强验证；修订版要求相关负模检查，IRC仍非强制')
    text=text.replace('当前任务是给定三个对象的驻点/热化学比较','入库时任务是给定三个对象的驻点/热化学比较（2026-09-26 已按负责人要求移除公开作者TS）')
 rows=[]
 kps=read(p/'evaluation/reference_key_points.json')['items'];con=read(p/'evaluation/reference_conclusions.json')['items'];rules=read(p/'evaluation/scoring_rules.json')['rules']
 for item in kps+con:
    ident=item.get('key_point_id',item.get('conclusion_id'))
    desc=str(item.get('expected',item.get('statement',''))).replace('|','/')
    # Current requirements and existing evidence are not a new computation.
    rows.append(f'| `{ident}` | {desc} | {ev} |')
 appendix='\n## 7. 2026-09-26 修订后的科学对应与验证适用范围\n\n'+source+'\n\n实际修复：'+repair+'\n\n验证适用性：'+boundary+'\n\n原第4、5节保留入库时的旧关联/待修记录，不代表当前评分；已取消的普通 limitation 结论不再评分。以上原始有效步骤、总能、频率及其来源未改，以下表格按当前五个 evaluator JSON 核对。reference 仍只作计算档案，不作为评分输入。\n\n| 当前关键点/结论 | 当前科学要求 | 已有真实计算支持 |\n|---|---|---|\n'+'\n'.join(rows)+'\n\n当前规则绑定（不改变原数值靶和容差）：\n\n'
 appendix+='\n'.join('- `'+r['rule_id']+'` → `'+r['reference_id']+'`；读取 `'+', '.join(r.get('binding',{}).get('fields',[]))+'`。' for r in rules)+'\n'
 if key=='8fef':appendix+='\n格式适配只将旧结果 optimized_geometry 映射为 geometry_file、mode_check.forming_C_C_pair_1based 映射为 forming_bond_1based，并通过元素标记反应物连接图建立旧/新原子编号对应；不改变计算值、不把验证者所知的TS作为公开输入。AR候选编号可交换，评分按化学通道映射。\n'
 if '## 7. 2026-09-26' not in text:text+=appendix
 put(ref,text)
 audit='# 2026-09-26 逐包维护记录\n\n论文：`'+p.name+'`；模式：`'+p.parent.name+'`。修前基线940d3d04；格式步骤5d18a199。用户已批准按流程修复，并明确作者优化TS不得公开；未批准迁移。\n\n## 原文依据\n\n'+source+'\n\n## 问题与实际修复\n\n'+repair+'\n\n## 成功计算支持\n\n'+ev+'\n\n完整步骤和原始来源见[verified_computation_reference](../verified_computation_reference.md)，尤其当前第7节。不重写历史计算，不把格式样例作为科学证据。\n\n## 输入角色与边界\n\n'+boundary+'\n\n## 关键点/结论及评分\n\n保留'+str(len(kps))+'个科学关键点、'+str(len(con))+'个科学结论；采用dual_axis_100.scientific_results.v1。普通limitation没有独立得分或必填门槛，实际身份/频率/连接/敏感性职责仍保留。所有结果型关键点已关联主结论，不以增加空洞结论凑数。\n\n## 验收与状态\n\n运行本批维护回归脚本检查真实结果（必要无损字段映射）、明确标注的synthetic格式样例、失败与不完整反例、包/manifest、实际评分适配和仅导出agent_input。科学语义由逐项原文/真实输出核对，不宣称调用过LLM judge或独立agent盲测。实际主机网络/挂载隔离尚未实测。详见[本批汇总](../../../../MAINTENANCE_REPORT.md)第25节。仍留verified_tasks；'+('科学评分边界待负责人决定，不建议发布。' if key=='2a71' else '修订完成后可作为负责人验收候选，不自动获得发布/迁移批准。')+'\n'
 put(p/'evaluation/task_provenance/maintenance_audit.md',audit)
 if key=='2877':
    evidence=read(p/'evaluation/evidence_map.json');evidence['source_access_note']='Use the recovered readable main PDF at docs/verification/group_2/paper_2877efc02814175d/source_data/user_supplied_20260925/1-s2.0-S0022286025023567-main.pdf; repository main.pdf is damaged. Methods p2; Table1/Section3.8 p8; SI Tables S1-S3 pp11-13.';put(p/'evaluation/evidence_map.json',evidence)

patch='*** Begin Patch\n'
for path,new in changes.items():
 if len(sys.argv)>1 and not all(t in str(path) for t in sys.argv[1:]):continue
 old=path.read_text() if path.exists() else None
 if old==new:continue
 if old is None:patch+='*** Add File: '+str(path)+'\n'+'\n'.join('+'+line for line in new.splitlines())+'\n'
 else:
    lines=list(difflib.unified_diff(old.splitlines(),new.splitlines(),n=3,lineterm=''))[2:]
    patch+='*** Update File: '+str(path)+'\n'+'\n'.join('@@' if l.startswith('@@') else l for l in lines)+'\n'
print(json.dumps(patch+'*** End Patch'))
