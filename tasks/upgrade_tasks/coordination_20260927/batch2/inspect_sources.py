from pathlib import Path
import json,re,hashlib,fitz
ROOT=Path(__file__).resolve().parents[4]
B=Path(__file__).resolve().parent
A=json.loads((B/'assignment.json').read_text())
M=json.loads((ROOT/'docs/evalution/update/upgrade_guidance_review_manifest_20260927.json').read_text())
(B/'source_reviews/guidance_manifest.json').write_text(json.dumps(M,ensure_ascii=False,indent=2))
for pid in A['batch']['papers']:
 d=(ROOT/'docs/evalution/update'/f'{pid}.md').read_text()
 dest=B/'source_reviews'/pid; dest.mkdir(exist_ok=True)
 (dest/'guidance.md').write_text(d)
 sources=[]
 for f in (ROOT/'papers'/pid/'documents').glob('*.pdf'):
  doc=fitz.open(f)
  (dest/(f.stem+'.txt')).write_text('\n'.join(f'\n===== PDF PAGE {i+1} =====\n'+p.get_text() for i,p in enumerate(doc)))
  sources.append({'path':str(f.relative_to(ROOT)),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'pages':len(doc)})
 (dest/'sources.json').write_text(json.dumps(sources,indent=2))
 print(pid,[(s['path'].split('/')[-1],s['pages']) for s in sources])
