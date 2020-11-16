def cross_bridge (steps):# create a function
  #steps = int(0)
  for x in steps:
    if x < 5:
     print ("crossed step")
    elif steps > 5:
     print ("The bridge is collapsing")
    else:
     print ("We must keep going")    
cross_bridge(3)
cross_bridge(6)

