"""Compare independent PDF codes and every workbook statement cell with records."""
import sys,json,re,unicodedata,collections,logging
from pathlib import Path
from common import ROOT,KINDS
from pypdf import PdfReader
logging.getLogger('pypdf').setLevel(logging.ERROR)
from cte_workbook import workbook,rows
if hasattr(sys.stdout,'reconfigure'):sys.stdout.reconfigure(encoding='utf-8')
records=json.loads((ROOT/'catalog.json').read_text(encoding='utf-8'))['records'];byid={n['id']:n for n in records}
report={};failed=[]
def normalize(s):return re.sub(r'\s+',' ',unicodedata.normalize('NFKC',s).replace('\u00ad','')).strip()
def check(label,a,b):
    a=collections.Counter(a);b=collections.Counter(b)
    report[label]={'source_occurrences':sum(a.values()),'repository_occurrences':sum(b.values()),'missing':list((a-b).elements())[:15],'extra':list((b-a).elements())[:15],'passed':a==b}
    if a!=b:failed.append(label)
def pages(name):return [p.extract_text() for p in PdfReader(ROOT/'sources/official'/(name+'.pdf')).pages]
def subset(name):return [n for n in records if n['subject']==name and n['node_type'] in KINDS]
text=' '.join(pages('science'))
codes={re.sub(r'\s+','',m[0]) for m in re.finditer(r'(?:K-2|3-5|K|[1-5]|MS|HS)-(?:PS|LS|ESS|ETS)\d-\d+(?:\s*MI)?',text)}
check('science performance expectation codes',codes,{n['code'] for n in subset('science')})
text=' '.join(pages('arts'))
codes=[re.sub(r'\s+','',c) for c in re.findall(r'ART\s*\.\s*(?:D|M|T|VA)\s*\.\s*[IVX]+\s*\.\s*(?:K|[1-8]|HS)\s*\.\s*\d+',text)]
check('arts printed-code occurrences',codes,[re.sub(r'\s+','',n['source_code']) for n in subset('arts')])
codes={c for t in pages('physical-education')[13:45] for c in re.findall(r'S[1-5]\.\d+\.(?:K|[1-8]|L[12])[a-z]?',t)}
check('PE unique printed codes',codes,{n['code'] for n in subset('physical-education')})
codes={c for t in pages('computer-science') for c in re.findall(r'(?:1A|1B|2|3A|3B)-(?:CS|NI|DA|AP|IC)-\d+',t)}
check('computer science content codes',codes,{n['code'] for n in subset('computer-science') if not n['code'].startswith('P') and n['node_type']=='standard'})
text='\n'.join(pages('world-languages'))
codes=[re.sub(r'\s+','',m[1]) for m in re.finditer(r'^\s*([1-5]\s*\.\s*\d\s*\.\s*[NMA](?:\s*\.\s*[A-Za-z]+){1,2})\s*\.?\s*$',text,re.M)]
check('world language unique benchmark codes',set(codes),{n['code'] for n in subset('world-languages') if n['node_type']=='substandard'})
text=re.sub(r'\s+','',' '.join(pages('english-language-development')[293:330]))
codes=set(re.findall(r'ELD-(?:SI|LA|MA|SC|SS)\.?(?:K-3|4-12|K|1|2-3|4-5|6-8|9-12)\.?(?:Narrate|Inform|Explain|Argue)(?:\.?(?:Interpretive|Expressive))?',text))
check('WIDA appendix expectation codes',codes,{n['code'] for n in subset('english-language-development') if n['node_type']=='substandard'})
codes=[];topic=None
for i,t in enumerate(pages('health'),1):
    if i not in list(range(26,55))+list(range(60,68)):continue
    for l in t.splitlines():
        tm=re.search(r'[\[(](\d+\.[1-6][.\s]+[A-Z]+)[\])]',l)
        if tm:topic=re.sub(r'[.\s]+','.',tm[1])
        m=re.match(r'^\s*(\d+)\.\s',l)
        if m and topic:codes.append(topic+'.'+m[1])
check('health indicator codes',codes,[n['code'] for n in subset('health')])
# Workbooks: independently enumerate normative statement cells and check both
# ownership and the complete cell wording against canonical records.
coverage=json.loads((ROOT/'sources/cte-coverage.json').read_text(encoding='utf-8'))
programs={p['cip']:p for p in coverage['programs']};owners=coverage['cell_owners'];expected=set();issues=[]
for doc in json.loads((ROOT/'sources/cte-program-sources.json').read_text(encoding='utf-8')):
    cip=Path(doc['file']).stem;sid=programs[cip]['source_id']
    for sheet,cells in workbook(ROOT/doc['file']).items():
        rr=rows(cells);header=rr[min(rr)];cols=[]
        if sheet.strip()=='PCC':cols=['C']
        elif 'career ready' in sheet.lower():cols=['B']
        elif 'standard' in sheet.lower() or 'gap analysis' in sheet.lower():
            if header.get('A',{}).get('text','').strip().lower()=='knowledge':cols=['E']
            elif 'AED Standards Index' in sheet:cols=['C']
            else:cols=[c for c,v in header.items() if re.match(r'^Standards\b|^Performance Indicators\b',v['text'],re.I)]
        for row,values in rr.items():
            if row<=min(rr):continue
            for c in cols:
                if c not in values:continue
                v=values[c];body=v['text'].strip()
                if sheet.strip()=='PCC' and not re.fullmatch(r'[A-Z]+\d+',values.get('A',{}).get('text','').strip()):continue
                if 'career ready' in sheet.lower() and not re.fullmatch(r'CRP\d{2}',values.get('A',{}).get('text','')):continue
                if body=='Segments' or not body:continue
                if re.fullmatch(r'N\s*/?\s*A|Column\d+',body,re.I):continue
                if 'AED Standards Index' in sheet:
                    m=re.match(r'^\d+[a-z]\.\d+\s+(.+)',body,re.S)
                    if not m:continue
                    body=m[1]
                key=sid+'|'+sheet+'|'+v['origin'];expected.add(key)
                ids=owners.get(key,[])
                texts=[normalize(byid[i]['text']) for i in ids if i in byid]
                if not ids or normalize(body) not in texts:issues.append({'cell':key,'owners':ids,'reason':'unmapped or wording differs'})
report['CTE statement cells']={'program_workbooks':len(programs),'expected_statement_cells':len(expected),'owned_statement_cells':len(owners),'issues':issues[:20],'unexplained_owned_cells':list(set(owners)-expected)[:10],'passed':not issues and set(owners)==expected}
if not report['CTE statement cells']['passed']:failed.append('CTE statement cells')
print(json.dumps(report,ensure_ascii=False,indent=2))
(ROOT/'docs/source-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
if failed:raise SystemExit('Audit mismatches: '+', '.join(failed))
