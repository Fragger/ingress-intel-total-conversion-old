#!/usr/bin/env python

import glob
import time
import re
import io
import base64

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


c = '\n\n'.join(map(readfile, glob.glob('code/*')))
n = time.strftime('%Y-%m-%d-%H%M%S')
m = readfile('main.js')

m = m.split('@@INJECTHERE@@')
m.insert(1, c)
m = '\n\n'.join(m)

m = m.replace('@@BUILDDATE@@', n)
m = re.sub('@@INCLUDERAW:([0-9a-zA-Z_./-]+)@@', loaderRaw, m)
m = re.sub('@@INCLUDESTRING:([0-9a-zA-Z_./-]+)@@', loaderString, m)
m = re.sub('@@INCLUDEIMAGE:([0-9a-zA-Z_./-]+)@@', loaderImage, m)

with io.open('iitc-debug.user.js', 'w', encoding='utf8') as f:
    f.write(m)

# vim: ai si ts=4 sw=4 sts=4 et
