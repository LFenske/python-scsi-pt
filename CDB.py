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

import ctypes
from ScsiPT import ScsiPT

class CDB(object):
    """
    Manage the data structure that holds a passthrough request.
    """
    
    def __init__(self, cdb, rs_size=24):
        # Construct CDB object for a passthrough request.
        super(CDB, self).__init__()
        self.objp = ScsiPT.sg.construct_scsi_pt_obj()
        if self.objp == None:
            raise Exception()
        # Add CDB to the object.
        self.cdb = ctypes.create_string_buffer(str(bytearray(cdb)), len(cdb))
        ScsiPT.sg.set_scsi_pt_cdb(self.objp, self.cdb, len(self.cdb))
        # Add Request Sense buffer to object.
        self.sense = ctypes.create_string_buffer(rs_size)
        ScsiPT.sg.set_scsi_pt_sense(self.objp, self.sense, len(self.sense))
        
    def __del__(self):
        # Destruct the object, if it exists.
        if self.objp != None:
            ScsiPT.sg.destruct_scsi_pt_obj(self.objp)
            self.objp = None
        #super(CDB, self).__del__()
            
    def set_data_out(self, buf):
        self.buf = ctypes.create_string_buffer(str(bytearray(buf)), len(buf))
        retval = ScsiPT.sg.set_scsi_pt_data_out(
            self.objp,
            self.buf,
            len(self.buf))
        if retval < 0:
            raise Exception(retval)

    def set_data_in(self, buflen):
        self.buf = ctypes.create_string_buffer(buflen)
        retval = ScsiPT.sg.set_scsi_pt_data_in(
            self.objp,
            self.buf,
            len(self.buf))
        if retval < 0:
            raise Exception(retval)


