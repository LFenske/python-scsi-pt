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

#import sys
#sys.path.append('/home/larry/git/ih/listdict')

from listdict import ListDict

class Cmd(object):
    """
    Manage creating objects of type CDB and filling in parameters.
    """
    
    abbrevs = \
    {
     # commands
     "tur"  : "test_unit_ready",
     "inq"  : "inquiry",
     "wb"   : "write_buffer",
     "sd"   : "send_diagnostic",
     "rdr"  : "receive_diagnostic_results",
     
     # fields
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
     "send_diagnostic": (0x1d, 6, OUT,
                         {
                          "self-test_code"       :((1,7),3,0),
                          "pf"                   :((1,4),1,0),
                          "selftest"             :((1,2),1,0),
                          "devoffl"              :((1,1),1,0),
                          "unitoffl"             :((1,0),1,0),
                          "parameter_list_length":( 3,  16,0),
                          }),
     "receive_diagnostic_results":
                        (0x1c, 6, IN,
                         {
                          "pcv"              :((1,0),1,0),
                          "page_code"        :( 2,   8,0),
                          "allocation_length":( 3,  16,5),
                          }),
    }
    
    data_inquiry = \
    (
     (( 0,7), 3, "int", "qual", "peripheral qualifier"     ),
     (( 0,4), 5, "int", "type", "peripheral device type"   ),
     (( 1,0), 1, "int", None  , "rmb"                      ),
     (  2,    8, "int", None  , "version"                  ),
     (( 3,5), 1, "int", None  , "normaca"                  ),
     (( 3,4), 1, "int", None  , "hisup"                    ),
     (( 3,3), 4, "int", None  , "response data format"     ),
     (  4,    8, "int", None  , "additional length"        ),
     (( 5,7), 1, "int", None  , "sccs"                     ),
     (( 5,6), 1, "int", None  , "acc"                      ),
     (( 5,5), 2, "int", None  , "tpgs"                     ),
     (( 5,3), 1, "int", None  , "3pc"                      ),
     (( 5,0), 1, "int", None  , "protect"                  ),
     (( 6,6), 1, "int", None  , "encserv"                  ),
     (( 6,5), 1, "int", None  , "vs"                       ),
     (( 6,4), 1, "int", None  , "multip"                   ),
     (( 6,3), 1, "int", None  , "mchngr"                   ),
     (( 6,0), 1, "int", None  , "addr16"                   ),
     (( 7,5), 1, "int", None  , "wbus16"                   ),
     (( 7,4), 1, "int", None  , "sync"                     ),
     (( 7,1), 1, "int", None  , "cmdque"                   ),
     (( 7,0), 1, "int", None  , "vs"                       ),
     (  8,   64, "str", "vid" , "t10 vendor identification"),
     ( 16,  128, "str", "pid" , "product identification"   ),
     ( 32,   32, "str", "rev" , "product revision level"   ),
     ( 36,   64, "str", "sn"  , "drive serial number"      ),
     ( 44,   96, "str", None  , "vendor unique"            ),
     ((56,3), 2, "int", None  , "clocking"                 ),
     ((56,1), 1, "int", None  , "qas"                      ),
     ((56,0), 1, "int", None  , "ius"                      ),
     ( 58,   16, "int", None  , "version descriptor 1"     ),
     ( 60,   16, "int", None  , "version descriptor 2"     ),
     ( 62,   16, "int", None  , "version descriptor 3"     ),
     ( 64,   16, "int", None  , "version descriptor 4"     ),
     ( 66,   16, "int", None  , "version descriptor 5"     ),
     ( 68,   16, "int", None  , "version descriptor 6"     ),
     ( 70,   16, "int", None  , "version descriptor 7"     ),
     ( 72,   16, "int", None  , "version descriptor 8"     ),
     )
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
    send_diagnostic_self_test_code = \
        {
        0: "",
        1: "Background short self-test",
        2: "Background extended self-test",
        3: "Reserved",
        4: "Abort background self-test",
        5: "Foreground short self-test",
        6: "Foreground extended self-test",
        7: "Reserved",
        }
    
    def __init__(self, cdbname, params={}):
        super(Cmd, self).__init__()
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
        #print "defs =", defs
        parms = {n:v[2] for (n,v) in defs.items()}  # Create parms for default field values.
        parms.update(pparms)  # Insert real parameters.
        for (name, value) in parms.items():
            if name not in defs:
                raise Exception("unknown field: "+name)
            width = defs[name][1]
            if value >= 1<<width:
                raise Exception("value too large for field: "+name)
            start = defs[name][0]
            if type(start) == type(0):  # must be either number or list of 2
                start = (start,7)
            # TODO Check type of start.
            startbitnum = start[0]*8 + (7-start[1])  # Number bits l-to-r.
            bitnum = startbitnum + defs[name][1] - 1
            # TODO Is value inserted backwards?
            while width > 0:
                if bitnum % 8 == 7 and width >= 8:
                    bitlen= 8
                    cdb[bitnum//8] = value & 0xff;
                else:
                    startofbyte = bitnum // 8 * 8  # Find first bit num in byte.
                    firstbit = max(startofbyte, bitnum-width+1)
                    bitlen= bitnum-firstbit+1
                    shift = (7 - bitnum%8)
                    vmask = (1 << bitlen) - 1
                    bmask = ~(vmask << shift)
                    cdb[bitnum//8] &= bmask
                    cdb[bitnum//8] |= (value & vmask) << shift
                bitnum -= bitlen
                value >>= bitlen
                width  -= bitlen
    
    class Field:
        def __init__(self, val, byteoffset, name, desc):
            self.val        = val
            self.byteoffset = byteoffset
            self.name       = name
            self.desc       = desc
            
        def __str__(self):
            return '(' + str(self.val) + ', ' + str(self.byteoffset) + ', "' + self.name + '", "' + self.desc + '")'
    
    @staticmethod
    def extract(data, defs, byteoffset=0):
        """
        Extract fields from data into a tuple based on field definitions in defs.
        byteoffset is added to each local byte offset to get the byte offset returned for each field.
        Return a ListDict of Fields.
        
        defs is a list of lists composed of start, width in bits, format, nickname, description.
        field start is either a byte number or a tuple with byte number and bit number.
        
        Return a ListDict of Fields.
        """
        
        retval = ListDict()
        for fielddef in defs:
            start, width, form, name, desc = fielddef
            if form == "int":
                if type(start) == type(0):
                    # It's a number. Convert it into a (bytenum,bitnum) tuple.
                    start = (start,7)
                ix, bitnum = start
                val = 0
                while (width > 0):
                    if bitnum == 7 and width >= 8:
                        val = (val << 8) | ord(data[ix])
                        ix += 1
                        width -= 8
                    else:
                        lastbit = bitnum+1 - width
                        if lastbit < 0:
                            lastbit = 0
                        thiswidth = bitnum+1 - lastbit
                        val = (val << thiswidth) | ((ord(data[ix]) >> lastbit) & ((1<<thiswidth)-1))
                        bitnum = 7
                        ix += 1
                        width -= thiswidth
                retval.append(Cmd.Field(val, byteoffset+start[0], name, desc), name)
            elif form == "str":
                assert(type(start) == type(0))
                assert(width % 8 == 0)
                retval.append(Cmd.Field(data[start:start+width/8], byteoffset+start, name, desc), name)
            else:
                # error in form
                pass
        return retval
    
#    @staticmethod
#    def extractdict(data, defs, byteoffset=0):
#        return Cmd.extracttodict(Cmd.extract(data, defs, byteoffset))
#    
#    @staticmethod
#    def extracttodict(extractresults):
#        return {field.name: field for field in extractresults if field.name}
    
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
    
        
