#!/usr/bin/env python
# Brocade upgrader
# Run with the firmware for both the switch and the  in the local directory
import pexpect, time, getpass, os, csv, mechanize
desktop=os.path.join(os.path.join(os.path.expanduser('~')), "Desktop")
ssh=os.getenv("HOME")
os.chdir(""+desktop)

def check_ping():
	hostname = "1.1.1.1"
	response = os.system("ping -c 1 " + hostname)
	# and then check the response...
	if response == 0:
		pingstatus = "Network Active"
		br = mechanize.Browser()
		br.open("https://192.168.1.253")
		br.select_form(nr=0)
		br.form['name'] = 'Enter your Name'
		br.form['title'] = 'Enter your Title'
		br.form['message'] = 'Enter your message'
		req = br.submit()
		
		print pingstatus
	else:
		pingstatus = "Network Error"

	return pingstatus

def sysuptime(host, password):
	# copy the firmware over and then reboots the switch.
	#pexpect.timeout=10
	session = pexpect.spawn('ssh admin@' + host)
	login = session.expect(['assword:', pexpect.TIMEOUT, pexpect.EOF], timeout=10)
	if login == 0:
		session.sendline(password)
		login2 = session.expect(['>', pexpect.TIMEOUT, pexpect.EOF], timeout=10)
		if login2 == 0:
			print "login success"
			session.sendline('show ver')
			time.sleep(3)
			session.sendline(' ')
			session.expect('>')
			response=session.before
			for line in response.split('\n'):
				if 'uptime' in line:
					start = line.find('is') +3
					end = line.rfind('(s)') +3
					a = line[start : end]
					print ('\nThe Switch IP '+host+' has '+a+' uptime')

			session.close()
			return
		elif login2 == 1:
			print "\nThe device IP "+host+ " is not a brocade SW"
			print session.before
		elif login2 == 2:
			print "\nThe device IP "+host+ " is not a brocade SW"
			print session.before
	elif login == 1:
		print "\nThe switch IP "+host+" is unreachable"
		print session.before
	elif login == 2:
		print "\nThe switch IP "+host+" is unreachable"
		print session.before
	return


def renameSws(host,password):   #with this funcion you can rename the switches that you are provisioning. it checks the mac address in the ruckus.csv file 
	session = pexpect.spawn('ssh admin@' + host)
	login = session.expect(['assword:', pexpect.TIMEOUT, pexpect.EOF], timeout=10)
	print session.before
	if login == 0:
		session.sendline(password)
		login2 = session.expect(['>', pexpect.TIMEOUT, pexpect.EOF], timeout=10)
		if login2 == 0:
			print "login success"
			session.sendline('en')
			session.expect(['#',pexpect.EOF])
			session.sendline('show int br')
			#if switch == "brocade24":
			 #   session.expect('-c') # expect space required
			  #  thing = session.before.split('\n') # Split the returned string by line
			   # for line in thing: # for loop to filter out junk lines
				#    if not("--More--" in line) and not("show int br" in line):
				 #       return
			session.sendline(' ') # send space to retrieve all ports
			session.sendline(' ')
			session.sendline(' ')
			session.expect(['#',pexpect.EOF])
			response = session.before
			#print response
			for line in response.split('\n'):
				if '1/1/1' in line:
					start = line.find('0') +4
					end = line.rfind(' ')
					a = line[start : end]
					b=a.upper()
					delimiter="."
					m = b.replace(delimiter,"")
					version= ":".join(["%s%s" % (m[i], m[i+1]) for i in range(0,12,2)])  
					print version
					with open('ruckus.csv','r') as f:
						reader = csv.reader(f)
						your_list = list(reader)
						threads = []
						for row in your_list:
							#print 'ciao'
							#print row[1]
							if row[1] in version:
								a=row[0]
								print a
								session.sendline('config t')
								session.expect('#')
								session.sendline('hostname '+a)
								session.expect(['#'])
								session.sendline('write me')
								session.expect('#')
								print session.before
								return
							
						#response = session.patch(url, json={"name":row[0]}, verify=False)
						#print response.text

					if 'T213' in version :
						print "\nThe Switch IP "+host+" is running with a Router FW version "+version
					if 'T211' in version :
						print "\nThe Switch IP "+host+" has "+version+" FW version"
					return
	else:
		print 'The Switch is not reachable'

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

def upgrade(host, password):
	# This function checks the state of all interfaces on a Brocade switch
	session = pexpect.spawn('scp SPS08030k.bin admin@' + host + ':flash:primary')
	print "Succeeded in starting SCP of switch firmware"
	session.expect('assword:')
	session.sendline(password)
	print "SCP in progress, this can take up to 5 minutes before timing out."
	session.expect('closed by remote host.',timeout=3000)
	session = pexpect.spawn('scp SPR08030k.bin admin@' + host + ':flash:secondary')
	print "Succeeded in starting SCP of router firmware"
	session.expect('assword:')
	session.sendline(password)
	print "SCP in progress, this can take up to 5 minutes before timing out."
	session.expect('closed by remote host.',timeout=3000)
	session.close()
	print "Upload of firmware successful"
	return

def brocade(host, password, switch):

	# This function checks the state of all interfaces on a Brocade switch

	

	session = pexpect.spawn('ssh admin@' + host)

	session.expect('assword:')

	session.sendline(password)

	session.expect('>')

	# expect the symbol before the cursor to be >

	session.sendline('show int br')

	if switch == "brocade24":

		session.expect('-c') # expect space required

		thing = session.before.split('\n') # Split the returned string by line

		for line in thing: # for loop to filter out junk lines

			if not("--More--" in line) and not("show int br" in line):

				print line

		session.sendline(' ') # send space to retrieve all ports

		session.expect('>')

		print session.before

	elif switch == "brocade12":

		session.expect('>')

		thing = session.before.split('\n') # Split the returned string by line

		for line in thing: # for loop to filter out junk lines

			if not("--More--" in line) and not("show int br" in line):

				print line

	elif switch == "brocade48":

		session.expect('-c') # expect space required

		thing = session.before.split('\n') # Split the returned string by line

		for line in thing: # for loop to filter out junk lines

			if not("--More--" in line) and not("show int br" in line):

				print line

		session.sendline(' ') # send space to retrieve all ports
		session.sendline(' ')

		session.expect('>')

		print session.before

	return



def determineswitch(host, password):

	# Determines the model of the switch

	session = pexpect.spawn('ssh admin@' + host)

	session.expect('assword:')

	session.sendline(password)

	session.expect('>')

	# expect the symbol before the cursor to be >

	session.sendline('show version')

	session.expect(['-c', '>'])

	if "ICX7150-C12" in session.before:

		switch = "brocade12"

	elif "ICX7150-24" in session.before:

		switch = "brocade24" 

	elif "ICX7250-24" in session.before:

		switch = "brocade24"

	elif "ICX7150-48" in session.before:

		switch = "brocade48"
	
	elif "ICX7450-48" in session.before:
		switch = "brocade48"


	return switch


def determineswitchprov(host):

	# Determines the model of the switch

	session = pexpect.spawn('telnet ' + host)

	#session.expect('assword:')

	#session.sendline(password)

	login = session.expect(['>', pexpect.TIMEOUT, pexpect.EOF], timeout=10)
	if login == 0:
		print "login success"

	# expect the symbol before the cursor to be >

		session.sendline('show version')

		session.expect(['-c', '>'])

		if "ICX7150-C12" in session.before:

			switch = "brocade12"

		elif "ICX7150-24" in session.before:

			switch = "brocade7150_24" 

		elif "ICX7250-24" in session.before:

			switch = "brocade7250_24"

		elif "ICX7150-48" in session.before:

			switch = "brocade48"



	return switch

def brocadeprov7150_12(host):
	# copy the firmware over and then reboots the switch.
	#pexpect.timeout=10
	a='''vlan 98 name freewifi by port\n
tagged ethe 1/1/1 to 1/1/12 ethe 1/2/1 to 1/2/2 ethe 1/3/1 to 1/3/2\n
!\n
ip dhcp-client enable\n
vlan 99 name customers by port\n
tagged ethe 1/1/1 to 1/1/12 ethe 1/2/1 to 1/2/2 ethe 1/3/1 to 1/3/2\n
!\n
interface ethernet 1/1/1 to 1/1/12\n
dual-mode\n
!\n
interface ethe 1/2/1 to 1/2/2\n
dual-mode\n
!\n
interface ethe 1/3/1 to 1/3/2\n
dual-mode\n
!\n
interface ethe 1/1/1 to 1/1/12\n
inline p power-limit 15100\n
!\n
exit\n
ntp\n 
Server 163.172.28.46\n
exit\n
snmp-server view CommunityView 1.3.6.1.4.1.1991 included\n
snmp-server view CommunityView mib-2  included\n
snmp-server community 14kingston ro view CommunityView\n
!\n
lldp run\n
!\n
ip ssh key-exchange-method dh-group1-sha1\n
crypto key gen rsa\n
user admin privilege 0 pass 0p3n1!nk\n
aaa authentication login default local\n
enable aaa console\n
no span\n
!\n
write me\n 
write me
	   '''
	session = pexpect.spawn('telnet ' + host)
	login = session.expect(['>', pexpect.TIMEOUT, pexpect.EOF], timeout=10)
	if login == 0:
		print "login success"
		session.sendline('en')
		session.expect('#') 
		print "enabled success"
		session.sendline('config t')
		session.expect('#')
		#session.sendline('hostname '+sitecode+'_WAN_SW')
		#session.expect('#')
		session.sendline(a)
		session.sendline('user admin privilege 0 pass 0p3n1!nk')
		session.expect('#')
		#session.sendline('no ip address '+host+'/24')
		#session.sendline('ip default-gateway '+ipgw)
		session.expect('#')
		session.sendline('write me')
		session.expect('#')
		
		#session.sendline('reload after 00:00:01')
		session.expect('#')
		session.sendline('no telnet server')
		#session.sendline('ip address '+ipaddr)
		session.sendline('write me')
		time.sleep(3)
		session.close()
		return
	elif login == 1:
		print "\nThe switch IP "+host+" is unreachable"
		print session.before
	elif login == 2:
		print "\nThe switch IP "+host+" is unreachable"
		print session.before
	return


def brocadeprov7150_24(host):
	# copy the firmware over and then reboots the switch.
	#pexpect.timeout=10
	a='''vlan 98 name freewifi by port\n
tagged ethe 1/1/1 to 1/1/24 ethe 1/2/1 to 1/2/2 ethe 1/3/1 to 1/3/4\n
!\n
vlan 99 name customers by port\n
tagged ethe 1/1/1 to 1/1/24 ethe 1/2/1 to 1/2/2 ethe 1/3/1 to 1/3/4\n
!\n
ip dhcp-client enable\n
interface ethernet 1/1/1 to 1/1/12\n
dual-mode\n
!\n
interface ethe 1/2/1 to 1/2/2\n
dual-mode\n
!\n
interface ethe 1/3/1 to 1/3/4\n
dual-mode\n
!\n
interface ethe 1/1/1 to 1/1/24\n
inline p power-limit 15100\n
!\n
exit\n
ntp\n 
Server 163.172.28.46\n
exit\n
snmp-server view CommunityView 1.3.6.1.4.1.1991 included\n
snmp-server view CommunityView mib-2  included\n
snmp-server community 14kingston ro view CommunityView\n
!\n
lldp run\n
!\n
ip ssh key-exchange-method dh-group1-sha1\n
crypto key gen rsa\n
user admin privilege 0 pass 0p3n1!nk\n
aaa authentication login default local\n
enable aaa console\n
no span\n
!\n
write me\n 
write me
	   '''
	session = pexpect.spawn('telnet ' + host)
	login = session.expect(['>', pexpect.TIMEOUT, pexpect.EOF], timeout=10)
	if login == 0:
		print "login success"
		session.sendline('en')
		session.expect('#') 
		print "enabled success"
		session.sendline('config t')
		session.expect('#')
		#session.sendline('hostname '+sitecode+'_WAN_SW')
		#session.expect('#')
		session.sendline(a)
		session.sendline('user admin privilege 0 pass 0p3n1!nk')
		session.expect('#')
		#session.sendline('no ip address '+host+'/24')
		#session.sendline('ip default-gateway '+ipgw)
		session.expect('#')
		session.sendline('write me')
		session.expect('#')
		#session.sendline('reload after 00:00:01')
		session.expect('#')
		session.sendline('no telnet server')
		#session.sendline('ip address '+ipaddr)
		session.sendline('write me')
		time.sleep(3)
		session.close()
		return
	elif login == 1:
		print "The switch IP "+host+" is unreachable"
		print session.before
	elif login == 2:
		print "The switch IP "+host+" is unreachable"
		print session.before
	return

def brocadeprov7250_24(host):
	# copy the firmware over and then reboots the switch.
	#pexpect.timeout=10
	a='''vlan 98 name freewifi by port\n
tagged ethe 1/1/1 to 1/1/24 ethe 1/2/1 to 1/2/8\n
!\n
vlan 99 name Customers by port\n
tagged ethe 1/1/1 to 1/1/24 ethe 1/2/1 to 1/2/8\n
!\n
ip dhcp-client enable\n
interface ethernet 1/1/1 to 1/1/24\n
dual-mode\n
!\n
interface ethe 1/2/1 to 1/2/8\n
dual-mode\n
interface ethe 1/1/1 to 1/1/24\n
inline p power-limit 15100\n
!\n
exit\n
ntp\n 
Server 163.172.28.46\n
exit\n
snmp-server view CommunityView 1.3.6.1.4.1.1991 included\n
snmp-server view CommunityView mib-2  included\n
snmp-server community 14kingston ro view CommunityView\n
!\n
lldp run\n
!\n
ip ssh key-exchange-method dh-group1-sha1\n
crypto key gen rsa\n
user admin privilege 0 pass 0p3n1!nk\n
aaa authentication login default local\n
enable aaa console\n
no span\n
!\n
write me\n 
write me
	   '''
	session = pexpect.spawn('telnet ' + host)
	login = session.expect(['>', pexpect.TIMEOUT, pexpect.EOF], timeout=10)
	if login == 0:
		print "login success"
		session.sendline('en')
		session.expect('#') 
		print "enabled success"
		session.sendline('config t')
		session.expect('#')
		#session.sendline('hostname '+sitecode+'_WAN_SW')
		#session.expect('#')
		session.sendline(a)
		session.sendline('user admin privilege 0 pass 0p3n1!nk')
		session.expect('#')
		#session.sendline('no ip address '+host+'/24')
		#session.sendline('ip default-gateway '+ipgw)
		session.expect('#')
			#print "enabled success"
		session.sendline('write me')
		session.expect('#')
		#session.sendline('reload after 00:00:01')
		session.expect('#')
		session.sendline('no telnet server')
		#session.sendline('ip address '+ipaddr)
		session.sendline('write me')
		time.sleep(3)
		print ('\n Configuration completed'+host)
		session.close()
		return
	elif login == 1:
		print "\nThe switch IP "+host+" is unreachable"
		print session.before
	elif login == 2:
		print "\nThe switch IP "+host+" is unreachable"
		print session.before
	return


def ruckusvlan1000(host,sitecode,ipaddr,ipgw):
	# copy the firmware over and then reboots the switch.
	#pexpect.timeout=10
	a='''vlan 1000 by port\n
tagged ethe 1/1/1 to 1/1/12 ethe 1/2/1 to 1/2/2 ethe 1/3/1 to 1/3/2\n
!\n
interface ethernet 1/1/1 to 1/1/12\n
dual-mode\n
!\n
interface ethe 1/2/1 to 1/2/2\n
dual-mode\n
!\n
interface ethe 1/3/1 to 1/3/2\n
dual-mode\n
!\n
exit\n
ntp\n 
Server 163.172.28.46\n
exit\n
snmp-server view CommunityView 1.3.6.1.4.1.1991 included\n
snmp-server view CommunityView mib-2  included\n
snmp-server community 14kingston ro view CommunityView\n
!\n
lldp run\n
!\n
ip ssh key-exchange-method dh-group1-sha1\n
crypto key gen rsa\n
user admin privilege 0 pass 0p3n1!nk\n
aaa authentication login default local\n
enable aaa console\n
no span\n
!\n
write me\n 
write me
	   '''
	session = pexpect.spawn('telnet ' + host)
	login = session.expect(['>', pexpect.TIMEOUT, pexpect.EOF], timeout=10)
	if login == 0:
		print "login success"
		session.sendline('en')
		session.expect('#') 
		print "enabled success"
		session.sendline('config t')
		session.expect('#')
		session.sendline('hostname '+sitecode+'_WAN_SW')
		session.expect('#')
		session.sendline(a)
		session.sendline('user admin privilege 0 pass 0p3n1!nk')
		session.expect('#')
		session.sendline('ip default-gateway '+ipgw)
		session.expect('#')
		session.sendline('ip address '+ipaddr)
		session.sendline('write me')
		session.sendline('no telnet server')
		time.sleep(3)
		print '\nConfiguration completed'
		session.close()
		return
	elif login == 1:
		print "\nThe switch IP "+host+" is unreachable"
		print session.before
	elif login == 2:
		print "\nThe switch IP "+host+" is unreachable"
		print session.before
	return

				   
def copyandreboot(host, password, vmware, fwversion):
	# copy the firmware over and then reboots the switch.
	#pexpect.timeout=10
	session = pexpect.spawn('ssh admin@' + host)
	login = session.expect(['assword:', pexpect.TIMEOUT, pexpect.EOF], timeout=10)
	if login == 0:
		session.sendline(password)
		login2 = session.expect(['>', pexpect.TIMEOUT, pexpect.EOF], timeout=10)
		if login2 == 0:
			print "login success"
			session.sendline('en')
			session.expect('#') 
			print "\nenabled success"
			session.sendline('copy tftp system-manifest ' + vmware + ' ' +fwversion+'_Manifest.txt all-images-primary')
			#print "copy tftp.. " 
			session.expect(': ')
			#print session.before
			time.sleep(3) 
			session.send('y')
			#print "copy tftp2.. "
			session.expect('MANIFEST FILE', timeout=300)
			print session.before
			print "\nwriting memory\n"
			session.close()
			return
		elif login2 == 1:
			print "\nThe device IP "+host+ " is not a brocade SW"
			print session.before
		elif login2 == 2:
			print "\nThe device IP "+host+ " is not a brocade SW"
			print session.before
	elif login == 1:
		print "\nThe switch IP "+host+" is unreachable"
		print session.before
	elif login == 2:
		print "\nThe switch IP "+host+" is unreachable"
		print session.before
	return

def copyandrebootsecondary(host, password, vmware, fwversion):
	# copy the firmware over and then reboots the switch.
	#pexpect.timeout=10
	session = pexpect.spawn('ssh admin@' + host)
	login = session.expect(['assword:', pexpect.TIMEOUT, pexpect.EOF], timeout=10)
	if login == 0:
		session.sendline(password)
		login2 = session.expect(['>', pexpect.TIMEOUT, pexpect.EOF], timeout=10)
		if login2 == 0:
			print "\nlogin success"
			session.sendline('en')
			session.expect('#') 
			print "\nenabled success"
			session.sendline('copy tftp system-manifest ' + vmware + ' ' +fwversion+'_Manifest.txt all-images-secondary')
			#print "copy tftp.. " 
			session.expect(': ')
			#print session.before
			time.sleep(3) 
			session.send('y')
			#print "copy tftp2.. "
			session.expect('MANIFEST FILE', timeout=300)
			print session.before
			print "\nwriting memory\n "
			session.close()
			return
		elif login2 == 1:
			print "\nThe device IP "+host+ " is not a brocade SW"
			print session.before
		elif login2 == 2:
			print "\nThe device IP "+host+ " is not a brocade SW"
			print session.before
	elif login == 1:
		print "\nThe switch IP "+host+" is unreachable"
		print session.before
	elif login == 2:
		print "\nThe switch IP "+host+" is unreachable"
		print session.before
	return

def firmwarerepair(host, password, boot):
	# copy the firmware over and then reboots the switch.
	#pexpect.timeout=10
	session = pexpect.spawn('scp '+desktop+'/SPS08070a.bin admin@'+host+':flash:'+boot)
	login = session.expect(['assword:', pexpect.TIMEOUT, pexpect.EOF])
	if login == 0:
		session.sendline(password)
		#print session.before
		login2 = session.expect(['.bin',pexpect.TIMEOUT, pexpect.EOF], timeout=10)
		if login2 == 0:
			print "\nThe switch "+host+" is uploading the new firmware"
			#print session.before
			#time.sleep(240)
			session.expect(['remote',pexpect.TIMEOUT, pexpect.EOF], timeout=500)
			print'\nDownload firmware completed'
			print session.before
			return
		elif login2 == 1:
			print "\nThe IP " +host+ " firmware upgrade was not possible"
			print session.before
		elif login == 2:
			print "\nThe IP " +host+ " firmware upgrade was not possible "
			print session.before
	elif login == 1:
		print "\nThe switch IP "+host+" is unreachable"
		print session.before
	elif login == 2:
		print "\nThe switch IP "+host+" is unreachable"
		print session.before
	return

def reboot(host, password):
	# copy the firmware over and then reboots the switch.
	#pexpect.timeout=10
	session = pexpect.spawn('ssh admin@' + host)
	login = session.expect(['assword:', pexpect.TIMEOUT, pexpect.EOF])
	if login == 0:
		session.sendline(password)
		login2 = session.expect(['>',pexpect.TIMEOUT, pexpect.EOF], timeout=10)
		if login2 == 0:
			#print "login success"
			session.sendline('en')
			session.expect('#') 
			#print "enabled success"
			session.sendline('write me')
			session.expect('#')
			session.sendline('reload after 00:00:05')
			session.expect('#')
			#print "copy tftp.. " 
			#session.expect(': ')
			print session.before
			time.sleep(3) 
			session.send('y')
			config = session.expect(['Running',pexpect.TIMEOUT, pexpect.EOF,'Error'], timeout=10)
			if config == 0:
				print "The Switch IP " +host+ " Switch configuration saved. Reboot "
				session.send('y')
			elif config == 1:
				print "The Switch IP " +host+ " will be rebooted in 5 minutes"
			elif config == 2:
				print "The Switch IP " +host+ " will be rebooted in 5 minutes"
			elif config == 3:
				print "The Switch IP " +host+ " An Error as occurred, the switch will not be rebooted"
			session.close()
			return
		elif login2 == 1:
			print "The IP " +host+ " reboot was not possible is not a Brocade SW"
			print session.before
		elif login == 2:
			print "The IP " +host+ " reboot was not possible "
			print session.before
	elif login == 1:
		print "The switch IP "+host+" is unreachable"
		print session.before
	elif login == 2:
		print "The switch IP "+host+" is unreachable"
		print session.before
	return

def fwverify(host, password):
	# copy the firmware over and then reboots the switch.
	#pexpect.TIMEOUT='10'
	session = pexpect.spawn('ssh admin@' + host)
	login = session.expect(['assword:',pexpect.EOF, pexpect.TIMEOUT], timeout=10)
	if login == 0:
		session.sendline(password)
		access = session.expect(['>', pexpect.EOF, pexpect.TIMEOUT],timeout=10)
		if access == 0: 
			print "login success "
			session.sendline('show flash')
			ver = session.expect(['>',pexpect.EOF])
			response = session.before
			#print response
			for line in response.split('\n'):
				if 'Pri' in line:
					start = line.find('Version:') +8 
					end = line.rfind(' ')
					version = line[start : end]
					#print version
					if 'T213' in version :
						print "The Switch IP "+host+" is running with a Router FW version "+version
						
					if 'T211' in version :
						print "The Switch IP "+host+" has "+version+" FW version"
						return
		if access == 1:
			print "The device IP "+host+" is not a Ruckus switch"
		if access == 2:
			print "The device IP "+host+" is not a Ruckus Switch"
	elif login == 1:
		print "The switch IP "+host+" is unreachable error timeout"
		print session.before
	elif login == 2:
		print "The switch IP "+host+" is unreachable error eof"
		print session.before

def fwverify2(host, password):
	# copy the firmware over and then reboots the switch.
	#pexpect.TIMEOUT='10'
	session = pexpect.spawn('ssh admin@' + host)
	login = session.expect(['assword:',pexpect.EOF, pexpect.TIMEOUT], timeout=10)
	if login == 0:
		session.sendline(password)
		access = session.expect(['>', pexpect.EOF, pexpect.TIMEOUT],timeout=10)
		if access == 0: 
			print "login success "
			session.sendline('show flash')
			ver = session.expect(['>',pexpect.EOF])
			response = session.before
			#print response
			for line in response.split('\n'):
				if 'Pri' in line:
					start = line.find('Version:') +8 
					end = line.rfind(' ')
					version = line[start : end]
					#print version
					if 'T213' in version :
						print "The Switch IP "+host+" is running with a Router FW version "+version
						#boot = raw_input('select which boot do you want to upgrade: primary/secondary: ')
						boot = 'primary'
						firmwarerepair(host, password, boot)
					if 'T211' in version :
						print "The Switch IP "+host+" has "+version+" FW version"
						return
		if access == 1:
			print "The device IP "+host+" is not a Ruckus switch"
		if access == 2:
			print "The device IP "+host+" is not a Ruckus Switch"
	elif login == 1:
		print "the switch IP "+host+" is unreachable error timeout"
		print session.before
	elif login == 2:
		print "the switch IP "+host+" is unreachable error eof"
		print session.before

def fwsikluEH(host, password,tftp):
	# copy the firmware over and then reboots the switch.
	#pexpect.TIMEOUT='10'
	session = pexpect.spawn('ssh admin@' + host)
	login = session.expect(['assword:',pexpect.EOF, pexpect.TIMEOUT], timeout=10)
	if login == 0:
		session.sendline(password)
		access = session.expect(['>', pexpect.EOF, pexpect.TIMEOUT],timeout=10)
		if access == 0: 
			print "login success"
			session.sendline('copy sw tftp://'+tftp+'/sikluEH')
			print 'firmware upgrading (EtherHaul antenna)'
			ver = session.expect(['>', pexpect.EOF, pexpect.TIMEOUT],timeout=200)
			response = session.before
			for line in response.split('\n'):
				if 'finished' in line:
					a=raw_input('Firmware upload complete. do you want to reboot the antenna now ? (Y/N) ')
					if a == 'y' :
						#session.expect(['>',pexpect.EOF])
						#print session.before
						session.sendline('run sw immediate no-timeout')
						#session.expect('.')
						time.sleep(3)
						print 'The antenna is rebooting'
						return
					if a == 'n' :
						print "The antenna is still running with the old firmware. It needs reboot"
						return
			print response
			return
			
		if access == 1:
			print "The device IP "+host+" is not a Siklu antenna"
		if access == 2:
			print "The device IP "+host+" is not a Siklu antenna"
	elif login == 1:
		print "The IP "+host+" is unreachable error timeout"
		print session.before
	elif login == 2:
		print "The IP "+host+" is unreachable error eof"
		print session.before

def fwsikluMH(host, password,tftp):
	# copy the firmware over and then reboots the switch.
	#pexpect.TIMEOUT='10'
	session = pexpect.spawn('ssh admin@' + host)
	login = session.expect(['assword:',pexpect.EOF, pexpect.TIMEOUT], timeout=10)
	if login == 0:
		session.sendline(password)
		access = session.expect(['>', pexpect.EOF, pexpect.TIMEOUT],timeout=10)
		if access == 0: 
			print "login success"
			session.sendline('copy sw tftp://'+tftp+'/sikluMH')
			print "firmware upgrading (MultiHaul antenna)"
			ver = session.expect(['>', pexpect.EOF, pexpect.TIMEOUT],timeout=300)
			response = session.before
			for line in response.split('\n'):
				if 'finished' in line:
					a=raw_input('Firmware upload complete. do you want to reboot the antenna now ? (Y/N) ')
					if a == 'y' :
						#session.expect(['>',pexpect.EOF])
						#print session.before
						session.sendline('run sw immediate no-timeout')
						#session.expect('.')
						time.sleep(3)
						print 'The antenna is rebooting'
						return
					if a == 'n' :
						print "The antenna is still running with the old firmware. It needs reboot"
						return
			print response
			return
			
		if access == 1:
			print "The device IP "+host+" is not a Siklu antenna"
		if access == 2:
			print "The device IP "+host+" is not a Siklu antenna"
	elif login == 1:
		print "The IP "+host+" is unreachable (timeout error)"
		print session.before
	elif login == 2:
		print "The IP "+host+" is unreachable (error eof)"
		print session.before

def determinesiklu(host, password):

	# Determines the model of the switch

	session = pexpect.spawn('ssh admin@' + host)

	session.expect(['assword:',pexpect.EOF, pexpect.TIMEOUT], timeout=10)

	#session.sendline(password)

	#session.expect('>')

	

	if "EH" in session.before:

		antenna = "EH"

	elif "MH" in session.before:

		antenna = "MH"

	else:
		antenna ="not found" 
	
	return antenna

def determinesikluprov():

	# Determines the model of the switch

	session = pexpect.spawn('ssh admin@192.168.0.1 ')
	
	session.expect(['assword:',pexpect.EOF, pexpect.TIMEOUT], timeout=10)
	
	
	

	
	#session.expect('>')
	
	

	if "TX" in session.before:

		antenna = "TX"

	elif "MH" in session.before:

		antenna = "MH" 

	return antenna
	
	#print "IP " +host+ " firmware version: 08.0.70aT211 "
def sikluprovMH(ssid,wpassword,hostname,snmplocation,userpassw):
	# copy the firmware over and then reboots the switch.
	#pexpect.timeout=10
	a='''# net-config configuring\n
set net-config config-file disable config-error-restart-delay 60 dhcp-relay disable\n
# password-strength configuring
set password-strength  min-length 8 min-difference 0\n
# configuring eth\n
set eth host  admin up\n
set eth host  auto-neg enabled\n
set eth host\n   
set eth eth-bu1  admin up\n
set eth eth-bu1\n   
set eth eth1  admin up\n
set eth eth1  eth-type 1000fd\n
set eth eth1  auto-neg enabled\n
set eth eth1\n   
set eth eth2  admin down\n
set eth eth2  eth-type 1000fd\n
set eth eth2  auto-neg enabled\n
set eth eth2\n   
set eth eth3  admin down\n
set eth eth3  eth-type 1000fd\n
set eth eth3  auto-neg enabled\n
set eth eth3\n   
# configuring lag aware parameters of eth\n
# bridge configuring\n
set bridge 1 name bridge-1 bridge-ports host, eth-bu1, eth1, eth2, eth3\n
# bridge-port configuring\n
# ip configuring\n
set ip 1 ip-addr static 192.168.0.1 prefix-len 24 vlan 0\n
set ip 2 ip-addr dhcp vlan 0\n
# route configuring\n
set system unit-mode normal\n
# fdb-table configuring\n
# arp configuring\n
# snmp-agent configuring\n
set snmp-agent read-com 14kingston write-com private snmp-version v2c\n
# snmp-mng configuring\n
# ntp configuring\n
set ntp 1  server 0.0.0.0\n
set ntp 1  secondary-server 0.0.0.0\n
set ntp 1  tmz 0\n
# aaa-server configuring\n
# configuring   event-cfg\n
set event-cfg temperature-high trap-mask no alarm-mask no threshold-high 55 threshold-low -30 hysteresis 1\n
# access-list configuring\n
set access-list 1 ip-addr 0.0.0.0 prefix-len 0\n
# aaa configuring\n
set aaa mode local shared-secret none connection-timeout 5 user-default-level user\n
# configuring   pse\n
set pse eth2 admin disable\n
set pse eth3 admin disable\n
	'''
	session = pexpect.spawn('ssh admin@192.168.0.1')
	login = session.expect(['assword:',pexpect.EOF, pexpect.TIMEOUT], timeout=10)
	if login == 0:
		session.sendline('admin')
		access = session.expect(['>', pexpect.EOF, pexpect.TIMEOUT],timeout=10)
		if access == 0: 
			print "login success"
			#session.sendline('hostname '+sitecode+'_WAN_SW')
		#session.expect('#')
		session.sendline(a)
		session.expect('>')
		session.sendline('set terminal-unit ssid '+ssid+' password '+wpassword)
		session.expect('>')
		session.sendline('set system contact Wifinity name '+hostname)
		session.expect('>')
		session.sendline('set system location '+snmplocation+' cli-timeout 15 loop-permission enabled')
		session.expect('>')
		session.sendline('set user admin passw '+userpassw)
		session.expect('>')
		session.sendline('copy running-configuration startup-configuration')
		session.expect('>')

			#print "enabled success"
		time.sleep(3)
		print 'The antenna was configured'
		session.close()
		return
		if access == 1:
			print "The device IP "+host+" is not a Siklu antenna"
		if access == 2:
			print "The device IP "+host+" is not a Siklu antenna"
	elif login == 1:
		print "The IP "+host+" is unreachable error timeout"
		print session.before
	elif login == 2:
		print "The IP "+host+" is unreachable error eof"
		print session.before
	return

def sikluprovEH(hostname,snmplocation,userpassw):
	# copy the firmware over and then reboots the switch.
	#pexpect.timeout=10
  
	session = pexpect.spawn('ssh admin@192.168.0.1')
	login = session.expect(['assword:',pexpect.EOF, pexpect.TIMEOUT], timeout=10)
	if login == 0:
		session.sendline('admin')
		access = session.expect(['>', pexpect.EOF, pexpect.TIMEOUT],timeout=10)
		if access == 0: 
			print "login success"
			#session.sendline('hostname '+sitecode+'_WAN_SW')
		#session.expect('#')
		
		session.sendline('set password-strength min-length 8 min-difference 0')
		session.expect('>')
		session.sendline('set ip 2 ip-addr dhcp vlan 0')
		session.expect('>')
		session.sendline('set system contact Wifinity name '+hostname)
		session.expect('>')
		session.sendline('set system location '+snmplocation+' cli-timeout 15 loop-permission enabled')
		session.expect('>')
		session.sendline('set user admin passw '+userpassw)
		session.expect('>')
		session.sendline('set snmp-agent read-com 14kingston write-com private snmp-version v2c')
		session.expect('>')
		session.sendline('copy running-configuration startup-configuration')
		session.expect('>')
		print 'Configuration completed'


			#print "enabled success"
		time.sleep(3)
		session.close()
		return
		if access == 1:
			print "The device IP "+host+" is not a Siklu antenna"
		if access == 2:
			print "The device IP "+host+" is not a Siklu antenna"
	elif login == 1:
		print "The IP "+host+" is unreachable error timeout"
		print session.before
	elif login == 2:
		print "The IP "+host+" is unreachable error eof"
		print session.before
	return

## Text menu in Python
	  
def print_menu():       ## Your menu design here
	print 30 * "-" , "MENU" , 30 * "-"
	print "1. Check Firmware Switches"
	print "2. Upgrade firmware Switches"
	print "3. Reboot all switches"
	print "4. Check Interfaces Status"
	print "5. Brocade 12p VLAN 1000 configuration"
	print "6. Brocade Sw provisioning"
	print "7. Brocade SW Firmware repair (from Router version to Switch version)"
	print "8. Change Switch Hostname"
	print "9. Check Switch uptime"
	print "10. Siklu Firmware upgrade"
	print "11. Siklu Antenna Provisioning"
	print "12. Exit"
	print 67 * "-"
  
loop=True      
  
while loop:          ## While loop which will keep going until loop = False
	print_menu()    ## Displays menu
	choice = raw_input("Enter your choice [1-12]: ")
 
	if choice=='1':     
		print "Check Firmware Switches"
		try:
			ipcrawl = addressRange() # provides the ip range as a list to crawl through
			password = getpass.getpass('Password: ') # password of the hosts
			#vmware = raw_input('insert vmware ip address: ') #vmware address
			start = time.time()
			for ip in range(int(ipcrawl[1]), int(ipcrawl[2]) + 1):
				host = ipcrawl[0] + str(ip)
				#upgrade(host, password) # login for brocade switch
				time.sleep(3)# wait added just because expect is bloody fast
				#copyandreboot(host, password, vmware) # copies fw into flash and reboots
				externalcommand='ssh-keygen -f "'+ssh+'/.ssh/known_hosts" -R '+host
				externalcommand2='ssh-keygen -f "/root/.ssh/known_hosts" -R '+host
				#print externalcommand
				os.system(externalcommand)
				os.system(externalcommand2)
				fwverify(host, password)
			print time.time() - start
		except KeyboardInterrupt:
			print "\nProgram stopped by user."
		#return

		## You can add your code or functions here
	elif choice=='2':
		print "Upgrade firmware Switches"
		try:
			ipcrawl = addressRange() # provides the ip range as a list to crawl through
			password = getpass.getpass('Password: ') # password of the hosts
			vmware = raw_input('insert tftp server ip address: ') #vmware address
			fwversion = raw_input('insert firmware version es. FI08070a    ')
			start = time.time()
			for ip in range(int(ipcrawl[1]), int(ipcrawl[2]) + 1):
				host = ipcrawl[0] + str(ip)
				externalcommand='ssh-keygen -f "'+ssh+'/.ssh/known_hosts" -R 192.168.0.1'
				externalcommand2='ssh-keygen -f "/root/.ssh/known_hosts" -R 192.168.0.1'
				#print externalcommand
				os.system(externalcommand)
				os.system(externalcommand2)
				#upgrade(host, password) # login for brocade switch
				time.sleep(3)# wait added just because expect is bloody fast
				copyandreboot(host, password, vmware, fwversion) # copies fw into flash and reboots
			print "waiting for the upgrade of primary images"
			time.sleep(130)
			for ip in range(int(ipcrawl[1]), int(ipcrawl[2]) + 1):
				host = ipcrawl[0] + str(ip)
				#upgrade(host, password) # login for brocade switch
				time.sleep(3)# wait added just because expect is bloody fast
				copyandrebootsecondary(host, password, vmware, fwversion) # copies fw into flash and reboots
			print "waiting for the upgrade of secondary images"
			time.sleep(130)
			print "verifing firwmare upgrade"
			for ip in range(int(ipcrawl[1]), int(ipcrawl[2]) + 1):
				host = ipcrawl[0] + str(ip)
				#upgrade(host, password) # login for brocade switch
				time.sleep(3)# wait added just because expect is bloody fast
				fwverify2(host, password)
				#fwverify(host, password)
			print time.time() - start
		except KeyboardInterrupt:
			print "\nProgram stopped by user."
		## You can add your code or functions here
	elif choice=='3':
		print "Reboot all switches"
		try:
			ipcrawl = addressRange() # provides the ip range as a list to crawl through
			password = getpass.getpass('Password: ') # password of the hosts
			#vmware = raw_input('insert vmware ip address: ') #vmware address
			start = time.time()
			for ip in range(int(ipcrawl[1]), int(ipcrawl[2]) + 1):
				host = ipcrawl[0] + str(ip)
				externalcommand='ssh-keygen -f "'+ssh+'/.ssh/known_hosts" -R 192.168.0.1'
				externalcommand2='ssh-keygen -f "/root/.ssh/known_hosts" -R 192.168.0.1'
				#print externalcommand
				os.system(externalcommand)
				os.system(externalcommand2)
				#upgrade(host, password) # login for brocade switch
				time.sleep(3)# wait added just because expect is bloody fast
				reboot(host, password) # copies fw into flash and reboots
			
			print time.time() - start
		except KeyboardInterrupt:
			print "\nProgram stopped by user."
		## You can add your code or functions here
	elif choice==4:
		print "Check Interfaces Status"
		try:

			ipcrawl = addressRange() # provides the ip range as a list to crawl through

			password = getpass.getpass('Password: ') # password of the hosts

			for ip in range(int(ipcrawl[1]), int(ipcrawl[2]) + 1):

				host = ipcrawl[0] + str(ip) 

				externalcommand='ssh-keygen -f "'+ssh+'/.ssh/known_hosts" -R '+host
				externalcommand2='ssh-keygen -f "/root/.ssh/known_hosts" -R '+host
				#print externalcommand
				os.system(externalcommand)
				os.system(externalcommand2)

				try:

					switch = determineswitch(host, password)

					if switch == "brocade24":

						brocade(host, password, switch) # login for brocade switch

					elif switch == "brocade12":

						brocade(host,password, switch)

					elif switch == "brocade48":

						brocade(host,password, switch)

					else:

						"Print couldn't determine switch model"

				except Exception as e:

					print "error"

		except KeyboardInterrupt:

			print "\nProgram stopped by user."



			#return

		## You can add your code or functions here
	elif choice=='5':
		print "Brocade 12p VLAN 1000 configuration"
		try:
			ipcrawl = addressRange() # provides the ip range as a list to crawl through
			#password = getpass.getpass('Password: ') # password of the hosts
			sitecode = raw_input('insert the sitecode: ') #sitecode
			ipaddr = raw_input('insert the sw ip address CIDR included Es. 100.96.1.201/24: ') #ip address
			ipgw = raw_input('insert the GW address: ') #sitecode
			start = time.time()
			for ip in range(int(ipcrawl[1]), int(ipcrawl[2]) + 1):
				host = ipcrawl[0] + str(ip)
				#upgrade(host, password) # login for brocade switch
				time.sleep(3)# wait added just because expect is bloody fast
				externalcommand='ssh-keygen -f "'+ssh+'/.ssh/known_hosts" -R '+host
				externalcommand2='ssh-keygen -f "/root/.ssh/known_hosts" -R '+host
				#print externalcommand
				os.system(externalcommand)
				os.system(externalcommand2)
				ruckusvlan1000(host,sitecode,ipaddr,ipgw) # copies fw into flash and reboots

			
			print time.time() - start
		except KeyboardInterrupt:
			print "\nProgram stopped by user."
		## You can add your code or functions here

	elif choice=='6':
		print "Brocade Sw provisioning"
		try:
			ipcrawl = addressRange() # provides the ip range as a list to crawl through
			password = getpass.getpass('Password: ') # password of the hosts
			#sitecode = raw_input('insert the sitecode: ') #sitecode
			#ipaddr = raw_input('insert the sw ip address CIDR included Es. 100.96.1.201/24: ') #ip address
			#ipgw = raw_input('insert the GW address: ') #sitecode
			start = time.time()
			for ip in range(int(ipcrawl[1]), int(ipcrawl[2]) + 1):

				host = ipcrawl[0] + str(ip) 
				externalcommand='ssh-keygen -f "'+ssh+'/.ssh/known_hosts" -R '+host
				externalcommand2='ssh-keygen -f "/root/.ssh/known_hosts" -R '+host
				#print externalcommand
				os.system(externalcommand)
				os.system(externalcommand2)

				try:

					switch = determineswitchprov(host)

					if switch == "brocade7250_24":

						brocadeprov7250_24(host)
						renameSws(host,password) # login for brocade switch

					elif switch == "brocade12":

						brocadeprov7150_12(host)
						renameSws(host,password)

					elif switch == "brocade7150_24":

						brocadeprov7150_24(host)
						renameSws(host,password)

					else:

						"Print couldn't determine switch model"

				except Exception as e:

					print "the IP "+host+" is unreachable"

		except KeyboardInterrupt:

			print "\nProgram stopped by user."

	elif choice=='7':
		print "Brocade SW Firmware repair (from Router version to Switch version)"
		try:
			ipcrawl = addressRange() # provides the ip range as a list to crawl through
			password = getpass.getpass('Password: ') # password of the hosts
			boot = raw_input('select which boot do you want to upgrade: primary/secondary: ') #sitecode
			#ipaddr = raw_input('insert the sw ip address CIDR included Es. 100.96.1.201/24: ') #ip address
			#ipgw = raw_input('insert the GW address: ') #sitecode
			start = time.time()
			for ip in range(int(ipcrawl[1]), int(ipcrawl[2]) + 1):
				host = ipcrawl[0] + str(ip)

				externalcommand='ssh-keygen -f "'+ssh+'/.ssh/known_hosts" -R '+host
				externalcommand2='ssh-keygen -f "/root/.ssh/known_hosts" -R '+host
				#print externalcommand
				os.system(externalcommand)
				os.system(externalcommand2)

				firmwarerepair(host, password, boot)

				

					
				#except Exception as e:

				   # print "the IP "+host+" is unreachable"

		except KeyboardInterrupt:

			print "\nProgram stopped by user."

	elif choice=='8':
		print "Change Switch Hostname"
		try:
			ipcrawl = addressRange() # provides the ip range as a list to crawl through
			password = getpass.getpass('Password: ') # password of the hosts
			#boot = raw_input('select which boot do you want to upgrade: primary/secondary: ') #sitecode
			#ipaddr = raw_input('insert the sw ip address CIDR included Es. 100.96.1.201/24: ') #ip address
			#ipgw = raw_input('insert the GW address: ') #sitecode
			start = time.time()
			for ip in range(int(ipcrawl[1]), int(ipcrawl[2]) + 1):
				host = ipcrawl[0] + str(ip)

				externalcommand='ssh-keygen -f "'+ssh+'/.ssh/known_hosts" -R '+host
				externalcommand2='ssh-keygen -f "/root/.ssh/known_hosts" -R '+host
				#print externalcommand
				os.system(externalcommand)
				os.system(externalcommand2)

				renameSws(host,password)

					
				#except Exception as e:

				   # print "the IP "+host+" is unreachable"

		except KeyboardInterrupt:

			print "\nProgram stopped by user."

	elif choice=='9':
		print "Check Switch uptime"
		try:
			ipcrawl = addressRange() # provides the ip range as a list to crawl through
			password = getpass.getpass('Password: ') # password of the hosts
			#boot = raw_input('select which boot do you want to upgrade: primary/secondary: ') #sitecode
			#ipaddr = raw_input('insert the sw ip address CIDR included Es. 100.96.1.201/24: ') #ip address
			#ipgw = raw_input('insert the GW address: ') #sitecode
			start = time.time()
			for ip in range(int(ipcrawl[1]), int(ipcrawl[2]) + 1):
				host = ipcrawl[0] + str(ip)
				externalcommand='ssh-keygen -f "'+ssh+'/.ssh/known_hosts" -R 192.168.0.1'
				externalcommand2='ssh-keygen -f "/root/.ssh/known_hosts" -R 192.168.0.1'
				#print externalcommand
				os.system(externalcommand)
				os.system(externalcommand2)

				

				sysuptime(host,password)

					
				#except Exception as e:

				   # print "the IP "+host+" is unreachable"

		except KeyboardInterrupt:

			print "\nProgram stopped by user."

	elif choice=='10':
		print "Siklu Firmware upgrade"
		try:
			ipcrawl = addressRange() # provides the ip range as a list to crawl through
			password = getpass.getpass('Password: ') # password of the hosts
			tftp = raw_input('insert the tftp IP address ') #sitecode
			#ipaddr = raw_input('insert the sw ip address CIDR included Es. 100.96.1.201/24: ') #ip address
			#ipgw = raw_input('insert the GW address: ') #sitecode
			start = time.time()
			for ip in range(int(ipcrawl[1]), int(ipcrawl[2]) + 1):
				host = ipcrawl[0] + str(ip)
				externalcommand='ssh-keygen -f "'+ssh+'/.ssh/known_hosts" -R '+host
				externalcommand2='ssh-keygen -f "/root/.ssh/known_hosts" -R '+host
				#print externalcommand
				os.system(externalcommand)
				os.system(externalcommand2)

				
				antenna=determinesiklu(host,password)
				print antenna
				if antenna == 'MH':
					fwsikluMH(host,password,tftp)

				elif antenna == 'EH':
					fwsikluEH(host,password,tftp)   
				#except Exception as e:
				else:
					print 'antenna not found'
					

				   # print "the IP "+host+" is unreachable"

		except KeyboardInterrupt:

			print "\nProgram stopped by user."

	elif choice=='11':
		print "Siklu Antenna Provisioning"
		try:
		
			externalcommand='ssh-keygen -f "'+ssh+'/.ssh/known_hosts" -R 192.168.0.1'
			externalcommand2='ssh-keygen -f "/root/.ssh/known_hosts" -R 192.168.0.1'
			#print externalcommand
			os.system(externalcommand)
			os.system(externalcommand2)
			#antenna='MH'
			antenna = determinesikluprov()
			#print antenna
			if antenna == "MH":
				ssid = raw_input('insert the SSID to use ')
				wpassword = raw_input('insert Wireless Security Password ')
				hostname = raw_input('insert Hostname ') #sitecode
				snmplocation = raw_input('insert the SNMP location ')
				userpassw = raw_input('insert admin password ')
				host = "192.168.0.1"
				password = "admin"
				tftp = raw_input('insert the TFTP IP address to use ')
				#ipgw = raw_input('insert the GW address: ') #sitecode
				start = time.time()

				fwsikluMH(host,password,tftp)
				time.sleep(100)
				
				sikluprovMH(ssid,wpassword,hostname,snmplocation,userpassw)

			elif antenna == "TX":
				hostname = raw_input('insert Hostname ') #sitecode
				snmplocation = raw_input('insert the SNMP location ')
				userpassw = raw_input('insert admin password ')
				host = "192.168.0.1"
				password = "admin"
				tftp = raw_input('insert the TFTP IP address to use ')
				#ipgw = raw_input('insert the GW address: ') #sitecode
				start = time.time()

				fwsikluEH(host,password,tftp)
				time.sleep(100)

				sikluprovEH(hostname,snmplocation,userpassw)    
				#except Exception as e:

				   # print "the IP "+host+" is unreachable"

		except KeyboardInterrupt:

			print "\nProgram stopped by user."

	elif choice=='12':
		print "Exit"

		## You can add your code or functions here
		loop=False # This will make the while loop to end as not value of loop is set to False
	else:
		# Any integer inputs other than values 1-5 we print an error message
		raw_input("Wrong option selection. Enter any key to try again..")



def main():
	try:
		print_menu
		os.system('rm /home/dany/.ssh/known_hosts')
		os.system('rm /root/.ssh/known_hosts" -R ')
	#try:
	 #   ipcrawl = addressRange() # provides the ip range as a list to crawl through
	  #  password = getpass.getpass('Password: ') # password of the hosts
	   # vmware = raw_input('insert vmware ip address: ') #vmware address
		#start = time.time()
		#for ip in range(int(ipcrawl[1]), int(ipcrawl[2]) + 1):
		 #   host = ipcrawl[0] + str(ip)
			#upgrade(host, password) # login for brocade switch
		  #  time.sleep(3)# wait added just because expect is bloody fast
		   # copyandreboot(host, password, vmware) # copies fw into flash and reboots
		#print time.time() - start
	#except KeyboardInterrupt:
	 #   print "\nProgram stopped by user."
	except KeyboardInterrupt:
		return

if __name__ == "__main__":
	main()
