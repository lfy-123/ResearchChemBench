#!/usr/bin/env python3
"""Recover identity-only topology, discard all source conformers, embed anew.

XYZ coordinates are consulted only to recover/check a chemical graph and its
source atom numbering. No source distances, endpoints, energies or target
torsions enter the new embedding. Prints patch via the maintenance helper.
"""
import argparse
import json
from pathlib import Path
import networkx as nx
import numpy as np
from rdkit import Chem, rdBase
from rdkit.Chem import AllChem, rdDetermineBonds, rdMolDescriptors, rdMolTransforms
import staged_task_repair_20260916 as repair


def nxgraph(m):
    g=nx.Graph()
    for a in m.GetAtoms(): g.add_node(a.GetIdx(),symbol=a.GetSymbol())
    g.add_edges_from((b.GetBeginAtomIdx(),b.GetEndAtomIdx()) for b in m.GetBonds())
    return g


def organic(source,smiles=None):
    old=Chem.MolFromXYZBlock(source);rdDetermineBonds.DetermineConnectivity(old)
    if smiles:
        t=Chem.AddHs(Chem.MolFromSmiles(smiles))
        matcher=nx.isomorphism.GraphMatcher(nxgraph(old),nxgraph(t),node_match=lambda a,b:a['symbol']==b['symbol'])
        assert matcher.is_isomorphic(), 'Source graph differs from independently specified full identity'
        mapping=matcher.mapping
        mol=Chem.RenumberAtoms(t,[mapping[i] for i in range(old.GetNumAtoms())])
    else:
        rdDetermineBonds.DetermineBondOrders(old,charge=0,embedChiral=False)
        mol=Chem.Mol(old)
    # Preserve only discrete atom-centre stereochemistry where present.
    if smiles:
        mol.AddConformer(Chem.Conformer(old.GetConformer()),assignId=True)
        Chem.AssignAtomChiralTagsFromStructure(mol,replaceExistingTags=True)
    mol.RemoveAllConformers()
    return mol


def metal(source):
    raw=Chem.MolFromXYZBlock(source);rdDetermineBonds.DetermineConnectivity(raw)
    rw=Chem.RWMol(raw)
    for i in range(4,-1,-1): rw.RemoveAtom(i)
    lig=rw.GetMol();rdDetermineBonds.DetermineBondOrders(lig,charge=0,embedChiral=False)
    expected=Chem.MolFromSmiles('CN(CCN(C)CCN(Cc1ccccn1)Cc1ccccn1)CCN(Cc1ccccn1)Cc1ccccn1')
    assert Chem.MolToSmiles(Chem.RemoveHs(lig))==Chem.MolToSmiles(expected)
    lig.RemoveAllConformers()
    rw=Chem.RWMol()
    for sym,q in [('Fe',3),('Fe',3),('O',-1),('O',-1),('O',-2)]:
        a=Chem.Atom(sym);a.SetFormalCharge(q);a.SetNoImplicit(True);rw.AddAtom(a)
    for a in lig.GetAtoms():rw.AddAtom(Chem.Atom(a))
    for b in lig.GetBonds():rw.AddBond(b.GetBeginAtomIdx()+5,b.GetEndAtomIdx()+5,b.GetBondType())
    rw.AddBond(2,3,Chem.BondType.SINGLE)
    for donor,fe in [(2,0),(3,1),(4,0),(4,1)]+[(i,0) for i in range(5,9)]+[(i,1) for i in range(9,13)]:
        rw.AddBond(donor,fe,Chem.BondType.DATIVE)
    mol=rw.GetMol();Chem.SanitizeMol(mol);assert mol.GetNumConformers()==0
    return mol


def embed(mol,seed0,metal_case=False,helicene=False):
    pt=Chem.GetPeriodicTable()
    for seed in range(seed0,seed0+80):
        m=Chem.Mol(mol);params=AllChem.ETKDGv3();params.randomSeed=seed;params.numThreads=1;params.useRandomCoords=True;params.maxIterations=1500
        if metal_case:
            # Generic coordination-chemistry ranges, not the source Fe-Fe result.
            bm=AllChem.GetMoleculeBoundsMatrix(m)
            for b in m.GetBonds():
                i,j=sorted([b.GetBeginAtomIdx(),b.GetEndAtomIdx()])
                if b.GetBondType()==Chem.BondType.DATIVE:bm[i,j]=2.65;bm[j,i]=1.8
            bm[0,1]=4.5;bm[1,0]=2.7
            # Distinct oxo/peroxo atoms are NOT covalently bonded. Generic
            # excluded-volume lower bounds avoid an artificial O3/O4/O5 clump.
            for i,j in ((2,4),(3,4)):
                bm[i,j]=4.5;bm[j,i]=2.2
            params.SetBoundsMat(bm);params.ignoreSmoothingFailures=True
        if AllChem.EmbedMolecule(m,params)!=0:continue
        xyz=m.GetConformer().GetPositions()
        ratios=[];non=[]
        valid=True
        for i in range(m.GetNumAtoms()):
            for j in range(i):
                dist=float(np.linalg.norm(xyz[i]-xyz[j]));b=m.GetBondBetweenAtoms(i,j)
                if metal_case and (i<2 or j<2):
                    if b and not 1.65<dist<2.9:valid=False
                    if not b and dist<1.5:valid=False
                    continue
                ratio=dist/(pt.GetRcovalent(m.GetAtomWithIdx(i).GetAtomicNum())+pt.GetRcovalent(m.GetAtomWithIdx(j).GetAtomicNum()))
                if b:
                    ratios.append(ratio)
                    if not .7<ratio<1.4:valid=False
                else:
                    non.append(ratio)
                    if ratio<1.05:valid=False
        if not valid:continue
        if helicene:
            chain=[1,66,65,64,63,62,61,59]
            angles=[rdMolTransforms.GetDihedralDeg(m.GetConformer(),*[j-1 for j in chain[i:i+4]]) for i in range(5)]
            # Retain source-labelled winding only, never its optimized magnitude.
            if sum(angles)<0:
                for i,v in enumerate(xyz): m.GetConformer().SetAtomPosition(i,(-v[0],v[1],v[2]))
        return m,{'seed':seed,'bond_radius_ratio_range':[min(ratios),max(ratios)],'minimum_nonbonded_radius_ratio':min(non),'quantum_calculation':False,'force_field_minimization':False,'source_coordinate_constraints':False}
    raise RuntimeError('No valid independent starter; do not substitute or perturb author geometry')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('paper',choices=['746','ef266','44f']);args=ap.parse_args()
    packs=repair.packages(args.paper);p=packs[0]
    specs={'746':[('compound5.xyz',None,72)],'ef266':[('Et2N3P.xyz','CCN(CC)P(N(CC)CC)N(CC)CC',46),('Et2N3P_PO.xyz','CCN(CC)[P+](CC(C)[O-])(N(CC)CC)N(CC)CC',56),('Et2N3P_PA.xyz','CCN(CC)[P+](C(=O)c1ccccc1C(=O)[O-])(N(CC)CC)N(CC)CC',61)],'44f':[('1H_start.xyz',None,87)]}[args.paper]
    for idx,(name,smiles,n) in enumerate(specs):
        source_path=p/'evaluation/author_results'/name
        if not source_path.exists():source_path=p/'agent_input/data/inputs'/name
        source=source_path.read_text()
        mol=metal(source) if args.paper=='44f' else organic(source,smiles)
        assert mol.GetNumAtoms()==n and mol.GetNumConformers()==0
        for i,a in enumerate(mol.GetAtoms()):a.SetAtomMapNum(i+1)
        graph=Chem.MolToSmiles(mol)
        new,check=embed(mol,916001+idx*100,args.paper=='44f',args.paper=='746')
        lines=[str(n),'Independent topology-only ETKDG starter; unoptimized; atom order preserved; no author endpoint coordinates']
        lines += [f'{a.GetSymbol()} {v[0]:.8f} {v[1]:.8f} {v[2]:.8f}' for a,v in zip(new.GetAtoms(),new.GetConformer().GetPositions())]
        for pkg in packs:
            old=pkg/'agent_input/data/inputs'/name
            archive=pkg/'evaluation/author_results'/name
            if not archive.exists():repair.put(archive,old.read_text())
            repair.put(old,'\n'.join(lines)+'\n')
            definition={'atom_count':n,'formula':rdMolDescriptors.CalcMolFormula(mol),'mapped_smiles':graph,'mapping':'Atom-map number equals one-based XYZ row; preserve chemical graph and discrete stereochemistry. Metal arrows denote coordination, not new reaction products.','starter_status':'independently embedded, unoptimized; not a computed minimum'}
            if args.paper=='746':definition['inner_rim_chain_1based']=[1,66,65,64,63,62,61,59];definition['torsion_definition']='five consecutive quadruples; primary mean(abs(phi)); retain signed phi and atom IDs'
            if args.paper=='44f':definition['coordination']={'Fe1_N_donors':[6,7,8,9],'Fe2_N_donors':[10,11,12,13],'peroxo':[3,4],'mu_oxo':5,'Fe_Fe_covalent_bond_in_graph':False}
            repair.save(pkg/'agent_input/data/inputs'/name.replace('.xyz','_identity.json'),definition)
            repair.save(pkg/'evaluation/task_provenance'/name.replace('.xyz','_independent_preparation.json'),{'rdkit_version':rdBase.rdkitVersion,'identity_source':'Source-defined graph checked against full named chemistry; source atom ordering retained. Coordinates used only for graph reconstruction/discrete identity, all conformers removed before embedding.','generator':'ETKDGv3; first valid geometry, no energy/answer-based selection','check':check,'metal_generic_bounds':'Fe-donor 1.8–2.65 A; Fe-Fe 2.7–4.5 A; nonbonded oxo/peroxo 2.2–4.5 A, if applicable; not taken from author endpoint','historical_verification':'author-route calculations remain historical; no claim of optimization from this new starter'})
            repair.note(pkg,f'{name} 已替换为完整拓扑独立嵌入、未优化起点；原坐标留 evaluation/author_results/{name}。公开身份文件保存原子映射/配位，生成未使用作者终态坐标约束或目标参数，未新增量化验证。')
    repair.emit()


if __name__=='__main__':main()
