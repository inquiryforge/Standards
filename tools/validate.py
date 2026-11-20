"""Offline integrity checks for records, hierarchy, sources, coverage, and links.
Run: python tools/validate.py. Requires only Python's standard library.
"""
from collections import defaultdict,Counter
from pathlib import Path
from urllib.parse import urlsplit,unquote
import hashlib,json,re,unicodedata
from common import ROOT,read_records,KINDS

def require(ok,message):
    if not ok:raise ValueError(message)
def sha(text):return hashlib.sha256(text.encode('utf-8')).hexdigest()
def letters(text):return re.sub(r'[^\w]','',unicodedata.normalize('NFKC',text),flags=re.UNICODE)
def main():
    records=read_records();by_id={n['id']:n for n in records}
    require(len(records)==len(by_id),'Duplicate IDs')
    require(len({n['path'].casefold() for n in records})==len(records),'Case-insensitive path collision')
    fields={'id','parent_id','node_type','code','title','jurisdiction','subject','framework','edition','grade_band','status','source','children','path','text','notes'}
    sources={s['id']:s for s in json.loads((ROOT/'sources/manifest.json').read_text(encoding='utf-8'))}
    for src in sources.values():
        require(hashlib.sha256((ROOT/src['file']).read_bytes()).hexdigest()==src['sha256'],'Source checksum mismatch: '+src['file'])
        if 'layout_file' in src:require(hashlib.sha256((ROOT/src['layout_file']).read_bytes()).hexdigest()==src['layout_sha256'],'Layout checksum mismatch')
    code_scopes=set()
    for n in records:
        require(fields<=n.keys(),'Missing metadata: '+n['id'])
        require(n['title'] and n['jurisdiction']=='US-MI','Invalid title/jurisdiction: '+n['id'])
        require(n['node_type'] in {'group','collection','domain','cluster','strand','topic','standard','substandard','state-extension','not-applicable'},'Unknown node type: '+n['id'])
        expected_status='active' if n['node_type'] in KINDS else ('not-applicable' if n['node_type']=='not-applicable' else 'structural')
        require(n['status']==expected_status,'Invalid record status: '+n['id'])
        require(all(isinstance(g,int) and 0<=g<=12 for g in n['grade_band']),'Invalid grade: '+n['id'])
        if n['parent_id']:
            require(n['parent_id'] in by_id,'Missing parent: '+n['id'])
            parent=by_id[n['parent_id']]
            require(n['id'] in parent['children'],'Parent omits child: '+n['id'])
            require(Path(n['path']).parent.parent==Path(parent['path']).parent,'File not nested under parent: '+n['id'])
        require(len(n['children'])==len(set(n['children'])),'Repeated children: '+n['id'])
        for cid in n['children']:require(cid in by_id and by_id[cid]['parent_id']==n['id'],'Invalid child: '+n['id'])
        ancestors=set();current=n
        while current['parent_id']:
            require(current['id'] not in ancestors,'Parent cycle: '+n['id']);ancestors.add(current['id']);current=by_id[current['parent_id']]
        if n['node_type'] in KINDS:
            require(n['text'] and n['code'] and n['source'],'Incomplete standard: '+n['id'])
            container=n
            while container['parent_id'] and container['node_type']!='collection':container=by_id[container['parent_id']]
            key=(container['id'],n['code'])
            require(key not in code_scopes,'Repeated code within a collection: '+n['id'])
            code_scopes.add(key)
        if n['text']:require(n.get('text_sha256')==sha(n['text']),'Text checksum stale: '+n['id'])
        require('\ufffd' not in n['text'],'Invalid extracted character: '+n['id'])
        require(len(str(ROOT/n['path']))<240,'Windows path too long: '+n['id'])
        for ref in n['source']:
            require(ref['source_id'] in sources,'Unknown source: '+n['id'])
            if 'pages' in ref:require(all(isinstance(p,int) and p>0 for p in ref['pages']),'Invalid PDF page: '+n['id'])
        if n['subject']=='social-studies':
            require(n['edition']=='2019','Wrong social studies edition: '+n['id'])
            if n['node_type']=='standard':require(n['source'][0]['source_id']=='mde:social-studies2019','Social studies source differs from the 2019 publication: '+n['id'])
    catalog=json.loads((ROOT/'catalog.json').read_text(encoding='utf-8'))['records']
    require(len(catalog)==len(records) and {n['id']:n for n in catalog}==by_id,'Catalog does not match the record files')
    coverage=json.loads((ROOT/'sources/social-studies-2019-coverage.json').read_text(encoding='utf-8'))
    source=sources[coverage['source_id']]
    require(source['sha256']==coverage['source_sha256'],'Wrong official source version')
    layout=json.loads((ROOT/source['layout_file']).read_text(encoding='utf-8'))
    all_owned=defaultdict(dict)
    for n in records:
        for ref in n['source']:
            if ref['source_id']!=coverage['source_id']:continue
            for span in ref.get('line_spans',[]):
                page=span['page'];lines=span['lines']
                for line in lines:
                    require(str(line) not in all_owned[str(page)],'Official source line has multiple owners')
                    all_owned[str(page)][str(line)]=n['id']
                if n['node_type']!='standard':continue
                raw='\n'.join(layout[page-1][i-1]['text'] for i in lines)
                # Body text on repeated HS process pages is explicitly versioned.
                variants={v['page']:v['text'] for v in n.get('source_variants',[])}
                target=variants.get(page,n['text'])
                printed=n['source_code']
                first=raw.splitlines()[0]
                if first.startswith(printed):raw=raw[len(printed):].lstrip()
                else:require(page!=ref['pages'][0],'Cannot locate printed code: '+n['id'])
                if n.get('title_origin')=='source-heading' and raw.startswith(n['title']):raw=raw[len(n['title']):].lstrip()
                if len(ref['line_spans'])>1 and not n['id'].startswith('MI.SS.2019.HS.PS.'):
                    # Page continuations are verified as one combined body below.
                    continue
                require(letters(raw)==letters(target),'Official body text differs: '+n['id']+' page '+str(page))
            if n['node_type']=='standard' and len(ref.get('line_spans',[]))>1 and not n['id'].startswith('MI.SS.2019.HS.PS.'):
                raw='\n'.join(layout[sp['page']-1][i-1]['text'] for sp in ref['line_spans'] for i in sp['lines'])
                require(raw.startswith(n['source_code']),'Missing printed code: '+n['id'])
                raw=raw[len(n['source_code']):].lstrip()
                if n.get('title_origin')=='source-heading':raw=raw.removeprefix(n['title']).lstrip()
                require(letters(raw)==letters(n['text']),'Multipage official text differs: '+n['id'])
    require(dict(all_owned)==coverage['line_ownership'],'Social studies source ownership map differs')
    for page,assign in all_owned.items():require(set(map(int,assign))==set(range(1,len(layout[int(page)-1])+1)),'Missing source lines on page '+page)
    expected_counts={'K':21,'G01':31,'G02':37,'G03':42,'G04':48,'G05':50,'G06':57,'G07':55,'G08':45,'K02.PS':17,'G03-05.PS':17,'MS.PS':15,'HS.PS':16,'HS.WHG':32,'HS.USH':39,'HS.CIV':54,'HS.ECON':33}
    for scope in coverage['scopes']:
        prefix=scope['collection_id']+'.'
        actual={n['code'] for n in records if n['node_type']=='standard' and n['id'].startswith(prefix)}
        require(actual==set(scope['codes']) and len(actual)==expected_counts[scope['scope']],'Official scope coverage differs: '+scope['scope'])
    require(sum(n['subject']=='social-studies' and n['node_type']=='standard' for n in records)==609,'Expected 609 official social studies standards')
    math_codes={f'6.{d}.{c}.{i}' for d,clusters in {'RP':{'A':range(1,4)},'NS':{'A':range(1,2),'B':range(2,5),'C':range(5,9)},'EE':{'A':range(1,5),'B':range(5,9),'C':range(9,10)},'G':{'A':range(1,5)},'SP':{'A':range(1,4),'B':range(4,6)}}.items() for c,nums in clusters.items() for i in nums}
    for parent,subs in {'6.RP.A.3':'abcd','6.NS.C.6':'abc','6.NS.C.7':'abcd','6.EE.A.2':'abc','6.SP.B.5':'abcd'}.items():math_codes.update(parent+l for l in subs)
    require({n['code'] for n in records if n['subject']=='mathematics' and n['grade_band']==[6] and n['node_type'] in KINDS}==math_codes,'Grade 6 math coverage differs')
    ela_codes={f'{s}.6.{i}' for s,count in {'RL':10,'RI':10,'W':10,'SL':6,'L':6}.items() for i in range(1,count+1)}
    for parent,subs in {'W.6.1':'abcde','W.6.2':'abcdef','W.6.3':'abcde','W.6.9':'ab','SL.6.1':'abcd','L.6.1':'abcde','L.6.2':'ab','L.6.3':'ab','L.6.4':'abcd','L.6.5':'abc'}.items():ela_codes.update(parent+l for l in subs)
    require({n['code'] for n in records if n['subject']=='english-language-arts' and n['grade_band']==[6] and n['node_type'] in KINDS|{'not-applicable'}}==ela_codes,'Grade 6 ELA coverage differs')
    require(by_id['MI.ELA.2010.RL.6.8']['node_type']=='not-applicable','RL.6.8 must remain not applicable')
    sci_codes={f'MS-{d}-{i}' for d,count in {'PS1':6,'PS2':5,'PS3':5,'PS4':3,'LS1':8,'LS2':5,'LS3':2,'LS4':6,'ESS1':4,'ESS2':6,'ESS3':5,'ETS1':4}.items() for i in range(1,count+1)}|{'MS-ESS2-5MI'}
    require({n['code'] for n in records if n['subject']=='science' and n['grade_band']==[6,7,8] and n['node_type'] in KINDS}==sci_codes,'Middle school science coverage differs')
    require(by_id['MI.SCI.2015.MS-ESS2-5MI']['parent_id']=='MI.SCI.2015.MS-ESS2-5','Michigan extension parent differs')
    baseline=json.loads((ROOT/'sources/subject-coverage-baseline.json').read_text(encoding='utf-8'))
    actual=Counter(n['subject'] for n in records if n['node_type'] in KINDS)
    require(dict(actual)==baseline['standard_records_by_subject'],'Subject coverage changed: update the source audit and baseline deliberately')
    actual_scopes=Counter(n['subject']+'|'+','.join(map(str,n['grade_band']))+'|'+n['node_type'] for n in records if n['node_type'] in KINDS|{'not-applicable'})
    require(dict(actual_scopes)==baseline['records_by_subject_grade_and_kind'],'Grade/band coverage changed')
    workbook_coverage=json.loads((ROOT/'sources/cte-coverage.json').read_text(encoding='utf-8'))
    require(len(workbook_coverage['programs'])==52,'Expected all 52 CTE program workbooks')
    covered=set()
    for key,owners in workbook_coverage['cell_owners'].items():
        sid,sheet,cell=key.split('|')
        require(sid in sources and re.fullmatch(r'[A-Z]+[1-9]\d*',cell),'Invalid workbook cell reference: '+key)
        for ident in owners:
            require(ident in by_id,'Missing workbook statement: '+ident)
            require(any(ref['source_id']==sid and ref.get('sheet')==sheet and cell in ref.get('cells',[]) for ref in by_id[ident]['source']),'Workbook ownership lacks source evidence: '+ident)
            covered.add(ident)
    require({n['id'] for n in records if n['subject'] in {'career-technical-education','career-readiness'} and n['node_type'] in KINDS}==covered,'Workbook statement coverage differs')
    for path in ROOT.rglob('*.md'):
        if not path.is_file():continue
        for target in re.findall(r'\]\(([^)]+)\)',path.read_text(encoding='utf-8')):
            url=urlsplit(target)
            if url.scheme or not url.path:continue
            require((path.parent/unquote(url.path)).resolve().exists(),'Broken local link: '+str(path.relative_to(ROOT))+' -> '+target)
    print(json.dumps({'records':len(records),'standard_and_substandard_records':sum(n['node_type'] in KINDS for n in records),'subjects':dict(sorted(actual.items())),'cte_program_workbooks':52,'cte_statement_cells':len(workbook_coverage['cell_owners']),'official_2019_social_studies_standards':609,'official_social_studies_source_lines':sum(len(v) for v in all_owned.values()),'checks':'passed'},indent=2))
if __name__=='__main__':main()
