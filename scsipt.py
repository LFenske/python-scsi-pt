#!/usr/bin/env python

import ctypes

class scsipt:
    
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
        self.objp = self.sg.construct_scsi_pt_obj()
        if self.objp == None:
            raise Exception()

    def __del__(self):
        if self.objp != None:
            self.sg.destruct_scsi_pt_obj(self.objp)
            self.objp = None
        retval = self.sg.scsi_pt_close_device(self.file)
        if retval < 0:
            raise Exception(retval)

if __name__ == "__main__":
    print "version:", scsipt.sg.scsi_pt_version()
    #pt = scsipt("/dev/sdbn")
    pt = scsipt("/dev/sdah")

    cdb_tur = ctypes.create_string_buffer(str(bytearray([0,0,0,0,0,0])),6)
    print "cdb_tur =", cdb_tur, "type =", type(cdb_tur), "len =", len(cdb_tur)
    scsipt.sg.set_scsi_pt_cdb(pt.objp, cdb_tur, len(cdb_tur))

    sense = ctypes.create_string_buffer(255)
    print "sense =", sense, "type =", type(sense), "len =", len(sense)
    scsipt.sg.set_scsi_pt_sense(pt.objp, sense, len(sense))

    print "objp =", pt.objp
    print "file =", pt.file
    retval = scsipt.sg.do_scsi_pt(pt.objp, pt.file, 20, 1)
    print "retval =", retval

    for i in range(10):
        print i, ord(sense.raw[i])

    del pt

