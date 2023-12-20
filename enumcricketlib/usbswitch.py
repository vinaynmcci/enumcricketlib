##############################################################################
# 
# Module: usbswitch.py
#
# Description:
#     API to manage USB Switch 2101
#
# Copyright notice:
#     This file copyright (c) 2022 by
#
#         MCCI Corporation
#         3520 Krums Corners Road
#         Ithaca, NY  14850
#
#     Released under the MCCI Corporation.
#
# Author:
#     Seenivasan V, MCCI Corporation Dec 2022
#
# Revision history:
#    V1.0.6 Thu May 2023 12:05:00   Seenivasan V
#       Module created
##############################################################################

import hid

VID_2101 = 0x040e
PID_2101 = 0xf413

class UsbSwitch:
    def __init__(self, slno):
        self.slno_list = []
        self.path_list = []
        self.dev_list = []
        self.slno = slno
        self.path = None
        self.dev = None
        self.ready = False

    def get_2101(self):
        """   get the model2101 enumaration in darwin 
        Args:
            self: The self parameter is a reference to the current 
            instance of the class,and is used to access variables
            that belongs to the class.
        Returns: 
            dlist: return same device model
        """
        dlist = []
        dev = hid.enumerate(VID_2101, PID_2101)
        if len(dev) != 0:
            for dev in hid.enumerate(VID_2101, PID_2101):
                dlist.append(dev['serial_number'])

        return dlist

    def scan_2101(self):
        """
        scanning the device model 2101 device

        Args:
            self: The self parameter is a reference to the current 
            instance of the class,and is used to access variables
            that belongs to the class.
        Returns:
            None
        """
        dlist = []
        self.slno_list.clear()
        
        self.path_list.clear()
    
        dev = hid.enumerate(VID_2101, PID_2101)
        if len(dev) != 0:
            for dev in hid.enumerate(VID_2101, PID_2101):
                try:
                    dlist.append(dev['serial_number'])
                    self.slno_list.append(dev['serial_number'])
                    self.path_list.append(dev['path'])
                except:
                    print("Path Error")
        
        self.ready = True
        return dlist

    def select_usb_switch(self, serialno):
        """
        select usb device model 2101 in darwin and windows with serail number
        Args:
            self: The self parameter is a reference to the current 
            instance of the class,and is used to access variables
            that belongs to the class.
            parent: Pointer to a parent window.
            top: creates an object
        Returns:
            True: serial is True
        """
        self.slno = None
        self.path = None
        
        for i in range(len(self.slno_list)):
            if(self.slno_list[i] == serialno):
                self.slno = serialno
                self.path = self.path_list[i]
                break
            
        if self.slno == serialno:
            return True
        else:
            return 
    
    def read_status(self):
        """
        Read the port status in windows, Linux
        Args:
            self: The self parameter is a reference to the current 
            instance of the class,and is used to access variables
            that belongs to the class.
            cmd:device write  command sending to port
        Returns:
            result: is succes return ro control trasfer
        """
        result = None
        res = -1

        dev = hid.device()
        dev.open_path(self.path)
        result = dev.get_input_report(0x00, 0x03)
        dev.close()
        res = 0
        
        return res, result

    def control_port(self, cmd):
        """
        contrlling the ports in windows, Linux, darwin
        Args:
            self: The self parameter is a reference to the current 
            instance of the class,and is used to access variables
            that belongs to the class.
            cmd:device write  command sending to port
        Returns:
            result: is succes return ro control trasfer
        """
        result = None
        res = -1

        dev = hid.device()
        dev.open_path(self.path)
        result = dev.write([0x00, cmd])
        dev.close()
        res = 0
    
        return res, result