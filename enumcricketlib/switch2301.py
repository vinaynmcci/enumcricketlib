##############################################################################
# 
# Module: switch2301.py
#
# Description:
#     Top level API to manage USB Switch 2301
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

from enumcricketlib import switch 

class Switch2301(switch.Switch):
    def __init__(self, cport):
        switch.Switch.__init__(self, cport, 9600)
    
    def get_volts(self):
        cmd = 'volts\r\n'
        return self.send_cmd(cmd)

    def get_amps(self):
        cmd = 'amps\r\n'
        return self.send_cmd(cmd)