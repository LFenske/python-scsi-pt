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

class ScsiPT(object):
    """
    static linkages to sgutils functions
    """

    sg = ctypes.CDLL("libsgutils2.so.2")

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
        super(ScsiPT, self).__init__()
        self.file = self.sg.scsi_pt_open_device(filename, 0, 0)
        if self.file < 0:
            raise Exception(self.file)

    def __del__(self):
        retval = self.sg.scsi_pt_close_device(self.file)
        if retval < 0:
            raise Exception(retval)
        #super(ScsiPT, self).__del__()

    def sendcdb(self, cdb):
        return self.sg.do_scsi_pt(cdb.objp, self.file, 20, 1)


