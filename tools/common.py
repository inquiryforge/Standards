"""Read the single-record Markdown format (standard library only)."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
START='<!-- standard-text:start -->'
END='<!-- standard-text:end -->'
KINDS={'standard','substandard','state-extension'}
def read_records():
    records=[]
    for path in sorted((ROOT/'standards').rglob('README.md')):
        raw=path.read_text(encoding='utf-8')
        if not raw.startswith('---\n'):continue
        front,body=raw[4:].split('\n---\n',1)
        record={}
        for line in front.splitlines():
            k,v=line.split(': ',1);record[k]=json.loads(v)
        assert record['path']==path.relative_to(ROOT).as_posix(),str(path)
        assert body.count(START)==body.count(END)<=1,str(path)
        record['text']=body.split(START+'\n',1)[1].split('\n'+END,1)[0] if START in body else ''
        records.append(record)
    return records
