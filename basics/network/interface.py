#!/usr/bin/env python
#############################################
# Provides interface status of each switch
# provided using nmap's format e.g. 10.0.0.1-9
#############################################

import pexpect, getpass

def addressRange():
    # Give an IP range using the nmap syntax 10.0.0.1-10
    iprange = raw_input('Input IP range: ')
    # this is a request for the user to type in an IP range
    lastdot = iprange.rfind('.')
    rangecheck = iprange.rfind('-')
    addressprefix = iprange[ : lastdot + 1] #10.0.0.

    if rangecheck == -1:
        rangestart = iprange[lastdot + 1 : ] # 1
        rangeend = rangestart
        ipcrawl = [addressprefix, rangestart, rangeend]
    else:
        rangestart = iprange[lastdot + 1 : rangecheck]
        rangeend = iprange[rangecheck + 1 :]
        ipcrawl = [addressprefix, rangestart, rangeend]
    return ipcrawl

def brocade(host, password):
    # This function checks the state of all interfaces on a Brocade switch
    
    session = pexpect.spawn('ssh admin@' + host)
    session.expect('assword:')
    session.sendline(password)
    session.expect('>')
    # expect the symbol before the cursor to be >
    session.sendline('show int br')
    session.expect('-c') # expect space required
    thing = session.before.split('\n') # Split the returned string by line
    for line in thing: # for loop to filter out junk lines
        if not("--More--" in line) and not("show int br" in line):
            print line
    session.sendline(' ') # send space to retrieve all ports
    session.expect('>')
    print session.before
    return

def toughswitch(host, password):
    # Checks the state of all interfaces on a Toughswitch
    session = pexpect.spawn('ssh admin@' + host)
    session.expect('assword: ')
    session.sendline(password)
    session.expect('# ')
    session.sendline('cat /usr/www/stats')
    session.expect('# ')
    print session.before
    return


def main():
    try:
        ipcrawl = addressRange() # provides the ip range as a list to crawl through
        password = getpass.getpass('Password: ') # password of the hosts
        for ip in range(int(ipcrawl[1]), int(ipcrawl[2]) + 1):
            host = ipcrawl[0] + str(ip) 
            brocade(host, password) # login for brocade switch
    except KeyboardInterrupt:
        print "\nProgram stopped by user."

    return

if __name__ == '__main__':
    main()
