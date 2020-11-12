print ("What level of brightnes is required?")
level = int(input())
factor = 2
print ("Adjust brightness.....")
for x in range (0,level,factor):
  symbol = (x*"*")
  #print (level)
  print ("Beep's brightness level:",symbol)
  print ("Bop's brightness level:",symbol) 
  print ()