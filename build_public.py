"""Build the public GitHub Pages copy of The Sporting Reporter from the Claude artifact page.
Usage: python3 build_public.py <artifact index.html> <output index.html>"""
import sys, re
src=open(sys.argv[1],encoding='utf-8').read()
# drop the artifact skeleton if present, keep page content
m=re.search(r'<body>(.*)</body></html>\s*$',src,re.S)
body=m.group(1) if m else src
body=body.replace('<a href="#ask">Ask the Reporter</a>','')
body=body.replace("Questions are available when this page is opened in Claude. For anything else, email jessefader27@gmail.com.","Questions or feedback? Email jessefader27@gmail.com.")
head=('<!doctype html><html lang="en"><head><meta charset="utf-8">'
 '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
 '<meta name="robots" content="noindex,nofollow">'
 '<style>:root{box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}img{max-width:100%}</style>'
 '</head><body>')
open(sys.argv[2],'w',encoding='utf-8').write(head+body+'</body></html>')
print('ok', len(head+body))
