# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import zipfile
from cStringIO import StringIO


class Zip(object):
    def __init__(self):
        self.__io = StringIO()
        self.__zf = zipfile.ZipFile(self.__io, 'a', zipfile.ZIP_DEFLATED, False)

    def add_file(self, io, aname):
        if aname not in self.__zf.namelist():
            self.__zf.writestr(zipfile.ZipInfo(aname), io.getvalue(), zipfile.ZIP_DEFLATED)
            io.seek(0)
        return self

    def __close(self):
        self.__zf.close()
        self.__io.seek(0)

    def output(self):
        self.__close()
        return self.__io

    @property
    def size(self):
        self.__io.seek(0, 2)
        size = self.__io.tell()
        self.__io.seek(0)
        return size


if __name__ == '__main__':
    import glob
    zip = Zip()
    for filename in glob.glob('*.py'):
        with open(filename) as f:
            io = StringIO(f.read())
            io.seek(0)
        zip.add_file(io, filename)

    output_io = zip.output()
    with open('xxx.zip', 'wb') as f:
        f.write(output_io.getvalue())