print ("How many bars should be charged?")
bars = int(input())
symbol = ("♥")
#print (symbol)
count = 0
while count < bars :
  count = count +1
  x = symbol * count
  print ("Charging",x)
print ("The battery is fully charged", end="") 