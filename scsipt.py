#!/usr/bin/env python

import ctypes

class scsipt:
    
    def __init__(self):
        self.sg = ctypes.CDLL("libsgutils2.so")
        self.sg.scsi_pt_version              .restype = ctypes.c_char_p
        self.sg.scsi_pt_version              .argtypes = []
        self.sg.scsi_pt_open_device          .restype = ctypes.c_int
        self.sg.scsi_pt_open_device          .argtypes = [ctypes.c_char_p,
                                                          ctypes.c_int,
                                                          ctypes.c_int]
        self.sg.scsi_pt_open_flags           .restype = ctypes.c_int
        self.sg.scsi_pt_open_flags           .argtypes = [ctypes.c_char_p,
                                                          ctypes.c_int,
                                                          ctypes.c_int]
        self.sg.scsi_pt_close_device         .restype = ctypes.c_int
        self.sg.scsi_pt_close_device         .argtypes = [ctypes.c_int]
        self.sg.construct_scsi_pt_obj        .restype = ctypes.c_void_p
        self.sg.construct_scsi_pt_obj        .argtypes = []
        self.sg.clear_scsi_pt_obj            .restype = ctypes.c_int # void
        self.sg.clear_scsi_pt_obj            .argtypes = [ctypes.c_void_p]
        self.sg.set_scsi_pt_cdb              .restype = ctypes.c_int # void
        self.sg.set_scsi_pt_cdb              .argtypes = [ctypes.c_void_p,
                                                          ctypes.c_char_p,
                                                          ctypes.c_int]
        self.sg.set_scsi_pt_sense            .restype = ctypes.c_int # void
        self.sg.set_scsi_pt_sense            .argtypes = [ctypes.c_void_p,
                                                          ctypes.c_char_p,
                                                          ctypes.c_int]
        self.sg.set_scsi_pt_data_in          .restype = ctypes.c_int # void
        self.sg.set_scsi_pt_data_in          .argtypes = [ctypes.c_void_p,
                                                          ctypes.c_char_p,
                                                          ctypes.c_int]
        self.sg.set_scsi_pt_data_out         .restype = ctypes.c_int # void
        self.sg.set_scsi_pt_data_out         .argtypes = [ctypes.c_void_p,
                                                          ctypes.c_char_p,
                                                          ctypes.c_int]
        self.sg.set_scsi_pt_packet_id        .restype = ctypes.c_int # void
        self.sg.set_scsi_pt_packet_id        .argtypes = [ctypes.c_void_p,
                                                          ctypes.c_int]
        self.sg.set_scsi_pt_tag              .restype = ctypes.c_int # void
        self.sg.set_scsi_pt_tag              .argtypes = [ctypes.c_void_p,
                                                          ctypes.c_ulong]
        self.sg.set_scsi_pt_task_management  .restype = ctypes.c_int # void
        self.sg.set_scsi_pt_task_management  .argtypes = [ctypes.c_void_p,
                                                          ctypes.c_int]
        self.sg.set_scsi_pt_task_attr        .restype = ctypes.c_int # void
        self.sg.set_scsi_pt_task_attr        .argtypes = [ctypes.c_void_p,
                                                          ctypes.c_int,
                                                          ctypes.c_int]
        self.sg.set_scsi_pt_flags            .restype = ctypes.c_int # void
        self.sg.set_scsi_pt_flags            .argtypes = [ctypes.c_void_p,
                                                          ctypes.c_int]
        self.sg.do_scsi_pt                   .restype = ctypes.c_int
        self.sg.do_scsi_pt                   .argtypes = [ctypes.c_void_p,
                                                          ctypes.c_int,
                                                          ctypes.c_int,
                                                          ctypes.c_int]
        self.sg.get_scsi_pt_result_category  .restype = ctypes.c_int
        self.sg.get_scsi_pt_result_category  .argtypes = [ctypes.c_void_p]
        self.sg.get_scsi_pt_resid            .restype = ctypes.c_int
        self.sg.get_scsi_pt_resid            .argtypes = [ctypes.c_void_p]
        self.sg.get_scsi_pt_status_response  .restype = ctypes.c_int
        self.sg.get_scsi_pt_status_response  .argtypes = [ctypes.c_void_p]
        self.sg.get_scsi_pt_sense_len        .restype = ctypes.c_int
        self.sg.get_scsi_pt_sense_len        .argtypes = [ctypes.c_void_p]
        self.sg.get_scsi_pt_os_err           .restype = ctypes.c_int
        self.sg.get_scsi_pt_os_err           .argtypes = [ctypes.c_void_p]
        self.sg.get_scsi_pt_os_err_str       .restype = ctypes.c_char_p
        self.sg.get_scsi_pt_os_err_str       .argtypes = [ctypes.c_void_p,
                                                          ctypes.c_int,
                                                          ctypes.c_char_p]
        self.sg.get_scsi_pt_transport_err    .restype = ctypes.c_int
        self.sg.get_scsi_pt_transport_err    .argtypes = [ctypes.c_void_p]
        self.sg.get_scsi_pt_transport_err_str.restype = ctypes.c_char_p
        self.sg.get_scsi_pt_transport_err_str.argtypes = [ctypes.c_void_p,
                                                          ctypes.c_int,
                                                          ctypes.c_char_p]
        self.sg.get_scsi_pt_duration_ms      .restype = ctypes.c_int
        self.sg.get_scsi_pt_duration_ms      .argtypes = [ctypes.c_void_p]
        self.sg.destruct_scsi_pt_obj         .restype = ctypes.c_int # void
        self.sg.destruct_scsi_pt_obj         .argtypes = [ctypes.c_void_p]
        
if __name__ == "__main__":
    pt = scsipt()
    print "version:", pt.sg.scsi_pt_version()
       
