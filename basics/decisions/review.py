print ("What is the device mac")
mac = input ()
print ("What is the Device IP?")
ip = input ()
#print (mac)
#if mac [7] =="00:FC:00":
if (mac=="00:FC:00" ) and (ip =="192.168.0.20") :
 #if ip [-2]== ("2"):
   print ("This is a  Pelco camera add it to the camera list")
    #configure it with a 172.17.1.1  ip
elif (mac == "00:0F:BB") or (ip == "172.17.1.100"):
 print ("This is either a CMG or Storage add it to the CMG lists")
 print ("Further distinguish using serial number, enter serial number:")
      #configure it with the 172.17.1.100 going up
 serial = input ()
 if serial == "12341234":
    print ("This is definetely a CMG")
 else:
       print ("This is just a storage server")

#elif mac [7]==("Fc:09:33"):
 # print ("This is an EMU")
else:
  print ("Mac range not yet in our database",mac) 
  ###################################################################################################################################################################################