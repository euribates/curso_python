#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import os
import zipfile

def find_zip():
    for (dirpath, dirnames, filenames) in os.walk('.'):
        for filename in filenames:
            if filename.lower().endswith('.zip'):
                fullname = os.path.join(dirpath, filename)
                yield fullname

if __name__ == '__main__':
    print('Buscando ficheros zip')
    for fn in find_zip():
        print('Fichero:', fn)
        zf = zipfile.ZipFile(fn, 'r')
        for fn in zf.namelist():
            print(' - {}'.format(fn))
        print('-'*80)