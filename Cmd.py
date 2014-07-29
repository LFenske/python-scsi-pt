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

class Cmd:
    """
    Manage creating objects of type CDB and filling in parameters.
    """
    
    abbrevs = \
    {
     "tur"  : "test_unit_ready",
     "inq"  : "inquiry",
     
     "alloc": "allocation_length",
     }

    # indices into cdbdefs values
    xCDBNUM = 0
    xLEN    = 1
    xDIR    = 2
    xFLDS   = 3
    # directions (xDIR)
    NONE = "NONE"
    OUT  = "OUT"
    IN   = "IN"
    # definitions of CDBs
    cdbdefs = \
    {
     "test_unit_ready": (0x00, 6, NONE, {}),
     "inquiry"        : (0x12, 6, IN,
                         {
                          "evpd"             :((1,0),1,0),
                          "page_code"        :( 2,   8,0),
                          "allocation_length":( 3,  16,5),
                          }),
     "write_buffer"   : (0x3b,10, OUT,
                         {
                          "mode_specific"        :((1,7),3,0),
                          "mode"                 :((1,4),5,0),
                          "buffer_id"            :( 2,   8,0),
                          "buffer_offset"        :( 3,  24,0),
                          "parameter_list_length":( 6,  24,0),
                          }),
    }
    
    # factory to create a Cmd to set time on a Rockbox device
    @classmethod
    def settime(Cls, year, day, hour, minute, second):
        cmd = Cls("write_buffer", {
                                   "mode":1,
                                   "buffer_id":0,
                                   "buffer_offset":0xc0000,
                                   "parameter_list_length":12,  # Why is this 12 when there are 8 bytes of data?
                                   })
        cmd.dat = [0] * 8
        Cls.fill(cmd.dat,
                  Cmd.data_settime,
                  {"year":year, "day":day, "hour":hour, "minute":minute, "second":second})
        return cmd
    
    data_settime = \
    {
     "year"  :(0,16,0),
     "day"   :(2,16,0),
     "hour"  :(5, 8,0),
     "minute":(6, 8,0),
     "second":(7, 8,0),
     }
    
    data_inquiry = \
    {
     "peripheral qualifier"     : (( 0,7), 3),
     "peripheral device type"   : (( 0,4), 5),
     "rmb"                      : (( 1,0), 1),
     "version"                  : (  2,    8),
     "normaca"                  : (( 3,5), 1),
     "hisup"                    : (( 3,4), 1),
     "response data format"     : (( 3,3), 4),
     "additional length"        : (  4,    8),
     "sccs"                     : (( 5,7), 1),
     "acc"                      : (( 5,6), 1),
     "tpgs"                     : (( 5,5), 2),
     "3pc"                      : (( 5,3), 1),
     "protect"                  : (( 5,0), 1),
     "encserv"                  : (( 6,6), 1),
     "vs"                       : (( 6,5), 1),
     "multip"                   : (( 6,4), 1),
     "mchngr"                   : (( 6,3), 1),
     "addr16"                   : (( 6,0), 1),
     "wbus16"                   : (( 7,5), 1),
     "sync"                     : (( 7,4), 1),
     "cmdque"                   : (( 7,1), 1),
     "vs"                       : (( 7,0), 1),
     "t10 vendor identification": (  8,   64),
     "product identification"   : ( 16,  128),
     "product revision level"   : ( 32,   32),
     "drive serial number"      : ( 36,   64),
     "vendor unique"            : ( 44,   96),
     "clocking"                 : ((56,3), 2),
     "qas"                      : ((56,1), 1),
     "ius"                      : ((56,0), 1),
     "version descriptor 1"     : ( 58,   16),
     "version descriptor 2"     : ( 60,   16),
     "version descriptor 3"     : ( 62,   16),
     "version descriptor 4"     : ( 64,   16),
     "version descriptor 5"     : ( 66,   16),
     "version descriptor 6"     : ( 68,   16),
     "version descriptor 7"     : ( 70,   16),
     "version descriptor 8"     : ( 72,   16),
     }
    peripheral_device_type = \
    {
        0x00: "Direct access block device",
        0x01: "Sequential-access device",
        0x02: "Printer device",
        0x03: "Processor device",
        0x04: "Write-once device",
        0x05: "CD/DVD device",
        0x06: "Scanner device",
        0x07: "Optical memory device",
        0x08: "Medium changer device",
        0x09: "Communications device",
        0x0c: "Storage array controller device",
        0x0d: "Enclosure services device",
        0x0e: "Simplified direct-access device",
        0x0f: "Optical card reader/writer device",
        0x10: "Bridge Controller Commands",
        0x11: "Object-based Storage Device",
        0x12: "Automation/Drive Interface",
        0x1e: "Well known logical unit",
        0x1f: "Unknown or no device type",
        }
    
    def __init__(self, cdbname, params={}):
        # Replace a possible abbreviation.
        if cdbname in self.abbrevs:
            cdbname = self.abbrevs[cdbname]
        # Ensure we know this command.
        if cdbname not in self.cdbdefs:
            raise Exception("bad CDB name")
        d = self.cdbdefs[cdbname]  # shorthand
        # Create initial CDB as all 0's.
        self.cdb = [0] * d[self.xLEN]
        # Fill in all the fields.
        opdef = {"opcode":(0,8,0)}
        opdef.update(d[self.xFLDS])
        opprm = {"opcode":d[self.xCDBNUM]}
        opprm.update(
            {(self.abbrevs[k]
              if k in self.abbrevs else k):v
                for (k,v) in params.items()})
        Cmd.fill(self.cdb, opdef, opprm)

    @staticmethod
    def fill(cdb, defs, pparms):
        """
        Take field values in parms and insert them into cdb based on
        the field definitions in defs.
        """
        print "defs =", defs
        parms = {n:v[2] for (n,v) in defs.items()}  # Create parms for default field values.
        parms.update(pparms)  # Insert real parameters.
        for (name, value) in parms.items():
            if name not in defs:
                raise Exception("unknown field: "+name)
            length = defs[name][1]
            if value >= 1<<length:
                raise Exception("value too large for field: "+name)
            start = defs[name][0]
            if type(start) == type(0):  # must be either number or list of 2
                start = (start,7)
            # TODO Check type of start.
            startbitnum = start[0]*8 + (7-start[1])  # Number bits l-to-r.
            bitnum = startbitnum + defs[name][1] - 1
            # TODO Is value inserted backwards?
            while length > 0:
                if bitnum % 8 == 7 and length >= 8:
                    bitlen= 8
                    cdb[bitnum//8] = value & 0xff;
                else:
                    startofbyte = bitnum // 8 * 8  # Find first bit num in byte.
                    firstbit = max(startofbyte, bitnum-length+1)
                    bitlen= bitnum-firstbit+1
                    shift = (7 - bitnum%8)
                    vmask = (1 << bitlen) - 1
                    bmask = ~(vmask << shift)
                    cdb[bitnum//8] &= bmask
                    cdb[bitnum//8] |= (value & vmask) << shift
                bitnum -= bitlen
                value >>= bitlen
                length -= bitlen
        
        
