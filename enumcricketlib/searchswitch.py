##############################################################################
# 
# Module: searchswitch.py
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
# Lib imports
import serial
import serial.tools.list_ports
import time

import hid

VID_2101 = 0x040e
PID_2101 = 0xf413


def version():
    return "Cricketlib v1.0.7"

def get_switches():
    devList = search_switches()
    return devList

def get_avail_ports():
    comlist = serial.tools.list_ports.comports()
    port_name = []
    for port, desc, hwid in sorted(comlist):
        port_name.append((hwid, port, desc))
    return port_name

def filter_port():
    usb_hwid_str = ["USB VID:PID=045E:0646", "USB VID:PID=2341:0042"]
    comlist = serial.tools.list_ports.comports()
    port_name = []

    for port, desc, hwid in sorted(comlist):
        res = [True for gnhwid in usb_hwid_str if(gnhwid in hwid)]
        if(res):
            port_name.append(port)
    return port_name

def get_2101():
    """
    get the model2101 enumaration in darwin 
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
            slno = dev['serial_number']
            if(len(slno) >= 12):
                dlist.append(slno)
    return dlist

def check_status(myport):
    myswitch = None
    try:
        ser = serial.Serial(myport, baudrate=115200, 
                            bytesize=serial.EIGHTBITS,
                            parity=serial.PARITY_NONE, timeout=1, 
                            stopbits=serial.STOPBITS_ONE)
        time.sleep(1)

        status_cmd = 'status\r\n'

        ser.write(status_cmd.encode())
        strout = ser.readline().decode('utf-8')
        
        start_time = time.time()
        while (time.time() - start_time) < 2:
            line = ser.readline()
        
        if 'Model 3142' in strout:
            myswitch = '3142'
        elif 'Model 3141' in strout:
            myswitch = '3141'
        ser.close()
        
        return myswitch
    except serial.SerialException as e:
        return myswitch
            

def check_version(myport):
    myswitch = None
    try:
        ser = serial.Serial(myport, baudrate=115200, 
                            bytesize=serial.EIGHTBITS,
                            parity=serial.PARITY_NONE, timeout=1, 
                            stopbits=serial.STOPBITS_ONE)
        time.sleep(1)

        cmd = 'version\r\n'
    
        ser.write(cmd.encode())
        strout = ser.readline().decode('utf-8')
        nstr = strout[2:]
        if(nstr.find('01') != -1):
            myswitch = '3141'
        elif(nstr.find('12') != -1):
            myswitch = '3201'
        ser.close()
        return myswitch
    except serial.SerialException as e:
        return myswitch 
    
    
def check_2301(myport):
    myswitch = None
    try:
        ser = serial.Serial(myport, baudrate=9600, 
                            bytesize=serial.EIGHTBITS,
                            parity=serial.PARITY_NONE, timeout=1, 
                            stopbits=serial.STOPBITS_ONE)
        time.sleep(1)

        cmd = 'version\r\n'
    
        ser.write(cmd.encode())
        strout = ser.readline().decode('utf-8')
        nstr = strout[2:]
        if(nstr.find('08') != -1):
            myswitch = '2301'
        ser.close()
        return myswitch
    except serial.SerialException as e:
        return myswitch  


def search_switches():
    port_name = []
    rev_list = []
    dev_list = []

    # Get list of 3141, 3201, 2301 switches    
    port_name = filter_port()

    for i in range(len(port_name)):
        myswitch = check_status(port_name[i])
        if myswitch != None:
            rev_list.append(port_name[i])
            dev_list.append(myswitch)
            continue
        myswitch = check_version(port_name[i])
        if myswitch != None:
            rev_list.append(port_name[i])
            dev_list.append(myswitch)
            continue
        myswitch = check_2301(port_name[i])
        if myswitch != None:
            rev_list.append(port_name[i])
            dev_list.append(myswitch)
            
            
    # Get the list of 2101
    dlist = get_2101()

    for dl in dlist:
        rev_list.append(dl)
        dev_list.append('2101')
        
    rdict = {}
    devlist = []
    
    for i in range(len(rev_list)):
        tempdict = {}
        tempdict["port"] = rev_list[i]
        tempdict["model"] = dev_list[i]
        devlist.append(tempdict)

    rdict["switches"] = devlist
    
    return rdict