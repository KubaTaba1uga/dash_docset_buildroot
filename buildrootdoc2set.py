#!/usr/local/bin/python

import os, re, sqlite3
from bs4 import BeautifulSoup 

conn = sqlite3.connect('buildroot.docset/Contents/Resources/docSet.dsidx')
cur = conn.cursor()

try: cur.execute('DROP TABLE searchIndex;')
except: pass
cur.execute('CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, type TEXT, path TEXT);')
cur.execute('CREATE UNIQUE INDEX anchor ON searchIndex (name, type, path);')

docpath = 'buildroot.docset/Contents/Resources/Documents/'

page = open(os.path.join(docpath,'manual.html')).read()
soup = BeautifulSoup(page)

any = re.compile('.*')
paths = []
names = []
for tag in soup.find_all('a', {'href':any}):
    name = tag.text.strip()
    if len(name) > 1:
        path = tag.attrs['href']
        if path in paths or name in names:
            continue
        if path != 'manual.html' and "#" in path and not "http" in path and not name.startswith("["):
            path = f"manual.html{path}"
            cur.execute('INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?)', (name, 'func', path))
            print('name: %s, path: %s' % (name, path))
            paths.append(path)
            names.append(name)

conn.commit()
conn.close()
