print ("Where should I look?")
place = input()
print (place)
if place == ("bedroom"):
 print ("Where in the bedroom should I look?")
 bed = input ()
 if bed == ("under the bed"):
  print (" Found some shoes but no battery")
 else:
   print ("Found some mess but not battery")

elif place == ("in the bathroom"):
 print  ("Where in the bathroom should I look?")
 bath = input()
 if bath == ("bathtub"):
  print ("Found a rubber duck but no battery")
 else:
    print ("Found a wet surface but no battery")
elif place == ("in the lab"):
 print("Where in the lab should I look")
 lab = input()
 if lab == ("on the table"):
  print ("Yes I found my battery")
 else:
   print("Found some tools but no battery")
else:
  print ("I do not know where that is but will keep looking")
  