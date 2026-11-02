"""Archive and backup helper for The Sporting Reporter data store.

Usage:
  python3 data_tools.py archive <collection> <YYYY-MM> <records.json>
      records.json is a JSON object {doc_id: record}. Merges them into
      data/archive/<collection>-<YYYY-MM>.json (adds new ids, never removes any),
      then prints: ARCHIVE <path> <total records in file> <records added>
  python3 data_tools.py count <path>
      Prints the number of records in an archive or backup file.
  python3 data_tools.py verify <collection> <YYYY-MM> <records.json>
      Exits 0 and prints OK only if every doc id in records.json is in the archive
      file with identical content. Use it after pushing and before deleting anything.
  python3 data_tools.py backup <YYYY-MM> <dir>
      <dir> holds one <collection>.json per live collection ({doc_id: record}).
      Writes data/backup/live-<YYYY-MM>.json with all of them and prints the counts.
Archive files are only ever added to; nothing here deletes data.
"""
import sys, json, os, re
ROOT=os.path.dirname(os.path.abspath(__file__))
def load(p):
    if not os.path.exists(p): return {}
    d=json.load(open(p,encoding='utf-8'))
    return d.get('records',d) if isinstance(d,dict) else {}
def save(p,meta,recs):
    os.makedirs(os.path.dirname(p),exist_ok=True)
    json.dump(dict(meta,count=len(recs),records=dict(sorted(recs.items()))),open(p,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
def apath(c,m):
    assert re.fullmatch(r'[a-z_]+',c) and re.fullmatch(r'\d{4}-\d{2}',m), 'bad collection or month'
    return os.path.join(ROOT,'data','archive',f'{c}-{m}.json')
cmd=sys.argv[1] if len(sys.argv)>1 else ''
if cmd=='archive':
    c,m,src=sys.argv[2:5]; p=apath(c,m); have=load(p); new=json.load(open(src,encoding='utf-8'))
    added=0
    for k,v in new.items():
        if k not in have: have[k]=v; added+=1
    save(p,{'collection':c,'month':m},have); print('ARCHIVE',os.path.relpath(p,ROOT),len(have),added)
elif cmd=='count':
    print(len(load(sys.argv[2])))
elif cmd=='verify':
    c,m,src=sys.argv[2:5]; have=load(apath(c,m)); new=json.load(open(src,encoding='utf-8'))
    bad=[k for k,v in new.items() if have.get(k)!=v]
    if bad: print('MISSING_OR_DIFFERENT',len(bad),bad[:5]); sys.exit(1)
    print('OK',len(new))
elif cmd=='backup':
    m,d=sys.argv[2:4]; out={}
    for f in sorted(os.listdir(d)):
        if f.endswith('.json'): out[f[:-5]]=json.load(open(os.path.join(d,f),encoding='utf-8'))
    p=os.path.join(ROOT,'data','backup',f'live-{m}.json'); os.makedirs(os.path.dirname(p),exist_ok=True)
    json.dump({'month':m,'collections':out},open(p,'w',encoding='utf-8'),ensure_ascii=False)
    print('BACKUP',os.path.relpath(p,ROOT),{k:len(v) for k,v in out.items()})
else:
    print(__doc__); sys.exit(2)
