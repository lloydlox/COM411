def movements ():
  path = ["Move Forward", "10","Move Backwards","5","Move Left","3","Move Right","1"]
  return path

def run ():
  print ("Moving...")
  x = movements ()
  print (x[0],"for",x[1],"steps")
  print ("Move",x[2],"for",x[3],"steps")
  print ("Move",x[4],"for",x[5], "steps")
  print ("Move",x[6],"for",x[7],"steps")

run ()