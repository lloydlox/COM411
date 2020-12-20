def directions():
  directions = ["Move Forward","Move Backwards","Turn Left", "Turn Right"]
  return directions

def menu ():
  print ("Please select a direction:")
  options = directions ()
  for x in range (len(options)):
    position = (options[x])
    print ((x), (position)) 

def run ():
  menu()
run ()  

