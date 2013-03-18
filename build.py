#!/usr/bin/env python

import glob
import time
import re
import io
import base64
import os

def readfile(fn):
    with io.open(fn, 'Ur', encoding='utf8') as f:
        return f.read()

def loaderString(var):
    fn = var.group(1)
    return readfile(fn).replace('\n', '\\n').replace('\'', '\\\'')

def loaderRaw(var):
    fn = var.group(1)
    return readfile(fn)

def loaderImage(var):
    fn = var.group(1)
    return 'data:image/png;base64,{0}'.format(str(base64.encodestring(open(fn, 'rb').read())).replace('\n', ''))

def subIncludes(m):
    m = m.replace('@@BUILDDATE@@', time.strftime('%Y-%m-%d-%H%M%S'))
    m = re.sub('@@INCLUDERAW:([0-9a-zA-Z_./-]+)@@', loaderRaw, m)
    m = re.sub('@@INCLUDESTRING:([0-9a-zA-Z_./-]+)@@', loaderString, m)
    m = re.sub('@@INCLUDEIMAGE:([0-9a-zA-Z_./-]+)@@', loaderImage, m)
    return m

c = '\n\n'.join(map(readfile, glob.glob('code/*')))
m = readfile('main.js')

m = m.split('@@INJECTHERE@@')
m.insert(1, c)
m = '\n\n'.join(m)

m = subIncludes(m)

try:
    os.makedirs('built/plugins')
except OSError as exception:
    if exception.errno != errno.EEXIST:
        raise

with io.open('built/iitc-debug.user.js', 'w', encoding='utf8') as f:
    f.write(m)

for fn in glob.glob('plugins/*.js'):
  m = readfile(fn)

  m = subIncludes(m)

  with io.open('built/' + fn, 'w', encoding='utf8') as f:
      f.write(m)

# vim: ai si ts=4 sw=4 sts=4 et
