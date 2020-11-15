print ("Pleasw enter a sequence")
character = input ()
print ("Please enter the character for the marker")
marker = input ()
for x in character:
  lox = len(character)
  for y in character:
    kiki=character.count(marker)
    distance = lox-kiki
  #print (lox)
print ("The distance between the marker is",distance)
