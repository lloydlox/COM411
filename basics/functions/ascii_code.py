print ("Program started!")
print ("Please enter a standard charater")
character = input()
if len(character)==1:
  letter = ord(character)
  print (letter)
  print("The ASCII code for ",character, "is:" ,character)
else :
  print ("A single character was expected")