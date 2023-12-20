##############################################################################
# 
# Module: Serialswitch.py
#
# Description:
#     API to show list of available MCCI USB Switch (3141, 3201, 2101 and 2301)
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
import serial
import serial.tools.list_ports

class SerialDev:
    def __init__(self, port, baud):
        self.handler = None
        self.port = port
        self.baud = baud

    def open(self):
        self.handler = serial.Serial()
        self.handler.port = self.port
        self.handler.baudrate = self.baud
        self.handler.bytesize = serial.EIGHTBITS
        self.handler.parity = serial.PARITY_NONE
        self.handler.timeout = 1
        self.handler.stopbits =serial. STOPBITS_ONE
        
        try:
            res = self.handler.open()
            return True
        except serial.SerialException as e:
            return False
            
    def close(self):
        try:
            self.handler.close()
            return True
        except:
            return False

    def write(self, cmd):
        try:
            cnt = self.handler.write(cmd.encode())
            return cnt
        except:
            return -1

    def read(self):
        try:
            return  0, self.handler.readline().decode('utf-8')
        except:
            return -1