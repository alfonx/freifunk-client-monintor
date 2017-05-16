#!/usr/bin/env python
from subprocess import call
from subprocess import check_output
import re
from datetime import date
from datetime import datetime
import time

from time import sleep

# Networkmanager muss aus

SSID = "Freifunk"


def writeCSVLine(logstring):
    text_file = open(SSID + ".log", "a")
    text_file.write(logstring)    
    text_file.close()
    pass


if __name__ == '__main__':
        # TODO wait
    logstring = str(datetime.now()) + ';'
    
    
    call(["ip","addr","flush","dev","wlan0"])

    call(["rfkill", "block", "wlan"])
    
    sleep(5)
    
    call(["rfkill", "unblock", "wlan"])
    
    scanres = check_output(['iwlist', 'wlan0', 'scan'])
    m = re.search(SSID, scanres)
    #print scanres
    if not m:
        logstring = logstring + 'FF SSID ist nicht sichtbar;';
        writeCSVLine(logstring)
        exit
        
    logstring = logstring + 'FF SSID ist sichtbar;'
    print 'SSID ' + SSID + ' ist sichtbar;'
    print logstring
    
    print 'Verbinde mit ' + SSID + '.. '
    connectwlan_output = check_output(['iwconfig', 'wlan0','essid', SSID])
    
    starttime = time.time()
    connectwlan_output = check_output(['dhclient', 'wlan0'])
    dhcpduration = time.time()-starttime
    logstring += str(dhcpduration)+';'

    print "sleep 20s nach dhclient weil IP6 laenger dauern kann..."    
    sleep(20)
    
    
    ifconfig_output = check_output(['ifconfig', 'wlan0'])
    m = re.search('.*wlan.*inet (?:Adresse|inet addr):(.*?) .*$',ifconfig_output,flags=re.MULTILINE+re.DOTALL)
    if m:
        print 'IPv4 = '+m.group(1)
        logstring += m.group(1) + ';'
    else:
        logstring += ';'
    m = re.search('.*wlan.*?(?:inet6-Adresse|inet6 addr): (fd21:b4dc:4b.*?)/.*$',ifconfig_output,flags=re.MULTILINE+re.DOTALL)
    if m:
        print 'IPv6 = '+m.group(1)
        logstring += m.group(1) + ';'
    else:
        logstring += ';'
        
    print logstring
    writeCSVLine(logstring)
    
    #call(["rfkill", "block", "wlan"])
    
