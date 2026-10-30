"""Build the public GitHub Pages copy of The Sporting Reporter from the published page.
Usage: python3 build_public.py <published index.html> <output index.html>"""
import sys, re
src=open(sys.argv[1],encoding='utf-8').read()
# drop the hosting skeleton if present, keep page content
m=re.search(r'<body>(.*)</body></html>\s*$',src,re.S)
body=m.group(1) if m else src
# questions box: not available on the public copy
body=body.replace('<a href="#ask">Ask the Reporter</a>','')
body=re.sub(r'<!--ASK-VIEW-->.*?<!--/ASK-VIEW-->',
  '<p class="muted" style="margin:0">Questions or feedback? Email jessefader27@gmail.com.</p>',body,flags=re.S)
body=re.sub(r'/\*ASK-JS\*/.*?/\*/ASK-JS\*/','',body,flags=re.S)
# signed-in sync of opened packs: browser storage only on the public copy
body=re.sub(r'/\*SYNC-JS\*/.*?/\*/SYNC-JS\*/','',body,flags=re.S)
# host-only meta tags
body=re.sub(r'<meta name="claude:[^"]*"[^>]*>\n?','',body)
body=body.replace("Questions are available when this page is opened in Claude. For anything else, email jessefader27@gmail.com.","Questions or feedback? Email jessefader27@gmail.com.")
# comparison links point at this page
body=re.sub(r'var ART_URL="[^"]*";','var ART_URL=location.href.split("#")[0];',body)
# remove HTML comments (build notes)
body=re.sub(r'<!--(?!\[).*?-->','',body,flags=re.S)
head=('<!doctype html><html lang="en"><head><meta charset="utf-8">'
 '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
 '<meta name="robots" content="noindex,nofollow">'
 
 '<style>:root{box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}img{max-width:100%}</style>'
 '</head><body>')
out=head+body+'</body></html>'
bad=[w for w in re.findall(r'(?i)claude|anthropic|scheduled (?:task|update)|ask-js|ask-view|sync-js',out)]
if bad:
    sys.exit('public copy still mentions: '+', '.join(sorted(set(bad))))
open(sys.argv[2],'w',encoding='utf-8').write(out)
# plain-text edition stamp next to the page, so the live site can be checked without running its scripts
import json, os
d=json.loads(re.search(r'id="pulse-data">(.*?)</script>',out,re.S).group(1).replace('<\\/','</'))
stamp=os.path.join(os.path.dirname(os.path.abspath(sys.argv[2])),'edition.txt')
open(stamp,'w',encoding='utf-8').write('edition: %s\nupdated: %s\n'%(d.get('edition',''),d.get('updated','')))
print('ok', len(out), d.get('updated'))
