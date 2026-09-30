"""Extract ONLY the black experimental trace from Fig2/compound1.
Raster digitization, not a calculated spectrum; no fitted author ECD is exported.
"""
from pathlib import Path
import csv,json
import numpy as np
from PIL import Image
B=Path(__file__).resolve().parent;D=B/'source_reviews/paper_9d091f4337662e78'
p=D/'main_p4.png';a=np.asarray(Image.open(p).convert('RGB'))
# Calibration from displayed top-left panel ticks in this exact source render.
x0,x1=133.5,459.0;y0,ys=234.0,20.25
anchors=np.array([[205,-2.7],[210,-3.8],[215,-4],[220,-3.8],[225,-3.2],[230,-2.2],[235,-1.1],[240,-.2],[245,.35],[250,.45],[270,.45],[300,.5],[340,.45],[370,.55],[398,.7]])
rows=[]
for nm in np.arange(205,397,2):
 x=int(round(x0+(nm-200)*(x1-x0)/200));estimate=y0-np.interp(nm,anchors[:,0],anchors[:,1])*ys
 candidates=[]
 for xx in range(x-1,x+2):
  for yy in range(max(180,int(estimate-10)),min(348,int(estimate+11))):
   pix=a[yy,xx].astype(float)
   if max(pix)-min(pix)<22 and np.mean(pix)<130 and abs(yy-y0)>1:
    candidates.append((abs(yy-estimate),yy,xx))
 if not candidates:continue
 # darkest near trace window; median handles line antialiasing.
 ys_found=[v[1] for v in candidates];yy=float(np.median(ys_found))
 rows.append({'wavelength_nm':float(nm),'delta_epsilon_M_inverse_cm_inverse':round((y0-yy)/ys,4),'wavelength_digitization_bound_nm':1.0,'delta_epsilon_digitization_bound':0.15,'partition':'heldout' if nm<=239 else 'diagnostic_tail','pixel_x':x,'pixel_y':yy})
with (D/'experimental_ecd_digitized.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
(D/'digitization_provenance.json').write_text(json.dumps({'source':'papers/paper_9d091f4337662e78/documents/main.pdf','page_1_based':4,'figure':'Figure 2 top-left, black Exp. ECD of 1 only','render_file':'main_p4.png','axes':{'x_200nm':x0,'x_400nm':x1,'y_zero':y0,'pixels_per_delta_epsilon':ys},'method':'Neutral dark pixels in black experimental curve window. Excludes red/blue traces, legends, axis intersections. Values are approximate digitization, not raw instrument measurements.','error_bound_basis':'About 1.6 px/nm and20.25px per Δepsilon; bounds allow line thickness/antialiasing and axis reading. They are not theory acceptance tolerances.','excluded':'Author assignment, calculated traces and source optimized conformers never enter the public dataset.','rows':len(rows)},indent=2))
print(len(rows),rows[:8])
