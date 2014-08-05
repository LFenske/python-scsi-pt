#!/usr/bin/env python

# Copyright 2014 Larry Fenske

# This file is part of the Python SCSI Toolkit.

# The Python SCSI Toolkit is free software: you can redistribute it
# and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# The Python SCSI Toolkit is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from ScsiPT import *
from CDB    import *
from Cmd    import *


def dumpbuf(buf):
    """
    Print a ctypes buffer as hexadecimal bytes.
    This code is not pretty.
    """
    a = 0
    for i in buf.raw:
        if a % 16 == 0:
            adr = "%.4x" % a
            hxd = ''
            asc = ''
        hxd += " %.2x" % ord(i)
        asc += i if (32 <= ord(i) and ord(i) < 128) else '.'
        if (a+1) % 16 == 0:
            print adr, "%-49s" % hxd, asc
        a += 1
    if len(asc) != 0:
        print adr, "%-49s" % hxd, asc 

if __name__ == "__main__":
    print "version:", ScsiPT.sg.scsi_pt_version()
    pt = ScsiPT("/dev/sg4")

    cdb_tur = CDB([0,0,0,0,0,0])

    retval = pt.sendcdb(cdb_tur)
    print "retval =", retval

    print "sense"
    dumpbuf(cdb_tur.sense)

    del cdb_tur
    
    alloc = 0xff
    cdb_inq = CDB([0x12,0,0,0,alloc,0])
    cdb_inq.set_data_in(alloc)
    retval = pt.sendcdb(cdb_inq)
    print "retval =", retval

    print "sense"
    dumpbuf(cdb_inq.sense)

    print "inq"
    dumpbuf(cdb_inq.buf)
        
    del cdb_inq
    
    cmd = Cmd("tur")
    print cmd.cdb

    cmd = Cmd("inq", {"evpd":0, "alloc":0xa4})
    print cmd.cdb
    cdb = CDB(cmd.cdb)
    cdb.set_data_in(0xa4)
    pt.sendcdb(cdb)
    dumpbuf(cdb.buf)
    del cdb
    
    del pt

