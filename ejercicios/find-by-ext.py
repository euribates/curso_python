#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import sys
import os


def find_by_ext(ext):
    result = 0
    for (dirpath, dirnames, filenames) in os.walk('.'):
        for filename in filenames:
            if filename.lower().endswith(ext):
                fullname = os.path.join(dirpath, filename)
                size = os.path.getsize(fullname) 
                result += size
                print(fullname, size, 'bytes')


if __name__ == '__main__':
    argc = len(sys.argv)
    if argc < 2:
        print('Tiene que especificar la extensión que busca')
        sys.exit(-1)
    ext = sys.argv[1].lower()
    print('Buscando ficheros con extensión {}'.format(ext))
    acc = find_by_ext(ext)
    print('Bytes totales:', acc)