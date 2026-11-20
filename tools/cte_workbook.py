"""Read workbook XML cells and retain source coordinates and merged-cell origins."""
import zipfile,xml.etree.ElementTree as ET,posixpath,re
NS={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}

def workbook(path):
    result={}
    with zipfile.ZipFile(path) as z:
        strings=[]
        if 'xl/sharedStrings.xml' in z.namelist():strings=[''.join(t.text or '' for t in si.iter('{'+NS['s']+'}t')) for si in ET.fromstring(z.read('xl/sharedStrings.xml'))]
        relationships={r.attrib['Id']:r.attrib['Target'] for r in ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
        for sheet in ET.fromstring(z.read('xl/workbook.xml')).find('s:sheets',NS):
            name=sheet.attrib['name'];target=relationships[sheet.attrib['{'+NS['r']+'}id']]
            if not any(k in name.lower() for k in ['standard','competenc','career ready','table of content','pcc','gap analysis']):continue
            target=target.lstrip('/') if target.startswith('/') else posixpath.normpath('xl/'+target)
            xml=ET.fromstring(z.read(target));cells={}
            for c in xml.iter('{'+NS['s']+'}c'):
                value=c.find('s:v',NS);inline=c.find('s:is',NS)
                if c.attrib.get('t')=='s' and value is not None:text=strings[int(value.text)]
                elif inline is not None:text=''.join(t.text or '' for t in inline.iter('{'+NS['s']+'}t'))
                elif value is not None:
                    text=value.text
                    if text and c.attrib.get('t','n')=='n':
                        try:text=format(float(text),'.12g')
                        except ValueError:pass
                else:continue
                if text is not None and str(text).strip():cells[c.attrib['r']]={'text':str(text),'origin':c.attrib['r']}
            merges=xml.find('s:mergeCells',NS)
            if merges is not None:
                for merge in merges:
                    a,b=merge.attrib['ref'].split(':')
                    ma=re.match(r'([A-Z]+)(\d+)',a);mb=re.match(r'([A-Z]+)(\d+)',b)
                    if ma[1]==mb[1] and a in cells:
                        for row in range(int(ma[2])+1,int(mb[2])+1):cells.setdefault(ma[1]+str(row),cells[a])
            result[name]=cells
    return result

def rows(cells):
    output={}
    for coordinate,entry in cells.items():
        match=re.match(r'([A-Z]+)(\d+)',coordinate)
        output.setdefault(int(match[2]),{})[match[1]]=entry
    return dict(sorted(output.items()))
