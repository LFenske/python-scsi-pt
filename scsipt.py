#!/usr/bin/env python

import ctypes

class ScsiPT:
    
    sg = ctypes.CDLL("libsgutils2.so")
    sg.scsi_pt_version              .restype = ctypes.c_char_p
    sg.scsi_pt_version              .argtypes = []
    sg.scsi_pt_open_device          .restype = ctypes.c_int
    sg.scsi_pt_open_device          .argtypes = [ctypes.c_char_p,
                                               ctypes.c_int,
                                               ctypes.c_int]
    sg.scsi_pt_open_flags           .restype = ctypes.c_int
    sg.scsi_pt_open_flags           .argtypes = [ctypes.c_char_p,
                                               ctypes.c_int,
                                               ctypes.c_int]
    sg.scsi_pt_close_device         .restype = ctypes.c_int
    sg.scsi_pt_close_device         .argtypes = [ctypes.c_int]
    sg.construct_scsi_pt_obj        .restype = ctypes.c_void_p
    sg.construct_scsi_pt_obj        .argtypes = []
    sg.clear_scsi_pt_obj            .restype = ctypes.c_int # void
    sg.clear_scsi_pt_obj            .argtypes = [ctypes.c_void_p]
    sg.set_scsi_pt_cdb              .restype = ctypes.c_int # void
    sg.set_scsi_pt_cdb              .argtypes = [ctypes.c_void_p,
                                               ctypes.c_char_p,
                                               ctypes.c_int]
    sg.set_scsi_pt_sense            .restype = ctypes.c_int # void
    sg.set_scsi_pt_sense            .argtypes = [ctypes.c_void_p,
                                               ctypes.c_char_p,
                                               ctypes.c_int]
    sg.set_scsi_pt_data_in          .restype = ctypes.c_int # void
    sg.set_scsi_pt_data_in          .argtypes = [ctypes.c_void_p,
                                               ctypes.c_char_p,
                                               ctypes.c_int]
    sg.set_scsi_pt_data_out         .restype = ctypes.c_int # void
    sg.set_scsi_pt_data_out         .argtypes = [ctypes.c_void_p,
                                               ctypes.c_char_p,
                                               ctypes.c_int]
    sg.set_scsi_pt_packet_id        .restype = ctypes.c_int # void
    sg.set_scsi_pt_packet_id        .argtypes = [ctypes.c_void_p,
                                               ctypes.c_int]
    sg.set_scsi_pt_tag              .restype = ctypes.c_int # void
    sg.set_scsi_pt_tag              .argtypes = [ctypes.c_void_p,
                                               ctypes.c_ulong]
    sg.set_scsi_pt_task_management  .restype = ctypes.c_int # void
    sg.set_scsi_pt_task_management  .argtypes = [ctypes.c_void_p,
                                               ctypes.c_int]
    sg.set_scsi_pt_task_attr        .restype = ctypes.c_int # void
    sg.set_scsi_pt_task_attr        .argtypes = [ctypes.c_void_p,
                                               ctypes.c_int,
                                               ctypes.c_int]
    sg.set_scsi_pt_flags            .restype = ctypes.c_int # void
    sg.set_scsi_pt_flags            .argtypes = [ctypes.c_void_p,
                                               ctypes.c_int]
    sg.do_scsi_pt                   .restype = ctypes.c_int
    sg.do_scsi_pt                   .argtypes = [ctypes.c_void_p,
                                               ctypes.c_int,
                                               ctypes.c_int,
                                               ctypes.c_int]
    sg.get_scsi_pt_result_category  .restype = ctypes.c_int
    sg.get_scsi_pt_result_category  .argtypes = [ctypes.c_void_p]
    sg.get_scsi_pt_resid            .restype = ctypes.c_int
    sg.get_scsi_pt_resid            .argtypes = [ctypes.c_void_p]
    sg.get_scsi_pt_status_response  .restype = ctypes.c_int
    sg.get_scsi_pt_status_response  .argtypes = [ctypes.c_void_p]
    sg.get_scsi_pt_sense_len        .restype = ctypes.c_int
    sg.get_scsi_pt_sense_len        .argtypes = [ctypes.c_void_p]
    sg.get_scsi_pt_os_err           .restype = ctypes.c_int
    sg.get_scsi_pt_os_err           .argtypes = [ctypes.c_void_p]
    sg.get_scsi_pt_os_err_str       .restype = ctypes.c_char_p
    sg.get_scsi_pt_os_err_str       .argtypes = [ctypes.c_void_p,
                                               ctypes.c_int,
                                               ctypes.c_char_p]
    sg.get_scsi_pt_transport_err    .restype = ctypes.c_int
    sg.get_scsi_pt_transport_err    .argtypes = [ctypes.c_void_p]
    sg.get_scsi_pt_transport_err_str.restype = ctypes.c_char_p
    sg.get_scsi_pt_transport_err_str.argtypes = [ctypes.c_void_p,
                                               ctypes.c_int,
                                               ctypes.c_char_p]
    sg.get_scsi_pt_duration_ms      .restype = ctypes.c_int
    sg.get_scsi_pt_duration_ms      .argtypes = [ctypes.c_void_p]
    sg.destruct_scsi_pt_obj         .restype = ctypes.c_int # void
    sg.destruct_scsi_pt_obj         .argtypes = [ctypes.c_void_p]

    def __init__(self, filename):
        self.file = self.sg.scsi_pt_open_device(filename, 0, 0)
        if self.file < 0:
            raise Exception(self.file)

    def __del__(self):
        retval = self.sg.scsi_pt_close_device(self.file)
        if retval < 0:
            raise Exception(retval)

    def sendcdb(self, cdb):
        return self.sg.do_scsi_pt(cdb.objp, self.file, 20, 1)


class CDB:
    """
    Manage the data structure that holds a passthrough request.
    """
    
    def __init__(self, cdb, rs_size=24):
        # Construct CDB object for a passthrough request.
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
            
    def set_data_out(self, buf):
        self.buf = ctypes.create_string_buffer(str(bytearray(buf)), len(buf))
        retval = ScsiPT.sg.set_scsi_pt_data_out(self.objp, self.buf, len(self.buf))
        if retval < 0:
            raise Exception(retval)

    def set_data_in(self, buflen):
        self.buf = ctypes.create_string_buffer(buflen)
        retval = ScsiPT.sg.set_scsi_pt_data_in(self.objp, self.buf, len(self.buf))
        if retval < 0:
            raise Exception(retval)


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
     "inquiry"        : (0x12, 6, IN, {"evpd":((1,0),1,0), "page_code":(2,8,0), "allocation_length":(3,16,5)}),
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
        opprm.update({(self.abbrevs[k] if k in self.abbrevs else k):v for (k,v) in params.items()})
        self.fill(self.cdb, opdef, opprm)

    def fill(self, cdb, defs, pparms):
        """
        Take field values in parms and insert them into cdb based on the field definitions in defs.
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
            if type(start) == type(0):  # must be either number of list of 2
                start = (start,7)
            startbitnum = start[0]*8 + (7-start[1])  # Number bits l-to-r.
            bitnum = startbitnum + defs[name][1] - 1
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
        asc += i if (chr(32) <= i and i < chr(96)) else '.'
        if (a+1) % 16 == 0:
            print adr, "%-49s" % hxd, asc
        a += 1
    if len(asc) != 0:
        print adr, "%-49s" % hxd, asc 

if __name__ == "__main__":
    print "version:", ScsiPT.sg.scsi_pt_version()
    #pt = ScsiPT("/dev/sdbn")
    pt = ScsiPT("/dev/sdah")

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

