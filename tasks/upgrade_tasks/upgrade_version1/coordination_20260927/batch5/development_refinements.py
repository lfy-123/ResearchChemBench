"""Audited marker digitization and public metadata updates; no scientific engines."""
from pathlib import Path
import csv,json,hashlib
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
def dump(p,d):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def input_copy(pid,name):
 return json.loads((ROOT/'tasks/upgrade_tasks/autonomous_research'/pid/'agent_input/data/inputs'/name).read_text())
def save(pid,name,d):dump(B/'prepared_inputs'/pid/name,d)

# Only visible discrete markers from Figure 10. Fitted curves/taus are not sampled.
pid='paper_2c439196c2f349c9'
image=B/'source_review/INP_page10_native_image1.png'
pixels={0.25:[(209,693),(299,693),(407,656),(490,656),(533,621),(643,621),(692,621),(794,621),(893,656)],
 0.5:[(209,656),(299,478),(407,442),(490,371),(533,299),(643,264),(692,264),(794,264),(893,335)],
 1.0:[(209,619),(299,443),(407,369),(490,227),(533,191),(643,85),(692,85),(794,85),(893,121)]}
cal={'x_pixels':[107,897],'time_ms':[0,200],'y_pixels':[728,14],'ring_count':[0,20]}
rows=[]
for conc,points in pixels.items():
 for n,(x,y) in enumerate(points,1):
  rows.append({'observation_id':f'fig10_c{conc:g}_{n:02d}','concentration_mM':conc,'input_power_mW':50,
   'time_ms':round((x-107)*200/790,5),'ring_count':round((728-y)*20/714,5),
   'pixel_x':x,'pixel_y':y,'time_digitization_halfwidth_ms':round(4*200/790,5),
   'ring_count_digitization_halfwidth':round(4*20/714,5),'measurement_uncertainty':None})
out=B/'prepared_inputs'/pid;out.mkdir(parents=True,exist_ok=True)
with (out/'fig10_measured_markers.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
meta={'source':'Target article main PDF p10, Figure 10, discrete square/circle/triangle measurement markers',
 'source_pdf_sha256':hashlib.sha256((ROOT/'papers'/pid/'documents/main.pdf').read_bytes()).hexdigest(),
 'source_native_plot_sha256':hashlib.sha256(image.read_bytes()).hexdigest(),'native_plot_size_pixels':[1000,845],
 'axis_calibration':cal,'observation_count':len(rows),'table':'fig10_measured_markers.csv',
 'digitization_method':'Manual visual center picks from the native embedded plot. Axis interpolation is linear; no fitted line, interpolated pseudo-measurement or fitted time constant is included. The overlapping origin marker is omitted.',
 'digitization_uncertainty':'A conservative +/-4 pixel reading envelope per coordinate; this is a digitization bound, not an experimentally calibrated noise standard deviation. Display fractional ring count values without silently snapping to integers.',
 'measurement_uncertainty_status':'Not supplied by the source plot; requires declared measurement/counting and timing uncertainty before weighted model discrimination.',
 'input_gate':'Partial authentic observations only. Power/Z-scan independent rows, calibrated SSPM waist, instrument response and defensible thermal bounds are still missing. This table does not resolve the blocked gate.',
 'scientific_fitting_performed':False}
save(pid,'fig10_digitization_provenance.json',meta)
dump(B/'source_review/INP_fig10_digitization_audit.json',{'metadata':meta,'rows':rows,'private_plot_file':str(image.relative_to(ROOT))})
d=input_copy(pid,'inp_molecule.json');d['molecular_boundary']='Identity of the solute INP only. The scored investigation concerns solution optical response under study_scope.json; isolated-molecule DFT is optional background and excludes neither solvent nor thermal effects from the primary physical model.';save(pid,'inp_molecule.json',d)
pid='paper_eda19e7c8edd4b39';d=input_copy(pid,'system_definition.json');d['scored_observables']=['Ni/Al vacancy energies at two supercell sizes with common reservoirs','Termination-resolved atom-exchange and balanced bulk-vacancy/slab-adatom cycles','L12 Ni3Al grand potential and slab/vacuum/k-point convergence'];save(pid,'system_definition.json',d)
pid='paper_0cd74ae20ab933f3';d=input_copy(pid,'model_systems.json');d['observables'].pop('main_result_order',None);d['observables'].pop('additional_attempts',None);d['observables']['expanded_matrix']='All three members require relaxed and common-core spin comparisons. Use calculation_records/results in the submission contract for attempts, calibration and effects.';save(pid,'model_systems.json',d)
pid='paper_80441aced6051d86';d=input_copy(pid,'g1_monomer_identity.json');d['measurement_mapping']='Atom-map IDs refer to the monomer XYZ rows; carry them through geometry generation. These intraguest ring sets support optional conformation diagnostics. The primary upgraded comparisons are density-matched host/partner deletion and free-guest controls; a single guest has no interguest distance/slip/twist.';save(pid,'g1_monomer_identity.json',d)
print('Saved 27 source marker observations with explicit digitization bounds; input gate remains blocked. Updated four legacy metadata files.')
